import re

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


def is_email_valid(email_id):
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9]+[._]?[a-zA-Z0-9]+[@]\w+[.]\w+$'
    if re.match(regex, email_id):
        return True
    else:
        return False


if __name__ == "__main__":
    print(is_email_valid("Test@test.com"))