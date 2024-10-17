import unittest
from event import Event
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import discord_sync

load_dotenv()
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
# need to increment now or discord won't create an event
# this will mean the time should be one hour ahead!
dt = datetime.now() + timedelta(hours=1)
example_event = Event(
        tournament="The [B]international",
        team1="Test",
        team2="Event",
        timestamp=(1729109799),
        streams=["1","2"]
        )

example_event2 = Event(
        tournament="The [B]international",
        team1="Test",
        team2="Event",
        timestamp=(1729109748),
        streams=["1","2"]
        )
description = "tournament: The [B]international\
streams: ['1', '2']\
uid:TestEventThe[B]international1729109799"

description2 = "tournament: The [B]international\
streams: ['1', '2']\
uid:TestEventThe[B]international1729109748"

events = [example_event, example_event2]
discord_events = [{"description": description},{"description": description2} ]


class TestDiscordEvents(unittest.TestCase):
    def test_event_obj(self):
        self.assertTrue(example_event)

    def test_event_post(self):
        # was the event posted successfully?
        res = discord_sync.post_event(example_event)
        self.assertEqual(res,200)

    def test_get_discord_events(self):
        res = discord_sync.get_discord_events()
        self.assertIsNotNone(res)

    def test_compare_event_discord_event(self):
        res = discord_sync.compare_event_discord_event(example_event, {"description":description})
        self.assertTrue(res)

    def test_compare_event_discord_event_false(self):
        res = discord_sync.compare_event_discord_event(example_event, {"description": f"asdf"})
        self.assertFalse(res)

    def test_remove_duplicates(self):
        res = discord_sync.remove_duplicates(events, discord_events)
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()  # This will run all the test cases when executed