import pytest
import datetime

import Data_Handling.dates as dates

############create_end_date
def test_create_end_date_type_returned():
    assert isinstance(dates.create_end_date(), datetime.datetime)


# def test_create_end_date_value_returned():
#     assert

############create_start_date
def test_create_start_date_type_returned():
    end_date = datetime.datetime.now()
    assert isinstance(dates.create_start_date(end_date), datetime.datetime)


@pytest.mark.parametrize(
    'end_date,delta,start_date',
    (
            datetime.datetime(day=20, year=2020, month=7),
            datetime.timedelta(days=1),
            datetime.datetime(day=19, year=2020, month=7),
    ),
    (
            datetime.datetime(day=20, year=2020, month=7, hour=4, minute=5, second=20),
            datetime.timedelta(seconds=5),
            datetime.datetime(day=20, year=2020, month=7, hour=4, minute=5, second=15),
    ),
    (
            datetime.datetime(day=20, year=2020, month=7, hour=4, minute=5, second=20),
            datetime.timedelta(seconds=90),
            datetime.datetime(day=20, year=2020, month=7, hour=4, minute=3, second=50),
    ),
)
def test_create_start_date_value_returned(end_date, delta, start_date):
    assert dates.create_start_date(end_date=end_date, delta=delta) == start_date

############within
def test_within_type_returned():
    time1 = datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15)
    time2 = datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=10)
    assert isinstance(dates.within(time1=time1,time2=time2,days=1), bool)

@pytest.mark.parametrize(
    'time1,time2,weeks,days,hours,minutes,seconds,result',
    (
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15),
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=10),
        0,
        0,
        0,
        0,
        20,
        True,
    ),
    (
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15),
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=10),
        0,
        0,
        0,
        0,
        10,
        False,
    ),
    (
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15),
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=1, second=15),
        0,
        0,
        0,
        3,
        20,
        True,
    ),
    (
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15),
        datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=10),
        0,
        0,
        0,
        5,
        45,
        False,
    ),
)
def test_within_value_returned(
        time1,
        time2,
        weeks,
        days,
        hours,
        minutes,
        seconds,
        result
):
    assert dates.within(
        time1 = time1,
        time2 = time2,
        weeks = weeks,
        days = days,
        hours = hours,
        minutes = minutes,
        seconds=seconds
    ) == result

############datetime_to_str
def test_datetime_to_str_type_returned():
    assert isinstance(dates.datetime_to_str(datetime.datetime(day=20, year=2020, month=7)), str)


@pytest.mark.parametrize(
    'date,string',
    (datetime.datetime(day=20, year=2020, month=7), '2020-07-20 00:00:00'),
    (datetime.datetime(day=1, year=2001, month=12), '2001-12-01 00:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3), '2020-07-20 03:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5), '2020-07-20 03:01:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15), '2020-07-20 03:01:15'),
)
def test_datetime_to_str_value_returned(date, string):
    assert dates.datetime_to_str(date) == string


############str_to_datetime
def test_datetime_to_str_type_returned():
    assert isinstance(dates.str_to_datetime('2020-07-20 00:00:00'), datetime.datetime)


@pytest.mark.parametrize(
    'date,string',
    (datetime.datetime(day=20, year=2020, month=7), '2020-07-20 00:00:00'),
    (datetime.datetime(day=1, year=2001, month=12), '2001-12-01 00:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3), '2020-07-20 03:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5), '2020-07-20 03:01:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15), '2020-07-20 03:01:15'),
)
def test_str_to_datetime_value_returned(date, string):
    assert dates.str_to_datetime(string) == string
