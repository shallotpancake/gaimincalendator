from ics import Calendar, Event
from datetime import datetime, timedelta

class MatchCalendar:
    def __init__(self):
        self.calendar = Calendar()

    def add_match(self, match):
        event = Event()
        event.name = f"{match.team_left} vs {match.team_right}"
        event.begin = match.data_timestamp  # Assuming this is a datetime object
        event.description = f"Tournament: {match.tournament}\nStreams: {', '.join([str(stream) for stream in match.streams.values()])}"
        self.calendar.events.add(event)

    def export_ics(self):
        return self.calendar.serialize()
