from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import re

@dataclass(init=False)
class Event:
    summary: str
    tournament: str
    streams: list
    description: str

    timestamp: int
    start_time: str
    end_time: str
    uid: str

    def __init__(self,
        tournament: str,
        team1: str,
        team2: str,
        timestamp: int,
        streams: list=None
        ):

        self.tournament = tournament
        self.timestamp = timestamp
        if streams is None:
            self.streams = []
        else:            
            self.streams = streams

        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        self.start_time = (dt).isoformat()
        self.end_time = (dt + timedelta(hours=2)).isoformat()

        uid = f"{team1}{team2}{tournament}{timestamp}"
        self.uid = re.sub(r"\s+","",uid)

        self.summary = f"{team1} vs {team2}"
        self.description = f"tournament: {self.tournament}\nstreams: {self.streams}\nuid: {self.uid}"
        
def matches_to_event(matches):
    events = []
    for match in matches:
        events.append(Event(
            team1=match.team_left,
            team2=match.team_right,
            timestamp=match.data_timestamp,
            streams=match.streams,
            tournament=match.tournament
        ))
    return events



if __name__ == "__main__":
    # making a fake event for testing
    m = Event(
        tournament="The I",
        team1="Tickles",
        team2="Eagle",
        timestamp=(datetime.now().timestamp()),
        streams=["1","2"]
        )
    print(m)