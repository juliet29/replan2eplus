from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from plan2eplus.ezcase.objects import read_existing_objects
from plan2eplus.ezcase.utils import (
    RunVariablesInput,
    handle_run_variables,
    initialize_idd,
    open_idf,
)
from plan2eplus.ops.afn.create import create_afn_objects
from plan2eplus.ops.afn.user_interface import AFNInput
from plan2eplus.ops.airboundary.create import update_airboundary_constructions
from plan2eplus.ops.constructions.create import create_constructions
from plan2eplus.ops.constructions.user_interface import (
    ConstructionInput,
    default_construction_input,
)
from plan2eplus.ops.output.create import add_output_variables
from plan2eplus.ops.run_settings.user_interfaces import (
    AnalysisPeriod,
    write_run_period_and_location,
)
from plan2eplus.ops.schedules.create import create_schedules
from plan2eplus.ops.subsurfaces.create import create_subsurfaces
from plan2eplus.ops.subsurfaces.interfaces import (
    Edge,
)
from plan2eplus.ops.subsurfaces.user_interfaces import SubsurfaceInputs
from plan2eplus.ops.zones.create import create_zones
from plan2eplus.ops.zones.user_interface import Room


@dataclass
class EZ:
    idf_path: Path | None = None
    output_path: Path | None = None  # TODO: shouldnt need output path anymore..
    epw_path: Path | None = None
    analysis_period: AnalysisPeriod | None = None
    read_existing: bool = True

    def __post_init__(self):
        print("Initializing EzCase.. ")
        initialize_idd()
        self.idf = open_idf(self.idf_path)
        self.objects = read_existing_objects(self.idf, self.read_existing)

    def add_zones(self, rooms: list[Room]):

        self.objects.zones, self.objects.surfaces = create_zones(self.idf, rooms)
        return self

    def add_subsurfaces(
        self, subsurface_inputs: SubsurfaceInputs, airboundary_edges: list[Edge] = []
    ):
        self.objects.airboundaries = update_airboundary_constructions(
            self.idf, airboundary_edges, self.objects.zones, self.objects.surfaces
        )
        # TODO the airboundaries should be part of the subsurface inputs.. -> detail or airboundary description ..

        self.objects.subsurfaces = create_subsurfaces(
            subsurface_inputs, self.objects.surfaces, self.objects.zones, self.idf
        )
        return self

    def add_airflow_network(self, afn_input: AFNInput = AFNInput()):
        self.objects.airflow_network = create_afn_objects(
            self.idf,
            self.objects.zones,
            self.objects.subsurfaces,
            self.objects.airboundaries,
            afn_input,
        )
        return self

    def add_constructions(
        self,
        construction_inputs: ConstructionInput = default_construction_input,  # TODO decide if the name will be singular or plural, also should the defaults be this high up? -> BUILD CONSTRUCTIONS INTO THE OBJECT!
    ):
        # TODO have a default construction set
        cpaths, mpaths, cset = (
            construction_inputs  # TODO: add construction inputs to function definition
        )
        create_constructions(
            self.idf,
            cpaths,
            mpaths,
            cset,
            self.objects.surfaces,
            self.objects.subsurfaces,
        )
        return self

    def save_and_run(
        self,
        run_vars: RunVariablesInput = RunVariablesInput(),
        output_path: Path | None = None,
        additional_variables: list[str] = [],
        run=False,
        save=True,
    ):
        op = output_path if output_path else self.output_path
        vars = handle_run_variables(run_vars, op)
        # TODO: write tests for different combos of variables
        logger.debug(vars)

        write_run_period_and_location(self.idf, vars.analysis_period, vars.epw_path)

        add_output_variables(self.idf, additional_variables)

        if self.objects.schedules:
            create_schedules(
                self.idf, self.objects.schedules, vars.output_schedules_path
            )

        if save:
            # NOTE: cannot change epw at this point and expect it to be saved..
            # TODO: add a check of this..
            self.idf.saveas(vars.output_idf_path)

        if run:
            if not self.idf_path:
                self.idf.idfabsname = vars.output_idf_path
            self.idf.epw = vars.epw_path
            # TODO: figure out why it is nessecary to set the weather again when it was not needed before..
            self.idf.run(
                output_directory=vars.output_results_path, weather=vars.epw_path
            )
            # touch the schedules path..
