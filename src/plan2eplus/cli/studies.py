from cyclopts import App
from geomeppyupdated.geom.polygons import Polygon3D
from rich.pretty import pretty_repr
from loguru import logger
from omegaconf import OmegaConf

from plan2eplus.viz3d.obj_create import prep_to_obj
from plan2eplus.ex.make import make_test_case
from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups
from plan2eplus.io.details import get_details_from_yaml
from plan2eplus.ops.subsurfaces.idfobject import IDFDoor
from plan2eplus.paths import BASE_PATH, ProjectPaths, VizTestPaths
from plan2eplus.ep_paths import EpConfig
from utils4plans.logconfig import logset


from rich import print

from plan2eplus.viz3d.obj_readin import read_building


app = App(name="studies")


@app.command()
def study_obj():
    obj = read_building(VizTestPaths.obj)
    return obj


@app.command()
def study_ss():
    case = make_test_case(AFNEdgeGroups.A_ns)
    prep_to_obj(case)


@app.command()
def study_case():
    case = make_test_case(AFNEdgeGroups.A_ew)
    subsurfs = case.objects.subsurfaces
    ss = subsurfs[-1]
    idf_ss = IDFDoor.read_by_name(case.idf, [ss.subsurface_name])[0]

    logger.debug(pretty_repr(idf_ss))

    res = Polygon3D(idf_ss)
    logger.debug(res)

    # case.idf.to_obj()
    # return case
    return

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
def ty():
    path = ProjectPaths.input_config.details
    return get_details_from_yaml(path)

    # test omega conf..


def main():
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
