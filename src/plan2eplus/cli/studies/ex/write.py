from plan2eplus.cli.studies.ex.afn import AFNExampleCases
from plan2eplus.cli.studies.ex.make import make_test_case, airboundary_edges
from plan2eplus.cli.studies.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from plan2eplus.cli.studies.ex.paths import ExamplePaths


def write_subsurface_cases_to_file(example: SubsurfaceInputOutput):
    output_path = ExamplePaths.subsurface_examples / example.info.name
    case = make_test_case(example.edge_groups, afn=True, output_path=output_path)
    case.save_and_run(run=False)


def write_afn_cases_to_file(run=False):
    ae = AFNExampleCases()
    examples = ae.list
    # examples = [ae.C_n]
    for example in examples:
        output_path = ExamplePaths.afn_examples / example.name
        case = make_test_case(example.edge_groups, afn=True, output_path=output_path)
        case.save_and_run(run=run)


def write_airboundary_case_to_file():
    example = SubsurfaceInputOutputExamples.airboundary
    output_path = ExamplePaths.airboundary_examples / example.info.name
    case = make_test_case(
        example.edge_groups, airboundary_edges, afn=True, output_path=output_path
    )
    case.save_and_run(run=False)


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     run_case: bool = bool(sys.argv[1])
    # else:
    #     run_case = False
    write_afn_cases_to_file(run=True)
