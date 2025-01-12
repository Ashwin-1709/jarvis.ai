import pytz
from parser import *
from constants import *
from datetime import (
    datetime,
    timezone,
    timedelta,
    date
)
from langchain_core.tools import tool
from google_calendar_client import GoogleCalendarClient
from logger import log_with_context, logging

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
    log_with_context(logging.INFO, f'fetch_upcoming_events_for_calendar() called with num_events: {num_events}.')
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
    log_with_context(logging.INFO, f'fetch_calendar_list() called.')
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
    log_with_context(logging.INFO, f'fetch_events_after_time() called with offset {minutes} mins {hours} hours {days} days.')
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
def get_current_time() -> str:
    """
    Get current date and time in ISO format.
    """
    print("Fetching the current time.")
    log_with_context(logging.INFO, 'get_current_time() called.')
    return datetime.now().isoformat()

@tool
def get_current_day_and_date() -> str:
    """
    Execute this function to get current day and date.
    
    Example output:
        Today's date is 2025-01-12
        Today's day is Sunday
    """
    today = date.today()
    log_with_context(logging.INFO, 'get_current_day_and_date() called.')
    current_date = today.strftime("%Y-%m-%d")
    current_day = today.strftime("%A")  # Get the full weekday name (e.g., "Monday")
    return f"Today's date: {current_date}\nToday's day: {current_day}"

@tool
def fetch_calendar_events(
    count_events: int = EVENT_LIMIT,
    start_datetime: str = None,
    end_datetime: str = None
) -> str:
    """
    Fetches `count_events` number of calendar events between `start_datetime` and `end_datetime`.

    Args:
        count_events (int, optional): Number of events to fetch. Defaults to 0.
        start_datetime (str, optional): Start date time string in format %Y-%m-%dT%H:%M:%S. Defaults to None.
        end_datetime (str, optional): Start date time string in format %Y-%m-%dT%H:%M:%S. Defaults to None.
        User may provide datetime strings in different formats, you have to interpret it and format it correctly before sending to the function.
        Examples:
            <begin>
                user: Do I have any events between 1st Jan 2025 and 5th Jan 2025?
                agent: call function with `start_datetime` as 2025-01-01T00:00:00 and `end_datetime` as 2025-01-05T23:59:59 
            <end>
                user: Show me my events from 10 am to 2 pm on 15th Feb 2025.
                agent: call function with `start_datetime` as 2025-02-15T10:00:00 and `end_datetime` as 2025-02-15T14:00:00
            <begin>
                user: what are the events I have on 4th Jan 2025?
                agent: call function with `start_datetime` as 2025-01-04T00:00:00 and `end_datetime` as 2025-01-04T23:59:59
            <end>
            <begin>
                user: what are the events I have after 4th Jan 2025 4 am?
                agent: call function with just `start_datetime` as 2025-01-04T04:00:00
            <end>
            <begin>
                user: what are the meetings I have before 4th Jan 2025 4 am?
                agent: call function with just `end_datetime` as 2025-01-04T04:00:00
            <end>
        End of examples 
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    Do not list all the attendees.
    """
    print('Fetching upcoming events, Please wait...')
    log_with_context(logging.INFO, f'fetch_calendar_events() called with {count_events} events {start_datetime} start & {end_datetime} end.')
    if end_datetime:
        end_datetime += '+05:30'
        if not start_datetime:
            user_timezone = pytz.timezone('Asia/Kolkata')
            start_datetime = datetime.now(user_timezone).isoformat()
    else: 
        start_datetime += '+05:30'
        
    events = client.fetch_calendar_events(
        count_events = count_events, 
        after_date_time = start_datetime,
        before_start_time = end_datetime
    )

    if len(events) == 0:
        return "No upcoming events!"
    return parse_events(events)
    

@tool
def end_chat() -> None:
    """
        Execute this function if user is satisfied or wants to end chat.
    """
    print("Goodbye, will see you again 👋")
    exit(0)

tools = [
    fetch_upcoming_events_for_calendar,
    fetch_calendar_list,
    get_current_time,
    fetch_events_after_time,
    end_chat,
    fetch_calendar_events
]
