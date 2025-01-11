import json
from datetime import datetime
from langchain_core.tools import tool
from google_calendar_client import GoogleCalendarClient

client = GoogleCalendarClient()

@tool
def fetch_upcoming_events_for_calendar(num_events: int) -> str:
    """
    Fetches upcoming events from users calendars. 
    Execute the function with parameter `num_events` depicting the number of upcoming calendar events to be fetched.
    Format the start and end time of events to human readable format like 25th Jan, 8pm - 10pm.
    """

    print("Looking for your upcoming events, Please wait...")
    events = client.fetch_upcoming_calendar_events(count_events = num_events)
    if len(events) == 0:
        return "No upcoming events!"
    
    context = "Here are the upcoming calendar events for the users: \n\n"
    cnt_event = 1

    for event in events:
        context += f"{cnt_event}. "
        filtered_event_details = dict()
        fields = ['summary', 'description']
        for field in fields:
            if field in event:
                filtered_event_details[field] = event[field]
        for time in ['start', 'end']:
            dt_obj = datetime.fromisoformat((event[time]['dateTime']))
            filtered_event_details[time] = dt_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
        context += json.dumps(filtered_event_details)
        cnt_event += 1
    return context

@tool
def fetch_calendar_list() -> str:
    """
    Fetches all the calendars for the user.
    Format all the necessary information in human readable format before presenting to the user.
    """

    print('Fetching your calendar list, Please wait...')
    calendar_list = client.get_calendar_list()
    context = "Here are the different calendars for the user: \n\n"

    cnt_calendars = 1
    for calendar in calendar_list:
        fields = ["id", "summary", "description", "kind"]
        context += f"{cnt_calendars}. "
        filtered_calendar_details = dict()
        for field in fields:
            if field in calendar:
                filtered_calendar_details[field] = calendar[field]
        
        context += json.dumps(filtered_calendar_details)
        cnt_calendars += 1
    
    return context

@tool
def end_chat() -> None:
    """
        Execute this function if user is satisfied and wants to end chat.
    """
    print("Goodbye, will see you again 👋")
    exit(0)

tools = [fetch_upcoming_events_for_calendar, fetch_calendar_list, end_chat]

