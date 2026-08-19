from datetime import time

from plan2eplus.ops.schedules.interfaces.constants import (
    DAY_END_TIME,
    YEAR_START_DATE,
)
from plan2eplus.ops.schedules.interfaces.day import (
    TimeEntry,
    create_day_from_single_value,
    create_day_from_time_entries,
)
from plan2eplus.ops.schedules.interfaces.year import (
    YEAR_END_DATE,
    Date,
    DayEntry,
    create_year_from_day_entries_and_defaults,
)


class ExampleYear:
    other_val = 0
    dates = [
        Date.from_date(YEAR_START_DATE),
        Date(7, 1),
        Date(7, 2),
        Date(7, 3),
        Date.from_date(YEAR_END_DATE),
    ]

    basic_day = create_day_from_single_value(0)
    v1 = create_day_from_time_entries(
        [
            TimeEntry(time(7), other_val),
            TimeEntry(DAY_END_TIME, 1),
        ]
    )
    v2 = create_day_from_time_entries(
        [
            TimeEntry(time(8), 1),
            TimeEntry(DAY_END_TIME, other_val),
        ]
    )

    @property
    def year(self):
        d1, d2 = self.dates[1:3]
        day_entries = [
            DayEntry(d1, self.v1),
            DayEntry(d2, self.v2),
        ]
        return create_year_from_day_entries_and_defaults(day_entries, self.basic_day)
