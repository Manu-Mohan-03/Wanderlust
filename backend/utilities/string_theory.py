
def automate_tripname():
    pass

def weekdays_to_number(days: list[str])-> str:
    mapping = {
        "mon": "1",
        "tue": "2",
        "wed": "3",
        "thu": "4",
        "fri": "5",
        "sat": "6",
        "sun": "7",
    }
    number_list = sorted([mapping[day.lower()] for day in days])
    number_str = "".join(number_list)
    return number_str