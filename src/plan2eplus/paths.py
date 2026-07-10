import pyprojroot
from pathlib import Path


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))

CONFIG_PATH = BASE_PATH / "epconfig"


class Constants:
    # NOTE: these are just for testing, modules that call will have their own names
    idf_name = "out.idf"
    results_location = "results"
    sql_path = "results/eplusout.sql"
    schedule_location = "schedules"


# TODO: put this in config..
SEED = 1234


class StaticPaths:
    base = Path(BASE_PATH) / "static"
    inputs = base / "_01_inputs"
    plans = base / "_02_plans"
    models = base / "_03_models"
    temp = base / "_04_temp"
    figures = base / "_05_figures"


class InputConfigPaths:
    base = StaticPaths.inputs / "test_configs"
    edges = base / "edges.yaml"
    details = base / "details.yaml"


class ProjectPaths:
    input_config = InputConfigPaths
    pass
