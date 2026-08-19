from cyclopts import App
from utils4plans.logs import logset

from plan2eplus.cli.studies.startup import startup_app

# from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups

app = App(name="studies")
app.command(startup_app)


# @app.command()
# def study_case():
#     case = make_test_case(AFNEdgeGroups.A_ew)
#     zone_names = [i.zone_name for i in case.objects.zones]
#     logger.info(zone_names)
#
#
# @app.command()
# def curr():
#     test_surface_types()
#
#
# @app.command()
# def ty():
#     path = ProjectPaths.input_config.details
#     return get_details_from_yaml(path)
#
#     # test omega conf..


def main():
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
