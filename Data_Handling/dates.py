import datetime


def create_end_date() -> datetime.datetime:
    return datetime.datetime.now()


def create_start_date(
        end_date: datetime.datetime,
        delta: datetime.timedelta = datetime.timedelta(days=0.5),
) -> datetime.datetime:
    return end_date - delta


def round_down(
        time: datetime.datetime,
        increment: str = 'minute',
) -> datetime.datetime:
    allowed_values = ['microsecond','second','minute','hour']
    if not isinstance(increment, str) or increment.lower() not in allowed_values:
        raise Exception(f"""
        Value passed ({increment}) for increment was not valid. 
        Should be a string and one of the following values:
        {', '.join(allowed_values)}"""
                        )
    time_parameters = {}
    for allowed_value in allowed_values:
        if allowed_value==increment.lower():
            break
        time_parameters.update(
            {
                allowed_value:0
            }
        )
    return time.replace(**time_parameters)



def within(
        time1: datetime.datetime,
        time2: datetime.datetime,
        weeks: float = 0,
        days: float = 0,
        hours: float = 0,
        minutes: float = 0,
        seconds: float = 0,
) -> bool:
    delta = datetime.timedelta(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

    return abs(time1 - time2) < delta


def datetime_to_str(date: datetime.datetime) -> str:
    if isinstance(date, str):
        return date
    else:
        return date.strftime('%Y-%m-%d %H:%M:%S')


def str_to_datetime(date: str) -> datetime.datetime:
    if isinstance(date, datetime.datetime):
        return date
    else:
        return datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
