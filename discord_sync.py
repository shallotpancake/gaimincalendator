import requests
import json
from event import Event
from dotenv import load_dotenv
import os
import cache_discord
from time import sleep

def post_event(match, uid):
    """
    Posts event to Discord
    """
    load_dotenv()
    DISCORD_API_URL = "https://discord.com/api/v10"
    BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    GUILD_ID = os.environ.get('GUILD_ID')
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
        
    event = event_to_guild_event(match)
    # Create a new event
    print(f"Creating new event: {match}")
    response = requests.post(
        f"{DISCORD_API_URL}/guilds/{GUILD_ID}/scheduled-events",
        headers=headers,
        data=json.dumps(event)
    )
    try:
        print(response.text)
        response.raise_for_status()
    except:
        pass
    with open("temp/event_id_cache.txt", "a") as f:
        f.write(f"{uid}\n")
    return response.status_code

def compare_event_discord_event(event: Event, discord_event: dict)-> bool:
    return event.uid in discord_event["description"]



def event_to_guild_event(event: Event):
    # convert Event to discord_
    event_data = {
        "name": event.summary,
        "description": event.description,
        "scheduled_start_time": event.start_time,
        "scheduled_end_time": event.end_time,
        "privacy_level": 2,  # GUILD_ONLY
        "entity_type": 3,  # External event
        "entity_metadata": {
            "location": "Online"
        }
    }
    return event_data
    
def get_discord_events():
    """
    Get events from Discord
    """
    load_dotenv()
    BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    DISCORD_API_URL = "https://discord.com/api/v10"
    GUILD_ID = os.environ.get('GUILD_ID')

    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    # Get all existing events
    response = requests.get(
        f"{DISCORD_API_URL}/guilds/{GUILD_ID}/scheduled-events",
        headers=headers
    )
    try:
        response.raise_for_status()
    except:
        print(response.text)
        return None


    discord_events = response.json()

    return discord_events

def remove_duplicates(incoming_events: list[Event]) -> list:
    unique_events = []

    with open("temp/event_id_cache.txt", "r") as f:
        existing_events = f.read()

    print(f"Starting event count: {len(incoming_events)}")
    for event in incoming_events:
        if event.uid in existing_events:
            print(f"Event duplicate: {event.uid}")
            print(existing_events)
            continue
        else:
            unique_events.append(event)
    
    print(f"Ending event count: {len(unique_events)}")
    return unique_events

def clear_events():
    load_dotenv()
    BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    DISCORD_API_URL = "https://discord.com/api/v10"
    GUILD_ID = os.environ.get('GUILD_ID')

    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    events = get_discord_events()
    for event in events:
        requests.delete(
        f"{DISCORD_API_URL}/guilds/{GUILD_ID}/scheduled-events/{event["id"]}",
        headers=headers
        )
        sleep(1)

    sleep(10)
    events = get_discord_events()

    if events:
        for event in events:
            requests.delete(
            f"{DISCORD_API_URL}/guilds/{GUILD_ID}/scheduled-events/{event["id"]}",
            headers=headers
            )
            sleep(1)

def DiscordSync(incoming_events: list):
    new_events = remove_duplicates(incoming_events=incoming_events)

    i = 0
    for event in new_events:
        if i > 0:
            break   
        post_event(event, event.uid)
        i+=1
        sleep(10)

    