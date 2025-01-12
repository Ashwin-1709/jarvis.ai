import json
from parser import *
from constants import *
from datetime import datetime, timezone, timedelta
from langchain_core.tools import tool
from google_calendar_client import GoogleCalendarClient

client = GoogleCalendarClient()

@tool
def fetch_upcoming_events_for_calendar(num_events: int) -> str:
    """
    Fetches upcoming events from users calendars. 
    Execute the function with parameter `num_events` depicting the number of upcoming calendar events to be fetched.
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    Do not list all the attendees.
    """

    print("Looking for your upcoming events, Please wait...")
    events = client.fetch_upcoming_calendar_events(count_events = num_events)
    if len(events) == 0:
        return "No upcoming events!"
    return parse_events(events)

@tool
def fetch_calendar_list() -> str:
    """
    Fetches all the calendars for the user.
    Format all the necessary information in human readable format before presenting to the user.
    """

    print('Fetching your calendar list, Please wait...')
    calendar_list = client.get_calendar_list()
    return parse_calendar_list(calendar_list)


@tool
def fetch_events_after_time(
    minutes: int = 0,
    hours: int = 0,
    days: int = 0
) -> str:
    """
    Fetches calendar events occurring after a specified time offset from the current time.

    Args:
        minutes (int, optional): Number of minutes to offset the current time. Defaults to 0.
        hours (int, optional): Number of hours to offset the current time. Defaults to 0.
        days (int, optional): Number of days to offset the current time. Defaults to 0.
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    Do not list all the attendees.
    """
    
    print('Fetching upcoming meetings, Please wait...')
    current_time = datetime.fromisoformat(datetime.now(timezone.utc).isoformat('T', 'auto'))
    
    # Add the specified minutes, hours, and days
    delta = timedelta(minutes = minutes, hours = hours, days = days)
    future_time = current_time + delta
    
    # Convert the result back to the same ISO 8601 format
    target_time = future_time.isoformat('T', 'auto')[:-6] + 'Z'

    events = client.fetch_calendar_events(
        count_events = EVENT_LIMIT, 
        after_date_time = target_time,
        before_start_time = None
    )

    if len(events) == 0:
        return "No upcoming events!"
    return parse_events(events)

@tool
def get_events_after_particular_datetime(date_time: str) -> str:
    """
    Fetches upcoming events after a particular `date_time`.

    Args:
        `date_time` (str): Date time string in format %Y-%m-%dT%H:%M:%S
        Example: 2015-05-28T09:00:00
        User will not provide date time in this exact format, you have to interpret it and formulate it.
        Examples:
            <begin>
                <user>: Do I have any meetings after 4th Jan?
                <agent>: call get_current_time() and extract year from current time.
                <agent>: call get_events_after_particular_datetime() with `date_time` as 2025-01-04T00:00:00

                <user> Do i have any meetings after 4 pm on 4th Jan 2025?
                <agent>: call get_events_after_particular_datetime() with `date_time` as 2025-01-04T16:00:00

                <user> what are the meetings I have after 23rd Feb 2025?
                <agent> call get_events_after_particular_datetime() with `date_time` as 2025-02-23T00:00:00
            <end>
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    Do not list all the attendees.
    """

    # TODO: Implement this
    print(f"Calling function with date_time {date_time}")

@tool
def get_current_time() -> str:
    """
    Get current date and time in ISO format.
    """
    print("Fetching the current time.")
    return datetime.now().isoformat()

@tool
def end_chat() -> None:
    """
        Execute this function if user is satisfied and wants to end chat.
    """
    print("Goodbye, will see you again 👋")
    exit(0)

tools = [
    fetch_upcoming_events_for_calendar,
    fetch_calendar_list,
    get_current_time,
    fetch_events_after_time,
    end_chat
]
