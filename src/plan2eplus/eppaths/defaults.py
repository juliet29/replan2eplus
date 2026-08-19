from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileStructure:
    idd: str = "Energy+.idd"
    example_files: str = "ExampleFiles"
    weather_files: str = "WeatherData"
    data_sets: str = "DataSets"


@dataclass
class ConstructionNames:
    mat_and_const_idf: str = "ASHRAE_2005_HOF_Materials.idf"
    window_const_idf: str = "WindowConstructs.idf"
    window_glass_idf: str = "WindowGlassMaterials.idf"
    window_gas_idf: str = "WindowGasMaterials.idf"

    @property
    def material_idfs(self):
        return [self.mat_and_const_idf, self.window_glass_idf, self.window_gas_idf]

    @property
    def construction_idfs(self):
        return [self.mat_and_const_idf, self.window_const_idf]


@dataclass
class EpConfig:
    path_to_ep_install: Path = Path("")
    ep_dir: FileStructure = field(default_factory=FileStructure)
    default_weather: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
    default_constructions: ConstructionNames = field(default_factory=ConstructionNames)
