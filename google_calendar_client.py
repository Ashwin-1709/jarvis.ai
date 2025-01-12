from datetime import datetime
import os.path
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
from constants import *
from logger import log_with_context, logging


class GoogleCalendarClient:
    def __init__(self) -> None:
        """
        Initializes the GoogleCalendarClient instance.
        Sets up the token and builds the service.
        """
        self.setup_token()
        self.build_service()
        log_with_context(logging.INFO, 'Google Calendar client setup done.')
        pass


    def setup_token(self) -> None:
        """
        Sets up the credentials for accessing the Google Calendar API.
        If a valid token file exists, it loads the credentials from the file.
        If the credentials are expired or do not exist, it initiates the OAuth flow to obtain new credentials.
        """
        self.creds = None
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIAL_FILE, SCOPES
                )
                self.creds = flow.run_local_server(port=VALIDATION_PORT)

                with open(TOKEN_FILE, "w") as token:
                    token.write(self.creds.to_json())

    def build_service(self) -> None:
        """
        Builds the Google Calendar API service using the credentials.
        """
        try:
            self.calendar_service = build(
                SERVICE_NAME, SERVICE_VERSION, credentials=self.creds
            )
        except HttpError as err:
            raise Exception(f"Cannot connect to the service: {err}")
        
    def fetch_calendar_events(
        self,
        count_events: int,
        after_date_time: str,
        before_start_time: str,
        calendar: str = PRIMARY_CALENDAR
    ) -> List[Dict]:
        """
        Fetches input number of events from a specific calendar after a certain date time.
        """
        orderByField = "startTime"
        if after_date_time is None:
            orderByField = "endTime"
        try:
            events_result = (
                self.calendar_service.events()
                .list(
                    calendarId = calendar,
                    timeMin = after_date_time,
                    timeMax = before_start_time,
                    maxResults = min(count_events, EVENT_LIMIT),
                    singleEvents=True,
                    orderBy = orderByField,
                )
                .execute()
            )
            events = events_result.get("items", [])
            return events
        except HttpError as err:
            log_with_context(logging.ERROR, f"Cannot fetch calendar entries: {err}. Please try again later!")

    def fetch_upcoming_calendar_events(
        self,
        count_events: int,
        calendar: str = PRIMARY_CALENDAR
    ) -> List[Dict]:
        """
        Fetches input number of upcoming events from a specific calendar.
        """
        user_timezone = pytz.timezone('Asia/Kolkata')
        cur_time = datetime.now(user_timezone).isoformat()
        return self.fetch_calendar_events(
            count_events = count_events,
            after_date_time = cur_time,
            before_start_time = None,
            calendar = calendar
        )

    def get_calendar_list(self) -> None:
        """
        Retrieves and prints the list of calendars.
        """
        try:
            calendar_list = self.calendar_service.calendarList().list().execute()
            calendars = calendar_list.get("items", [])
            return calendars
        except HttpError as error:
            log_with_context(logging.ERROR, f'An error occurred: {error}')
