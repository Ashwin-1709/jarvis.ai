import json
from datetime import datetime
from typing import List, Dict
from constants import (
    EVENT_INFO_PREFIX,
    FILTERED_EVENT_FIELDS,
    CALENDAR_INFO_PREFIX,
    FILTERED_CALENDAR_FIELDS,
)


def copy_fields(source: Dict, fields: List) -> Dict:
    """
    Copies a subset of fields of a source dictionary to a new destination dictionary.
    """
    dest = dict()
    for field in fields:
        if field in source:
            dest[field] = source[field]
    return dest


def parse_events(events: List[Dict]) -> str:
    """
    Parses the list of calendar events to act as an input for LLM.
    Filters the necessary information for the events.
    """
    content = EVENT_INFO_PREFIX
    event_count = 1

    for event in events:
        content += f"\n{event_count}. "
        for field in FILTERED_EVENT_FIELDS:
            if field in event:
                if field == "attendees":
                    content += "attendees: "
                    email = list()
                    for a in event[field]:
                        if "self" in a and a["self"]:
                            continue
                        email.append(a["email"])
                    content += ",".join(email) + "\n"
                else:
                    content += f"{field}: {event[field]}\n"
        for time in ["start", "end"]:
            content += f"{time}: {convert_datetime(event[time]['dateTime'])}\n"
        event_count += 1

    return content


def parse_calendar_list(calendars: List[Dict]) -> str:
    """
    Parses the list of different calendars user has to act as an input for LLM.
    Filters the necessary information for the calendars.
    """

    content = CALENDAR_INFO_PREFIX
    calendar_count = 1

    for calendar in calendars:
        content += f"{calendar_count}. "
        filtered_calendar = copy_fields(calendar, FILTERED_CALENDAR_FIELDS)
        content += json.dumps(filtered_calendar)
        calendar_count += 1

    return content


def convert_datetime(_datetime: str) -> str:
    """
    Convert datetime to %Y-%m-%d %H:%M:%S %Z format.
    """
    dt_obj = datetime.fromisoformat(_datetime)
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
