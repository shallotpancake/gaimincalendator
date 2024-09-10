from scraper import Scrape
from calendar_manager import MatchCalendar
from google_sync import GoogleCalendarSync

# Configuration for Google Calendar
GOOGLE_CALENDAR_ID = 'YOUR_CALENDAR_ID_HERE'  # Replace with actual calendar ID

def sync_calendar_with_google():
    # Scrape the matches
    url = "https://liquipedia.net/dota2/Liquipedia:Matches"
    scraper = Scrape(url)
    match_entries = scraper.parse_match_entries()

    # Set up the calendar manager and Google Calendar sync
    calendar = MatchCalendar()
    google_sync = GoogleCalendarSync()

    # Add events to the local calendar and sync to Google Calendar
    for entry in match_entries:
        calendar.add_match(entry)  # Add to local calendar
        google_sync.add_event(GOOGLE_CALENDAR_ID, entry)  # Sync to Google Calendar

    # Export the local calendar to an ICS file
    with open("matches_calendar.ics", "w") as f:
        f.write(calendar.export_ics())

    print("Calendar successfully synced with Google Calendar.")

if __name__ == "__main__":
    sync_calendar_with_google()
