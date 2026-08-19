from pathlib import Path

import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))


class Constants:
    # NOTE: these are just for testing, modules that call will have their own names
    idf_name = "out.idf"
    results_location = "results"
    sql_path = "results/eplusout.sql"
    schedule_location = "schedules"
    config_path = Path(BASE_PATH) / "epconfig"


# TODO: put this in config..
SEED = 1234


# TODO: move this over.. to ex
