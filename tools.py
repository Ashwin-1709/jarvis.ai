import pytz
from parser import *
from constants import *
from datetime import datetime, timezone, timedelta, date
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
    log_with_context(
        logging.INFO,
        f"fetch_upcoming_events_for_calendar() called with num_events: {num_events}.",
    )
    events = client.fetch_upcoming_calendar_events(count_events=num_events)
    if len(events) == 0:
        return "No upcoming events!"
    return parse_events(events)


@tool
def fetch_calendar_list() -> str:
    """
    Fetches all the calendars for the user.
    Format all the necessary information in human readable format before presenting to the user.
    """

    print("Fetching your calendar list, Please wait...")
    log_with_context(logging.INFO, f"fetch_calendar_list() called.")
    calendar_list = client.get_calendar_list()
    return parse_calendar_list(calendar_list)


@tool
def fetch_events_after_time(minutes: int = 0, hours: int = 0, days: int = 0) -> str:
    """
    Fetches calendar events occurring after a specified time offset from the current time.

    Args:
        minutes (int, optional): Number of minutes to offset the current time. Defaults to 0.
        hours (int, optional): Number of hours to offset the current time. Defaults to 0.
        days (int, optional): Number of days to offset the current time. Defaults to 0.
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    Do not list all the attendees.
    """

    print("Fetching upcoming meetings, Please wait...")
    log_with_context(
        logging.INFO,
        f"fetch_events_after_time() called with offset {minutes} mins {hours} hours {days} days.",
    )
    current_time = datetime.fromisoformat(
        datetime.now(timezone.utc).isoformat("T", "auto")
    )

    # Add the specified minutes, hours, and days
    delta = timedelta(minutes=minutes, hours=hours, days=days)
    future_time = current_time + delta

    # Convert the result back to the same ISO 8601 format
    target_time = future_time.isoformat("T", "auto")[:-6] + "Z"

    events = client.fetch_calendar_events(
        count_events=EVENT_LIMIT, after_date_time=target_time, before_start_time=None
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
    log_with_context(logging.INFO, "get_current_time() called.")
    user_timezone = pytz.timezone(USER_TIMEZONE)
    current_time = datetime.now(user_timezone).isoformat()

    return f"Current time in ISO format is: {current_time}"


@tool
def get_date_time_multiagent() -> str:
    """
    Get current date and time in ISO format. Do not worry about other aspects of the query, just answer the date time information.
    Examples:
        <begin>
            user: Am I free after 8 pm today?
            agent: return current date and time in ISO format
        <end>
        <begin>
            user: do I have any meetings tomorrow?
            agent: return current date and time in ISO format
        <end>
        <begin>
            user: schedule a reminder for 4 pm tomorrow
            agent: return current date and time in ISO format
        <end>
        <begin>
            user: what events are scheduled for tomorrow
            agent: return current date and time in ISO format
        <end>
    """
    print("Fetching the current time.")
    log_with_context(logging.INFO, "get_current_time() called.")
    user_timezone = pytz.timezone(USER_TIMEZONE)
    current_time = datetime.now(user_timezone).isoformat()

    return f"Current time in ISO format is: {current_time}"


@tool
def get_current_day_and_date() -> str:
    """
    Execute this function to get current day and date.

    Example output:
        Today's date is 2025-01-12
        Today's day is Sunday
    """
    today = date.today()
    log_with_context(logging.INFO, "get_current_day_and_date() called.")
    current_date = today.strftime("%Y-%m-%d")
    current_day = today.strftime("%A")  # Get the full weekday name (e.g., "Monday")
    return f"Today's date: {current_date}\nToday's day: {current_day}"


@tool
def fetch_calendar_events(
    count_events: int = EVENT_LIMIT,
    start_datetime: str = None,
    end_datetime: str = None,
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
    print("Fetching upcoming events, Please wait...")
    log_with_context(
        logging.INFO,
        f"fetch_calendar_events() called with {count_events} events {start_datetime} start & {end_datetime} end.",
    )
    if end_datetime:
        end_datetime += "+05:30"
        if not start_datetime:
            user_timezone = pytz.timezone(USER_TIMEZONE)
            start_datetime = datetime.now(user_timezone).isoformat()
        else:
            start_datetime += "+05:30"
    else:
        start_datetime += "+05:30"

    events = client.fetch_calendar_events(
        count_events=count_events,
        after_date_time=start_datetime,
        before_start_time=end_datetime,
    )

    if len(events) == 0:
        return "No upcoming events!"
    return parse_events(events)


@tool
def create_event(
    start_datetime: str,
    end_datetime: str,
    attendees: str = "",
    summary: str = "",
    description: str = "",
    event_type: str = "default",
) -> str:
    """
    Create an event in users calendar based on given data.

    Args:
        start_datetime (str): Start date time string in format %Y-%m-%dT%H:%M:%S like 2025-01-12T08:00:00.
        end_datetime (str): End date time string in format %Y-%m-%dT%H:%M:%S like 2025-01-12T08:00:00.
        attendees (str, optional): Comma separated string of attendee email addresses. Defaults to ''.
        summary (str, optional): Title of the event. Defaults to ''.
        description (str, optional): Description of the event. Defaults to ''.
        event_type(str, optional): Event type among ['default', 'focusTime', 'outOfOffice']. Defaults to 'default'.
        User may provide start_datetime end_datetime in different formats, you have to interpret it correctly.
        Examples:
            <begin>
                user: Setup a event for 12th Jan 2025, 8 pm to 11:30 pm
                agent: call function with `start_datetime` as 2025-01-12T20:00:00 and `end_datetime` as 2025-01-12T23:30:00
            <end>
            <begin>
                user: Setup 1 hour long 1:1 sync with dave@gmail.com for 3rd Jan, 5 pm
                agent: call function with `start_datetime` as 2025-01-03T17:00:00 and `end_datetime` as 2025-01-03T18:00:00, attendees as 'dave@gmail.com'
            <end>
            <begin>
                user: Create an event for sandra's party for 21st Sept 4 pm to 10 pm
                agent: call function with `start_datetime` as 2025-09-21T16:00:00 and `end_datetime` as 2025-09-21T22:00:00 and summary as "Sandra's Party"
            <end>
            <begin>
                user: Create an hour long group study session for algebra on 3rd Jan 5 pm adding sandra@gmail.com and dave@gmail.com
                agent: call function with `start_datetime` as 2025-01-03T17:00:00 and `end_datetime` as 2025-01-03T18:00:00, attendees as 'sandra@gmail.com,dave@gmail.com' and summary as "Algebra Study Session"
            <end>
            <begin>
                user: Add an event for 24th as sandra's birthday
                agent: call function with `start_datetime` as 2025-01-24T00:00:00 and `end_datetime` as 2025-01-24T23:59:59, summary as "sandra's birthday"
            <end>
            <begin>
                user: Add an event for 24th as annual check with dave@gmail.com. Promotions discussions need to be done in this.
                agent: call function with `start_datetime` as 2025-01-24T00:00:00 and `end_datetime` as 2025-01-24T23:59:59, attendees as 'dave@gmail.com', summary as "Annual Check", description as "Promotions discussions need to be done in this"
            <end>
            <begin>
                user: I will be going on japan trip from 13th march to 23rd march, schedule out of office / OOO time in my calendar.
                agent: call function with `start_datetime` as 2025-03-13T00:00:00 and `end_datetime` as 2025-03-23T23:59:59, summary as "Japan Trip", event_type as 'outOfOffice'
            <end>
            <begin>
                user: I do not want to be disturbed for 2 hours, schedule focus time / dnd / do not disturb on 5th Feb for 10 am.
                agent: call function with `start_datetime` as 2025-02-05T10:00:00 and `end_datetime` as 2025-02-05T12:00:00, event_type as 'focusTime'
            <end>
        End of examples
    """
    print("Creating a new event, Please wait...")
    log_with_context(
        logging.INFO,
        f"create_event() called with start: {start_datetime}, end: {end_datetime}, attendees: {attendees}, summary: {summary}, description: {description}.",
    )

    attendees = attendees.strip().split(",") if len(attendees) > 0 else list()
    event = client.create_event(
        start_datetime=start_datetime + "+05:30",
        end_datetime=end_datetime + "+05:30",
        attendees=attendees,
        summary=summary,
        description=description,
        event_type=event_type,
    )

    if event:
        return "Event created successfully!"
    else:
        return "Failed to create event."


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
    fetch_calendar_events,
    create_event,
]

datetime_agent_tools = [
    get_date_time_multiagent,
    get_current_day_and_date,
]

calendar_agent_tools = [
    fetch_upcoming_events_for_calendar,
    fetch_calendar_list,
    fetch_events_after_time,
    fetch_calendar_events,
    create_event,
]
