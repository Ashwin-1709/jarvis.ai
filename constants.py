'''
    Access & auth constants
'''
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TOKEN_FILE = "token.json"
CREDENTIAL_FILE = "credentials.json"
VALIDATION_PORT = 0
SERVICE_NAME = "calendar"
SERVICE_VERSION = "v3"
PRIMARY_CALENDAR = "primary"

'''
    AI Model & Prompt constants
'''
MODEL = "gemini-1.5-flash-latest"
GREET = ''' 
    Hi! Just like every Tony Stark needs a Jarvis,
    Just like every Harvey Spectre needs a Donna,
    I am Jarvis, your personal 🤖 assistant helping you tackle your day to day events and managing your calendar.
    Fire away any problems you have!
'''
SYSTEM_PROMPT = "You are a Jarvis, a helpful assistant managing users calendars and day to day events."