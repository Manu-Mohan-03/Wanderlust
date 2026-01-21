from datetime import date, datetime, timedelta
from pydantic import BaseModel

class DateModel(BaseModel):
    ts: datetime

def get_current_date():
    current_date_obj = date.today()
    current_date = current_date_obj.strftime("%Y-%m-%d")
    return current_date


def get_current_datetime():
    current_datetime_obj = datetime.now()
    current_datetime_str = current_datetime_obj.strftime("%Y-%m-%dT%H:%M")
    return current_datetime_str


def is_valid_date_string(date_str: str, date_format="%Y-%m-%d"):
    """Check if a date in format YYYY-MM-DD is a valid date"""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def is_dates_in_order(from_date, to_date):
    if not is_valid_date_string(from_date):
        return False
    if not is_valid_date_string(to_date):
        return False

    from_date_obj = datetime.strptime(from_date,"%Y-%m-%d").date()
    to_date_obj = datetime.strptime(to_date,"%Y-%m-%d").date()

    if to_date_obj >= from_date_obj:
        return True
    return False


def add_minutes_to_datetime(datetime_str, time_period, date_format):
    datetime_obj = datetime.strptime(datetime_str, date_format)
    result_time = datetime_obj + timedelta(minutes=time_period)
    return datetime.strftime(result_time, date_format )


def convert_time(start_time, end_time=None):
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
    if end_time:
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S")
        if start_time_obj < end_time_obj:
            return end_time_obj.strftime("%H:%M")
        else:
            return end_time_obj.strftime("%H:%M") + "(+1)"
    else:
        return start_time_obj.strftime("%H:%M")

def parse_time(ts_str):
    """Convert timestamp in string format to HH:MM format"""
    ts_model = DateModel(ts=ts_str)
    return ts_model.ts.strftime("%H:%M")

def get_weekday(ts_str):
    datetime_obj = datetime.fromisoformat(ts_str)
    weekday_number = datetime_obj.isoweekday()
    return weekday_number

