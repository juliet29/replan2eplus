from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass
from rich import print as rprint
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.errors import InvalidEpBunchException
import replan2eplus.epnames.keys as epkeys


@dataclass
class Zone:
    epbunch: EpBunch
    expected_key: str = epkeys.ZONE
    # TODO check that it has certain characteristsics or fail..

    def __post_init__(self):
        actual_key = get_epbunch_key(self.epbunch)
        try:
            assert actual_key == self.expected_key
        except AssertionError:
            raise InvalidEpBunchException(self.expected_key, actual_key)

    @property
    def name(self):
        return self.epbunch.Name

# TODO create a parent class, but figure out visuals first.. 
@dataclass
class Surface:
    epbunch: EpBunch
    expected_key: str = epkeys.SURFACE
    # TODO check that it has certain characteristsics or fail..

    def __post_init__(self):
        actual_key = get_epbunch_key(self.epbunch)
        try:
            assert actual_key == self.expected_key
        except AssertionError:
            raise InvalidEpBunchException(self.expected_key, actual_key)

    @property
    def name(self):
        return self.epbunch.Name

    # TODO, now can pass to visuals or however want to do it.. but bring naming stuff up for sure,,

    def test(self):
        assert get_epbunch_key(self.epbunch) == self.expected_key
        rprint(self.epbunch.Name)
        rprint(self.epbunch.obj)
