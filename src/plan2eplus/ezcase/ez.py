from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from plan2eplus.eppaths.logic import EpPaths
from plan2eplus.ezcase.objects import read_existing_objects
from plan2eplus.ezcase.utils import (
    RunSettings,
    initialize_idd,
    open_idf,
)
from plan2eplus.io.files import get_or_make_folder_path
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
from plan2eplus.paths import Constants


@dataclass
class EZ:
    idf_path: Path | None = None
    read_existing: bool = True
    config_path: Path = Constants.config_path
    run_settings: RunSettings = field(default_factory=RunSettings)

    def __post_init__(self):
        logger.info("Initializing EzCase.. ")
        if not self.config_path.exists():
            raise Exception(
                f"Could not find the path to config: {self.config_path}. Please ensure this is well-defined to enable finding the EnergyPlus installation"
            )

        self.ep_paths = EpPaths(self.config_path)
        if self.run_settings.epw_path is None:
            self.run_settings.epw_path = self.ep_paths.default_weather

        initialize_idd(self.ep_paths.idd_path)
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

    def add_airflow_network(self, afn_input: AFNInput | None = None):
        if afn_input is None:
            afn_input = AFNInput()
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
        construction_inputs: ConstructionInput | None = None,
    ):
        if not construction_inputs:
            construction_inputs = default_construction_input(self.ep_paths)
        cpaths, mpaths, cset = construction_inputs
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
        output_path: Path | None = None,
        additional_variables: list[str] = [],
        run=False,
        save=True,
    ):
        if output_path:
            self.run_settings.output_path = output_path
        settings = self.run_settings
        logger.debug(settings)

        assert settings.epw_path
        write_run_period_and_location(
            self.idf, settings.analysis_period, settings.epw_path
        )

        add_output_variables(self.idf, additional_variables)

        if save or run:
            get_or_make_folder_path(settings.output_root())

        if self.objects.schedules:
            get_or_make_folder_path(settings.output_schedules_path)
            create_schedules(
                self.idf, self.objects.schedules, settings.output_schedules_path
            )

        if save:
            self.idf.saveas(settings.output_idf_path)

        if run:
            if not self.idf_path:
                self.idf.idfabsname = settings.output_idf_path
            self.idf.epw = settings.epw_path
            self.idf.run(
                output_directory=settings.output_results_path,
                weather=settings.epw_path,
            )
            # touch the schedules path..
