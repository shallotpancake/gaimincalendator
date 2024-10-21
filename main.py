from scraper import Scrape
from google_sync import GoogleCalendarSync
from dotenv import load_dotenv
import os
import env_setup
from discord_sync import DiscordSync
import time
from event import matches_to_event
from pathlib import Path

root = os.getcwd()

paths = ['temp/',]

for path in paths:
    p = Path(root).joinpath(path)
    p.mkdir(exist_ok=True)

files = ['temp/event_id_cache.txt',]
for file in files:
    f = Path(root).joinpath(file)
    f.touch(exist_ok=True)


do_discordsync = True

env_setup.load_environment()
scraper = Scrape()

events = scraper.events
with open('matches.json', 'w') as f:
    f.write(str(events))

# Set up Google Calendar sync


load_dotenv() # load ID from .env
#GOOGLE_CALENDAR_ID = os.environ.get('CALENDAR_ID')
#google_sync = GoogleCalendarSync()

# Set up Discord Event sync
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

print("Syncing match entries to Google Calendar:")
for match in events:
    #google_sync.add_or_update_event(GOOGLE_CALENDAR_ID, match)
    ...
    
print("Google calendar sync complete.")

DiscordSync(events)
    
print("Discord events sync complete.")