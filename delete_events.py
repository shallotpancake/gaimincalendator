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
        Deletes all events from the given calendar, handling pagination.
        """
        page_token = None
        while True:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                pageToken=page_token,  # Handle pagination
                showDeleted=False,     # Only get non-deleted events
                singleEvents=True      # Get individual events
            ).execute()
            
            events_list = events_result.get('items', [])
            if not events_list:
                print("No more events found.")
                break

            for event in events_list:
                try:
                    print(f"Deleting event: {event.get('summary', 'No title')} ({event['id']})")
                    self.service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
                except Exception as e:
                    print(f"An error occurred while deleting event {event.get('summary', 'No title')}: {e}")

            # Check if there's another page of events
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    calendar_id = os.environ.get('CALENDAR_ID')
    cleaner = GoogleCalendarCleaner()
    cleaner.delete_all_events(calendar_id)
