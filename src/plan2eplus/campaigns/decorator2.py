from pathlib import Path
from typing import Any, Callable, NamedTuple
from dataclasses import dataclass
from itertools import product
from loguru import logger
from rich import print
from utils4plans.lists import chain_flatten
from utils4plans.io.names import create_date_string
from plan2eplus.io.files import get_or_make_folder_path, write_toml
from rich.pretty import pretty_repr


class Option:
    def __init__(self, name, IS_DEFAULT=False) -> None:
        self.name: str = name
        self.IS_DEFAULT = IS_DEFAULT

    @property
    def toml(self):
        return (
            {"name": self.name}
            if not self.IS_DEFAULT
            else {"name": self.name, "DEFAULT": self.IS_DEFAULT}
        )


class ModificationSelection(NamedTuple):
    name: str
    selection: str

    @property
    def toml(self):
        return {self.name: self.selection}


class Variable(NamedTuple):
    name: str
    options: list[Option]

    def __post_init__(self):
        self.check_only_one_default_option()
        self.check_names_are_unique()

    def check_only_one_default_option(self):
        res = [i for i in self.options if i.IS_DEFAULT]
        assert len(res) == 1

    def check_names_are_unique(self):
        res = [i.name for i in self.options]
        assert len(set(res)) == len(res)

    @property
    def default_option(self):
        return [i.name for i in self.options if i.IS_DEFAULT][0]

    @property
    def non_default_options(self):
        return [i.name for i in self.options if not i.IS_DEFAULT]

    @property
    def non_default_selections(self):
        return [
            ModificationSelection(i, j)
            for i, j in product([self.name], self.non_default_options)
        ]

    @property
    def toml(self):
        return {"name": self.name, "options": [i.toml for i in self.options]}


class ExperimentDef(NamedTuple):
    case_name: str
    modification: ModificationSelection | None = None

    @property
    def toml(self):
        d1 = {"case": self.case_name}
        d2 = {"modifications": "" if not self.modification else self.modification.toml}
        res = {**d1, **d2}
        return res


@dataclass
class DefinitionDict:
    case_names: list[str]
    case_variables: list[str]  # zones, surfaces
    modifications: list[Variable]

    # TODO can this be extended to handle prodycts?
    @property
    def experiments(self):
        def define_mod_experiments(mod: Variable):
            return [
                ExperimentDef(i, j)
                for i, j in product(
                    self.case_names,
                    mod.non_default_selections,
                )
            ]

        default_cases = [ExperimentDef(i) for i in self.case_names]
        modification_cases = chain_flatten(
            [define_mod_experiments(mod) for mod in self.modifications]
        )

        return default_cases + modification_cases

    @property
    def toml(self):
        d = {}
        d["case_names"] = self.case_names
        d["case_variables"] = self.case_variables
        d["modifications"] = [i.toml for i in self.modifications]
        return d


@dataclass
class DataDict:
    case: dict[str, dict[str, list]]
    mods: dict[str, dict[str, Any]]  # really will be list

    def verify_match_defn_dict(self, defn_dict: DefinitionDict):
        assert set(self.case.keys()) == set(
            defn_dict.case_variables
        ), "Case Variables do not match"
        # TODO!
        # check case names  -> A, B, C
        # check modification variable name + options.. -> some typing here for sure..

    @property
    def toml(self):
        return {"case": self.case, "mods": self.mods}


def create_func_params(
    exp: ExperimentDef, data_dict: DataDict, defn_dict: DefinitionDict
):
    exp.case_name
    defn_dict.case_variables
    # dictionary is better than list here..
    case_values = {k: v[exp.case_name] for k, v in data_dict.case.items()}
    mod_values = {}
    # Actually this is the default behavior,
    for mod in defn_dict.modifications:
        default = mod.default_option
        mod_values[mod.name] = data_dict.mods[mod.name][default]
    if exp.modification:
        mod = exp.modification
        mod_values[mod.name] = data_dict.mods[mod.name][mod.selection]
    return case_values, mod_values
    # TODO some checks to make sure these are aligned


# TODO add to config
EXP_TOML_NAME = "metadata"
DATA_TOML_NAME = "data"
DEFN_TOML_NAME = "defn"


class ExperimentGenerationError(Exception):
    def __init__(self, ix: int, exp: ExperimentDef, reason: str) -> None:
        self.ix = ix
        self.exp = exp
        self.reason = reason

        self.message()

    def message(self):
        print(f"Error generating exp {self.ix}: {self.exp.case_name}")


def prepare_experiment(
    ix: int,
    exp: ExperimentDef,
    data_dict: DataDict,
    defn_dict: DefinitionDict,
    func: Callable,
    campaign_path: Path,
):
    print(f"\nExp {ix} | {exp}")
    exp_name = f"{ix:03}"
    exp_path = get_or_make_folder_path(campaign_path / exp_name)
    write_toml(exp.toml, exp_path, EXP_TOML_NAME)

    # write metadata.toml to path
    # return path to case so that out.idf can be saved..

    case_values, mod_values = create_func_params(exp, data_dict, defn_dict)
    try:
        case = func(**case_values, **mod_values, out_path=exp_path)
    except (AssertionError, IndexError, ValueError) as e:
        logger.error(e)
        raise ExperimentGenerationError(ix, exp, str(e)) from e

    return case


def write_campaign_toml(
    data_dict: DataDict,
    defn_dict: DefinitionDict,
    campaign_name: str,
    campaign_path: Path,
):
    metadata = {"date": create_date_string(), "name": campaign_name}
    write_toml(metadata, campaign_path, EXP_TOML_NAME)
    # write_toml(data_dict.toml, campaign_path, DATA_TOML_NAME)
    write_toml(defn_dict.toml, campaign_path, DEFN_TOML_NAME)


def make_experimental_campaign(
    defn_dict: DefinitionDict,
    data_dict: DataDict,
    root_path: Path,
    campaign_name: str = "",
    OVERWRITE=False,
):
    def decorator_experimental_campaign(func):
        def wrapper(*args, **kwargs):
            campaign_full_name = f"{create_date_string()}_{campaign_name}"
            campaign_path = get_or_make_folder_path(root_path / campaign_full_name)
            write_campaign_toml(data_dict, defn_dict, campaign_name, campaign_path)

            experiments = defn_dict.experiments
            logger.success(f"Have initialized {len(experiments)} experiments!")
            failed_experiments = []
            success_expeiments = []
            for ix, exp in enumerate(experiments):
                try:
                    prepare_experiment(
                        ix, exp, data_dict, defn_dict, func, campaign_path
                    )
                except ExperimentGenerationError as e:
                    logger.error(
                        f"Faied to create experiment for {exp.case_name}... Moving on.."
                    )

                    failed_experiments.append((ix, exp.case_name, e.reason))
                    continue
                success_expeiments.append((ix, exp.case_name))

            logger.info(f"Failed expeiment details: {pretty_repr(failed_experiments)}")
            logger.info(f"Failed case names:{[i[1] for i in failed_experiments]}")
            logger.info(f"Success case names:{[i[1] for i in success_expeiments]}")
            logger.success(
                f"Failed: {len(failed_experiments)}. Success: {len(success_expeiments)}"
            )

            return

        return wrapper

    return decorator_experimental_campaign
