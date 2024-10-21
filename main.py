from scraper import Scrape
from dotenv import load_dotenv
import os
import lib.env_setup as env_setup
from discord.discord_sync import DiscordSync

from pathlib import Path

root = os.getcwd()

paths = ['temp/',]

for path in paths:
    p = Path(root).joinpath(path)
    p.mkdir(exist_ok=True)

files = ['temp/discord_event_id_cache.txt',
         'temp/latest_matches.json',]

for file in files:
    f = Path(root).joinpath(file)
    f.touch(exist_ok=True)


env_setup.load_environment()
scraper = Scrape()

events = scraper.events
with open('latest_matches.json', 'w') as f:
    f.write(str(events))


# Set up Discord Event sync
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

DiscordSync(events)
    
print("Discord events sync complete.")