from datetime import date, datetime, timedelta

def get_current_date():
    current_date_obj = date.today()
    current_date = current_date_obj.strftime("%Y-%m-%d")
    return current_date


def get_current_datetime():
    current_datetime_obj = datetime.now()
    current_datetime_str = current_datetime_obj.strftime("%Y-%m-%dT%H:%M")
    return current_datetime_str


def is_valid_date_string(date_str: str):
    """Check if a date in format YYYY-MM-DD is a valid date"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
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


def add_duration_to_datetime(datetime_str, duration):
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    return datetime_obj + timedelta(minutes=duration)


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


