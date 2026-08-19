from plan2eplus.ops.zones.user_interface import Room
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.range import Range

HEIGHT = 3.00  # m


class Ranges:
    X1 = Range(0, 1)
    X2 = Range(1, 2)
    Y1 = Range(0, 1)


class Domains:
    d1 = Domain(Ranges.X1, Ranges.Y1)
    d2 = Domain(Ranges.X2, Ranges.Y1)


class Rooms:
    r1 = Room(0, "room1", Domains.d1, HEIGHT)
    r2 = Room(1, "room2", Domains.d2, HEIGHT)
    # two_room_list = [r1, r2]

    @property
    def two_room_list(self):
        return [self.r1, self.r2]
