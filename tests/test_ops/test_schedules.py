from datetime import time

from plan2eplus.ops.schedules.interfaces.constants import YEAR_START_DATE
from plan2eplus.ops.schedules.interfaces.day import (
    DAY_END_TIME,
    DAY_START_TIME,
    TimeEntry,
    create_day_from_single_value,
    create_day_from_time_entries,
    initialize_array,
    update_arr,
)
from plan2eplus.ops.schedules.interfaces.year import (
    Date,
    DayEntry,
    create_year_from_day_entries_and_defaults,
    create_year_from_single_value,
    initialize_year_array,
    update_year_arr,
)
from plan2eplus.cli.studies.ex.schedule import ExampleYear


# TODO put into a class as well?
def create_expected_day():
    arr = initialize_array(DAY_START_TIME, DAY_END_TIME)
    t1, t2, t3, t4 = [DAY_START_TIME, time(6, 0), time(9, 15), time(23, 59)]
    v1, v2, v3 = [0, 1, 0]
    arr = update_arr(arr, t1, t2, v1)
    arr = update_arr(arr, t2, t3, v2)
    arr = update_arr(arr, t3, t4, v3)
    return arr


def test_create_day():
    time_entries = [
        TimeEntry(time(6), 0),
        TimeEntry(time(9, 15), 1),
        TimeEntry(time(23, 59), 0),
    ]
    res = create_day_from_time_entries(time_entries)
    exp = create_expected_day()
    assert (res.arr == exp).all()
    # return res


def test_create_day_from_single_value():
    value = 100
    res = create_day_from_single_value(value)
    assert (res.arr == value).all()


class TestYear(ExampleYear):
    def create_expected_year(self):
        arr = initialize_year_array()
        dstart, d1, d2, d3, dend = self.dates
        arr = update_year_arr(arr, dstart, d1, self.basic_day)
        arr = update_year_arr(arr, d1, d2, self.v1)
        arr = update_year_arr(arr, d2, d3, self.v2)
        arr = update_year_arr(arr, d3, dend, self.basic_day)
        return arr

    def test_create_year_with_defaults(self):
        exp = self.create_expected_year()
        assert (self.year.arr == exp).all()


def test_create_year_from_single_value():
    year = create_year_from_single_value(1)
    assert (year.arr).all()


if __name__ == "__main__":
    ty = TestYear()
    ty.test_create_year_with_defaults()
    # print(ty.create_expected_year())
    # res = initialize_year_array()
    # print(res)
