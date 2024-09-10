import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import timedelta

class GoogleCalendarSync:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.creds = None
        self.service = None
        self.load_credentials()

    def load_credentials(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def add_event(self, calendar_id, match):
        """
        Create and add a Google Calendar event for the match.
        """
        # ISO format datetime already includes the timezone offset
        start_time = match.data_timestamp.isoformat()  # Already timezone-aware
        end_time = (match.data_timestamp + timedelta(hours=2)).isoformat()  # Already timezone-aware

        event = {
            'summary': f"{match.team_left} vs {match.team_right}",
            'description': f"Tournament: {match.tournament}\nStreams: {', '.join([str(stream) for stream in match.streams.values()])}",
            'start': {
                'dateTime': start_time,  # timezone info is included in isoformat
            },
            'end': {
                'dateTime': end_time,  # timezone info is included in isoformat
            }
        }

        try:
            event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except Exception as e:
            print(f"An error occurred: {e}")