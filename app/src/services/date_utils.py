import datetime


def utc_date() -> datetime.date:
    return datetime.datetime.now(tz=datetime.UTC).date()
