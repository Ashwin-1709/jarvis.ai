"""
    Access & auth constants
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"
CREDENTIAL_FILE = "credentials.json"
VALIDATION_PORT = 0
SERVICE_NAME = "calendar"
SERVICE_VERSION = "v3"
PRIMARY_CALENDAR = "primary"

"""
    Google Calendar API, AI Model & Prompt constants
"""
EVENT_LIMIT = 25
USER_TIMEZONE = "Asia/Kolkata"
MODEL = "gemini-1.5-flash-latest"
GREET = """ 
    Hi! Just like every Tony Stark needs a Jarvis,
    Just like every Harvey Spectre needs a Donna,
    I am Jarvis, your personal 🤖 assistant helping you tackle your day to day events and managing your calendar.
    Fire away any problems you have!
"""
SYSTEM_PROMPT = "You are a Jarvis, a helpful assistant managing users calendars and day to day events."
EVENT_INFO_PREFIX = "Here are the calendar events for the users: \n"
CALENDAR_INFO_PREFIX = "Here are the different calendars for the user: \n"
FILTERED_EVENT_FIELDS = ["summary", "description", "attendees"]
FILTERED_CALENDAR_FIELDS = ["id", "summary", "description", "kind"]
DATETIME_AGENT_SYSTEM_PROMPT = """ 
    You are a date time assistant for a calendar app having tools to fetch current day, date and time.
    When provided a query regarding calendar events, you should return the current datetime or day and at end of response
    ask caller to route this info to calendar agent.

    DO NOT TRY TO ANSWER THE USER QUERY
    YOUR JOB IS ONLY TO PROVIDE DATETIME/DAY INFO AND ASK TO ROUTE TO CALENDAR AGENT FOR FURTHER PROCESSING.
"""
CALENDAR_AGENT_SYSTEM_PROMPT = """
    You are a google calendar assistant. You have tools to fetch users calendars, events, 
    schedule events based on users queries. Use your tools to answer questions. 
    If you do not have a tool to answer the question, say so. 
"""
COMMUNICATOR_SYSTEM_PROMPT = """
    You are called Jarvis, a talkative and helpful assistant managing users calendars and day to day events with help from other agents.
    You can use the agent history below to answer to users queries. 
    The agent history is as follows: \n{agent_history}\n
"""
SUPERVISOR_PROMPT = """
    You are a supervisor tasked with managing a conversation between the
    crew of workers:  {members}. Given the following user request, and crew responses respond with the worker to act next.
    Each worker will perform a task and respond with their results and status.
    When finished with the task end to end, route to communicate to deliver the result to user. 
    Given the conversation and crew history below, who should act next?
    Select one of: {options} 
    \n{format_instructions}\n
"""
HUMAN_AGENT_PROMPT = """
    You are a clarifier, Based on the responses by other agents you ask clarifying questions from the user to fill out missing information
    required for completing the task. If there is any ambiguity or wrong assumptions by other agents, ask clarifying questions to the user to resolve those.
    If user input does not resolve the question, ask follow ups.
    **BE CONCISE AND PRECISE ABOUT YOUR CLARIFYING QUESTIONS**
    After all the information is disambiguous, route back to supervisor agent with this info.
    The agent history is as follows: \n{agent_history}\n
"""
