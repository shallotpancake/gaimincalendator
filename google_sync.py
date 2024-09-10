from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import timedelta
import os
import pickle

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

    def create_unique_id(self, match):
        """
        Creates a unique identifier for a match based on teams and timestamp.
        """
        return f"{match.team_left}_vs_{match.team_right}_{match.data_timestamp.isoformat()}"

    def search_event_by_unique_id(self, calendar_id, unique_id):
        """
        Searches for an event with a given unique identifier in extendedProperties.
        """
        events_result = self.service.events().list(
            calendarId=calendar_id,
            privateExtendedProperty=f"matchId={unique_id}",
            maxResults=1,
            singleEvents=True
        ).execute()

        events = events_result.get('items', [])
        return events[0] if events else None

    def add_or_update_event(self, calendar_id, match):
        """
        Adds a new event or updates an existing one if found using a unique identifier.
        """
        start_time = match.data_timestamp.isoformat()  # Start time of the event
        unique_id = self.create_unique_id(match)  # Generate a unique ID for the match

        existing_event = self.search_event_by_unique_id(calendar_id, unique_id)

        event = {
            'summary': f"{match.team_left} vs {match.team_right}",
            'description': f"Tournament: {match.tournament}\nStreams: {', '.join([str(stream) for stream in match.streams.values()])}",
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': (match.data_timestamp + timedelta(hours=2)).isoformat(),
                'timeZone': 'UTC'
            },
            'extendedProperties': {
                'private': {
                    'matchId': unique_id  # Store the unique identifier
                }
            }
        }

        if existing_event:
            # Update the existing event
            event_id = existing_event['id']
            print(f"Updating existing event: {event['summary']}")
            self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        else:
            # Create a new event
            print(f"Creating new event: {event['summary']}")
            self.service.events().insert(calendarId=calendar_id, body=event).execute()
