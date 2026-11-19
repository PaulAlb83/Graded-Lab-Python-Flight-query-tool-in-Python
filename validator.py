"""Row validation: airport list loading, single-row checks, record building."""
import math
from datetime import datetime

def _has_datetime_format(text):
    if len(text) != 16:
        return False
    for i in range(16):
        ch = text[i]
        if i == 4 or i == 7:
            if ch != "-":
                return False
        elif i == 10:
            if ch != " ":
                return False
        elif i == 13:
            if ch != ":":
                return False
        else:
            if not ("0" <= ch <= "9"):
                return False
    return True


def _is_valid_datetime(text):
    if not _has_datetime_format(text):
        return False
    try:
        datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        return False
    return True


def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
  
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return {l for l in lines if l != "" and l[0] != "#"}


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
    raise NotImplementedError


def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    raise NotImplementedError
