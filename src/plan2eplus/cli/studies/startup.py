from cyclopts import App

from plan2eplus.eppaths.logic import EpPaths

startup_app = App(name="sup")


@startup_app.command()
def fd():
    ep = EpPaths()
    return ep


# @startup_app.command()
# def try_config():
#     schema = OmegaConf.structured(EpConfig)
#     config_path = BASE_PATH / "config/test.yaml"
#     user_path = BASE_PATH / "config/user.yaml"
#     conf = OmegaConf.load(config_path)
#     user_conf = OmegaConf.load(user_path)
#     # the later config takes precednece..
#     res = OmegaConf.merge(schema, conf, user_conf)
#     print(OmegaConf.to_yaml(res))
#     return res
