from scraper import Scrape
from google_sync import GoogleCalendarSync
from dotenv import load_dotenv
import os
import env_setup

env_setup.load_environment()
scraper = Scrape(os.environ.get('URL'))
match_entries = scraper.parse_match_entries()

# Set up Google Calendar sync
load_dotenv() # load ID from .env
GOOGLE_CALENDAR_ID = os.environ.get('CALENDAR_ID')
google_sync = GoogleCalendarSync()

print("Syncing match entries to Google Calendar:")
for entry in match_entries:
    google_sync.add_or_update_event(GOOGLE_CALENDAR_ID, entry)