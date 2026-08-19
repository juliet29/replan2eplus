import os
from dataclasses import dataclass
from pathlib import Path

from loguru import logger
from omegaconf import OmegaConf
from rich.pretty import pretty_repr

from plan2eplus.eppaths.defaults import EpConfig
from plan2eplus.errors import InvalidPathError
from plan2eplus.paths import CONFIG_PATH


def handle_user_config(path: Path, schema):
    if not path.exists():
        logger.warning(f"Looked for `user.yaml` at {path} but couldn't find it")
        return None

    user_config = OmegaConf.load(path)
    if not user_config:
        logger.warning(f"`user.yaml` at {path} is empty! Falling back...")
        return None
    config = OmegaConf.merge(schema, user_config)
    return config


def handle_default_configs(base_path: Path, schema):
    current_env = os.environ.get("APP_ENV")
    if not current_env:
        current_env = "dev"

    path = base_path / f"{current_env}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Config file is needed, but none was found at {path}")

    core_config = OmegaConf.load(path)
    config = OmegaConf.merge(schema, core_config)
    return config


@dataclass
class EpPaths:
    def __post_init__(self):
        schema = OmegaConf.structured(EpConfig)

        base_path = (
            CONFIG_PATH  # TODO: make some sort of property when integrate with ezcase..
        )
        config = handle_user_config(base_path / "user.yaml", schema)
        if not config:
            config = handle_default_configs(base_path, schema)

        self.config: EpConfig = OmegaConf.to_object(config)  # pyright: ignore[reportAttributeAccessIssue]

        logger.success(f"Succesfully read config: {pretty_repr(self.config)}")

    def get_path(self, name: str | Path):
        if not self.config.path_to_ep_install.exists():
            raise Exception(
                f"Don't know where to look for EnergyPlus! - path_to_ep_install does not exist: {self.config.path_to_ep_install}"
            )
        path = self.config.path_to_ep_install / name
        if not path:
            raise InvalidPathError(name, path)
        return path

    @property
    def idd_path(self):
        return self.get_path(self.config.ep_dir.idd)

    @property
    def default_weather(self):
        return self.get_path(
            Path(self.config.ep_dir.weather_files) / self.config.default_weather
        )

    @property
    def example_files(self):
        return self.get_path(self.config.ep_dir.example_files)

    @property
    def material_idfs(self):
        return [
            self.get_path(Path(self.config.ep_dir.data_sets) / i)
            for i in self.config.default_constructions.material_idfs
        ]

    @property
    def construction_idfs(self):
        return [
            self.get_path(Path(self.config.ep_dir.data_sets) / i)
            for i in self.config.default_constructions.construction_idfs
        ]
