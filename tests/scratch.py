from replan2eplus.ezcase.defaults import PATH_TO_IDD
from replan2eplus.ezcase.examples import get_example_idf
from replan2eplus.ezcase.main import EZCase
from replan2eplus.paths import static_paths
from replan2eplus.ezobjects.zone import Zone


if __name__ == "__main__":
    idf = get_example_idf()
    z = idf.get_zones()
    print(z)
