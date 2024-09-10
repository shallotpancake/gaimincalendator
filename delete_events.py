from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

class GoogleCalendarCleaner:
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

    def delete_all_events(self, calendar_id):
        """
        Deletes all events from the given calendar.
        """
        events = self.service.events().list(calendarId=calendar_id).execute()
        events_list = events.get('items', [])

        if not events_list:
            print("No events found.")
            return

        for event in events_list:
            try:
                print(f"Deleting event: {event['summary']} ({event['id']})")
                self.service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
            except Exception as e:
                print(f"An error occurred: {e}")

# Usage:
calendar_id = '0a07c917af84c81af957586ad561302d22fba2a1799b765310522145c43a62da@group.calendar.google.com'  # Replace with your actual calendar ID
cleaner = GoogleCalendarCleaner()
cleaner.delete_all_events(calendar_id)
