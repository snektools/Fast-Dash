import pytest
import datetime

import Data_Handling.dates as dates


def test_create_end_date_type_returned():
    assert isinstance(dates.create_end_date(), datetime.datetime)


def test_create_end_date_value_returned():
    assert dates


def test_create_start_date_type_returned():
    end_date = datetime.datetime.now()
    assert isinstance(dates.create_start_date(end_date), datetime.datetime)

@pytest.mark.parametrize(
    'date,expected_string',
    (datetime.datetime(day=20, year=2020, month=7), '2020-07-20 00:00:00'),
    (datetime.datetime(day=1, year=2001, month=12), '2001-12-01 00:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3), '2020-07-20 03:00:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5), '2020-07-20 03:01:00'),
    (datetime.datetime(day=20, year=2020, month=7, hour=3, minute=5, second=15), '2020-07-20 03:01:15'),
)
def test_datetime_to_str_type_returned(date, expected_string):
    assert  dates.datetime_to_str(date) == expected_string