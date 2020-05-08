from datetime import datetime

def serialize_datetime(dt:datetime) -> str:
    if isinstance(dt, datetime):
        return "{}-{}-{} {}:{}".format(dt.year, dt.month, dt.day, dt.hour, dt.minute)

def deserialize_datetime(datetimestr:str) -> datetime:
    return datetimestr.strptime(datetimestr, '%Y-%m-%d %H:%M')