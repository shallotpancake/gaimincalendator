from scraper import Scrape
from google_sync import GoogleCalendarSync
from dotenv import load_dotenv
import os
import env_setup
from discord_sync import DiscordEventSync
import time

env_setup.load_environment()
scraper = Scrape(os.environ.get('URL'))
match_entries = scraper.parse_match_entries()
print(f"scraper.py - Match entries found: {len(match_entries)}")
with open('matches.json', 'w') as f:
    f.write(str(match_entries))

# Set up Google Calendar sync
load_dotenv() # load ID from .env
GOOGLE_CALENDAR_ID = os.environ.get('CALENDAR_ID')
google_sync = GoogleCalendarSync()

# Set up Discord Event sync
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
discord_sync = DiscordEventSync(BOT_TOKEN, GUILD_ID, CHANNEL_ID)

print("Syncing match entries to Google Calendar:")
for index, match in enumerate(match_entries):
    if index > 5: # limit this to 5 events, too noisy
        break
    google_sync.add_or_update_event(GOOGLE_CALENDAR_ID, match)
    
print("Google calendar sync complete.")
    
print("Syncing match entries to Discord Guild Events:")
for index, match in enumerate(match_entries):
    if index > 5: # limit this to 5 events, discord API is annoying
        break
    discord_sync.add_or_update_event(match) #this is completely broken, maybe
    time.sleep(5) # discord keeps rate limiting me reeeeeeeee
    
print("Discord events sync complete.")