from cyclopts import App
from loguru import logger
from omegaconf import OmegaConf

from plan2eplus.cli.pretest.surfaces import test_surface_types
from plan2eplus.ex.make import make_test_case
from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups
from plan2eplus.io.details import get_details_from_yaml
from plan2eplus.paths import BASE_PATH, ProjectPaths
from plan2eplus.ep_paths import EpConfig
from utils4plans.logs import logset

app = App(name="studies")


@app.command()
def study_case():
    case = make_test_case(AFNEdgeGroups.A_ew)
    zone_names = [i.zone_name for i in case.objects.zones]
    logger.info(zone_names)


@app.command()
def try_config():
    schema = OmegaConf.structured(EpConfig)
    config_path = BASE_PATH / "config/test.yaml"
    user_path = BASE_PATH / "config/user.yaml"
    conf = OmegaConf.load(config_path)
    user_conf = OmegaConf.load(user_path)
    # the later config takes precednece..
    res = OmegaConf.merge(schema, conf, user_conf)
    print(OmegaConf.to_yaml(res))
    return res


@app.command()
def curr():
    test_surface_types()


@app.command()
def ty():
    path = ProjectPaths.input_config.details
    return get_details_from_yaml(path)

    # test omega conf..


def main():
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
