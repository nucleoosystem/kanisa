from datetime import date


def date_has_passed(src):
    if not src:
        return False

    today = date.today()
    return src < today


def today_in_range(sd, ed):
    if not sd and not ed:
        # If no start date or end date is provided, today is in the provided
        # range.
        return True

    today = date.today()

    if sd and sd > today:
        # We've got a start date, and it's not happened yet.
        return False

    if ed and ed < today:
        # We've got a finish date which has passed.
        return False

    return True
