import requests
import json
from datetime import timedelta
import string
import random

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

        if response.status_code != 200:
            print(f"Failed to fetch events: {response.status_code}, {response.text}")
            return None

        events = response.json()
        for event in events:
            if unique_id in event['description']:
                return event

        return None

    def add_or_update_event(self, match):
        """
        Adds a new event or updates an existing one if found using a unique identifier.
        """
        unique_id = self.create_unique_id()
        existing_event = self.search_event_by_unique_id(unique_id)

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

        if existing_event:
            # Update the existing event
            event_id = existing_event['id']
            print(f"Updating existing event: {event_data['name']}")
            response = requests.patch(
                f"{DISCORD_API_URL}/guilds/{self.guild_id}/scheduled-events/{event_id}",
                headers=self.headers,
                data=json.dumps(event_data)
            )
        else:
            # Create a new event
            print(f"Creating new event: {event_data['name']}")
            response = requests.post(
                f"{DISCORD_API_URL}/guilds/{self.guild_id}/scheduled-events",
                headers=self.headers,
                data=json.dumps(event_data)
            )

        if response.status_code in [200, 201]:
            print(f"Event created/updated successfully: {event_data['name']}")
        else:
            print(f"Failed to create/update event: {response.status_code}, {response.text}")

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
