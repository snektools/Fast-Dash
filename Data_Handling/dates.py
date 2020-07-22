import datetime


def create_end_date():
    return datetime.datetime.now()


def create_start_date(end_date, delta: datetime.timedelta = datetime.timedelta(days=0.5)):
    return end_date - delta


def datetime_to_sql(date):
    if isinstance(date, str):
        output = date
    else:
        output = date.strftime('%Y-%m-%d %H:%M:%S')
    return f"'{output}'"


def within(
        time1,
        time2,
        weeks=0,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
):
    delta = datetime.timedelta(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

    return abs(time1 - time2) < delta
