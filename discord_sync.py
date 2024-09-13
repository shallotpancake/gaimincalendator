import requests
import json
from datetime import datetime, timedelta
import string
import random
from collections import defaultdict

DISCORD_API_URL = "https://discord.com/api/v10"

class DiscordEventSync:
    def __init__(self, bot_token, guild_id, channel_id):
        self.bot_token = bot_token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }

    def create_unique_id(self):
        """
        Creates a unique identifier for a match
        """
        # Define the characters to choose from (letters and digits)
        characters = string.ascii_letters + string.digits
        # Use random.choices to generate a list of random characters, then join them into a string
        random_string = ''.join(random.choices(characters, k=50))
        return random_string

    def search_event_by_unique_id(self, unique_id):
        """
        Searches for an event with a given unique identifier in extended properties.
        """
        response = requests.get(
            f"{DISCORD_API_URL}/guilds/{self.guild_id}/scheduled-events",
            headers=self.headers
        )

        response.raise_for_status()

        events = response.json()
        for event in events:
            if unique_id in event['description']:
                return event

        return None
    
    def match_to_event(self, match):
        unique_id = self.create_unique_id()
        event_data = {
            "name": f"{match.team_left} vs {match.team_right}",
            "description": f"Tournament: {match.tournament}\nStreams: {', '.join([str(stream) for stream in match.streams.values()])}\n{unique_id}",
            "scheduled_start_time": match.data_timestamp.isoformat(),
            "scheduled_end_time": (match.data_timestamp + timedelta(hours=2)).isoformat(),
            "privacy_level": 2,  # GUILD_ONLY
            "entity_type": 3,  # External event
            "entity_metadata": {
                "location": "Online"
            }
        }
        return event_data

    def add_or_update_event(self, match):
        """
        Adds a new event or updates an existing one if found using a unique identifier.
        """
        print("add_or_update_event")
        #existing_event = self.search_event_by_unique_id(unique_id) the discord API is too sensitive for this type of check. maybe I just delete all events and write new on run
        #existing_event = None 
        event = self.match_to_event(match)
        # Create a new event
        print(f"Creating new event: {event['name']}")
        response = requests.post(
            f"{DISCORD_API_URL}/guilds/{self.guild_id}/scheduled-events",
            headers=self.headers,
            data=json.dumps(event)
        )
        try:
            print(response.text)
            response.raise_for_status()
        except:
            pass


    def delete_event_by_unique_id(self, unique_id):
        """
        Deletes an event with the specified unique ID.
        """
        existing_event = self.search_event_by_unique_id(unique_id)
        if existing_event:
            event_id = existing_event['id']
            response = requests.delete(
                f"{DISCORD_API_URL}/guilds/{self.guild_id}/scheduled-events/{event_id}",
                headers=self.headers
            )

            if response.status_code == 204:
                print(f"Deleted event: {existing_event['name']}")
            else:
                print(f"Failed to delete event: {response.status_code}, {response.text}")
        else:
            print(f"No event found with ID: {unique_id}")
            
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from datetime import datetime, timedelta, timezone
    from models import Match, Stream
    load_dotenv()
    streams = defaultdict(list)
    streams['twitch'].append(Stream('twitch', 'The_International'))
    match = Match("Test", "Test", "TI", streams, (datetime.now(timezone.utc) + timedelta(hours=1)), "UTC-05: 00")
    
    BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    GUILD_ID = os.environ.get('GUILD_ID')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    
    discord_sync = DiscordEventSync(BOT_TOKEN, GUILD_ID, CHANNEL_ID)
    discord_sync.add_or_update_event(match)

