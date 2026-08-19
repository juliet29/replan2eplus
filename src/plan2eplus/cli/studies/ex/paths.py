from pathlib import Path

from plan2eplus.paths import BASE_PATH


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


class ExamplePaths:
    THROWAWAY_PATH = BASE_PATH / "throwaway"
    results_for_tests = StaticPaths.models / "results_for_tests"
    trials = StaticPaths.models / "trials"
    ORTHO_CASE_RESULTS = results_for_tests / "ortho"
    CAMPAIGN_TESTS = results_for_tests / "campaigns"
    subsurface_examples = results_for_tests / "subsurface_examples"
    afn_examples = results_for_tests / "afn_examples"
    airboundary_examples = results_for_tests / "airboundary_examples"
    test_scheds = StaticPaths.temp / "test_scheds"
    ts_open = test_scheds / "open"
    ts_dynamic = test_scheds / "dynamic"
    ts_closed = test_scheds / "closed"
