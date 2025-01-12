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
