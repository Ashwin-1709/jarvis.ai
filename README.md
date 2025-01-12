## Jarvis

![CodeQL Review](https://github.com/Ashwin-1709/jarvis.ai/actions/workflows/codeql.yml/badge.svg)

Jarvis is a personal AI assistant designed to help you manage your day-to-day events and calendar. It leverages Google Calendar API and a gemini AI model to provide a seamless experience.

### Features

- **Google Calendar Integration**: Fetch and manage your calendar events.
- **Conversational AI**: Interact with Jarvis using natural language.
- **Memory Management**: Keeps track of the conversation context.

### Upcoming
- **More Calendar Features**: Creating, modifying events, checking conflicts, scheduling events, event attachments & files and more!
- **Web UI**: User friendly UI to interact with **Jarvis**.


For now, Jarvis can be used from terminal
### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ashwin-1709/jarvis.ai
    cd jarvis
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your API keys:
    - Follow the steps required for obtaining authorization for Google Calendar APIs from [Google Cloud Console](https://developers.google.com/calendar/api/quickstart/python#enable_the_api)
    - Create Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
    - Create a `.env` file in the root directory.
    - Add your GEMINI_API_KEY and other necessary configurations:
        ```
        GEMINI_API_KEY=your_google_api_key
        ```

### Usage

1. Run the Jarvis assistant:
    ```sh
    python jarvis.py
    ```

2. Interact with Jarvis through the command line.

### Example

```
Hi! Just like every Tony Stark needs a Jarvis,
Just like every Harvey Spectre needs a Donna,
I am Jarvis, your personal 🤖 assistant helping you tackle your day to day events and managing your calendar.
Fire away any problems you have!

> Hi Jarvis, what are the next 2 meetings I have?

Looking for your upcoming events, Please wait...
Here are your next 2 meetings:
1. Trip Planning, 11th Jan, 10pm - 12am
2. Weekly Friday Sync, 17th Jan, 11.30pm - 1.30am

> what are the calendars I have?
Fetching your calendar list, Please wait...
Here are your calendars:
1. Primary
2. Birthdays
3. Holidays in India

> Do I have any conflicts in next 4 meetings?
Looking for your upcoming events, Please wait...
Based on your next 4 meetings, there are no conflicts.

> Do I have any meetings with sriram after 2 days? 
Fetching upcoming meetings, Please wait...
Yes, you have two meetings with sriram after 2 days: Weekly Friday Sync on 24th Jan, 11pm - 1:30am and Trip Planning on 25th Jan, 10pm - 12am.

> Who will be i meeting in for the weekly friday sync?
Looking for your upcoming events, Please wait...
Besides you, <redacted> will be in the Weekly Friday Sync.

> meetings I have after 2 months
Fetching upcoming meetings, Please wait...
Here are your meetings after 2 months:

*   Flight to <redacted> on March 13th, 7:55pm - March 14th, 3am
*   Flight to <redacted> on March 14th, 7am - 8:10am
*   Weekly Friday Sync on March 14th, 11pm - March 15th, 1:30am

> Thanks Jarvis, I am done

Goodbye, will see you again 👋
```
