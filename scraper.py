from bs4 import BeautifulSoup
from collections import defaultdict
from models import Match, Stream
from datetime import datetime, timedelta, timezone
import interactive
import requests
from event import Event,matches_to_event

class Scrape:
    def __init__(self):
        # Fetch the data and parse it
        self.soup = self.fetch_data()
        self.matches = self.remove_tbd(self.parse_match_entries())
        self.events = matches_to_event(self.matches)


    def fetch_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
        url = r"https://liquipedia.net/dota2/api.php?action=parse&format=json&contentmodel=wikitext&maxage=600&smaxage=600&disablelimitreport=true&uselang=content&prop=text&text={{NewDota2_matches_upcoming|filterbuttons-liquipediatier=1|filterbuttons-liquipediatiertype=Monthly,Weekly,Qualifier,Misc,Showmatch,National}}"

        html = requests.get(url=url, headers=headers).json()["parse"]["text"]["*"]

        return BeautifulSoup(html, 'html.parser')

    def get_elements_by_class(self, class_name):
        """
        Find all elements with the specified class.
        """
        return self.soup.find_all(class_=class_name)

    def parse_match_entries(self):
        match_elements = self.get_elements_by_class('match')
        match_entries = []
        for match in match_elements:
            team_left = self.extract_team_name(match, 'team-left')
            team_right = self.extract_team_name(match, 'team-right')
            tournament = self.extract_tournament(match)
            streams = self.extract_streams(match)  # Streams now contains Stream objects
            data_timestamp = self.extract_timezone_aware_datetime(match)
            
            match_entry = Match(team_left, team_right, tournament, streams, data_timestamp)
            match_entries.append(match_entry)
        
        return match_entries
    
    def remove_tbd(self, matches):
        unique_matches = []
        for match in matches:
            if "TBD" in match.team_left or "TBD" in match.team_right:
                ...
            else:
                unique_matches.append(match)

        return unique_matches

    def extract_team_name(self, match, side):
        team_side = match.find(class_=side)
        if team_side:
            team_name = team_side.find(class_='team-template-text')
            if team_name:
                return team_name.get_text(strip=True)
        return 'TBD'

    def extract_tournament(self, match):
        match_tournament = match.find(class_='match-tournament')
        if match_tournament:
            tournament_text = match_tournament.find(class_='tournament-text')
            if tournament_text:
                return tournament_text.get_text(strip=True)
        return None

    def extract_streams(self, match):
        """
        Extracts all stream information for the match and returns them categorized by service.
        Each stream contains a dynamically constructed link.
        """
        match_streams = match.find(class_='match-streams')
        categorized_streams = defaultdict(list)
        
        if match_streams:
            streams = match_streams.find_all('a', href=True)
            for stream in streams:
                href = stream.get('href', '')
                stream_obj = self.extract_category_and_title_from_href(href)
                if stream_obj:
                    categorized_streams[stream_obj.service].append(stream_obj)  # Store the Stream object
        
        return dict(categorized_streams)

    def extract_timezone_aware_datetime(self, match):
        """
        Convert data-timestamp and data-tz into a timezone-aware datetime object.
        Handles timezones in +HH:mm or -HH:mm format, and ensures proper parsing.
        """

        return int(match.find(class_='timer-object').attrs["data-timestamp"])

    def extract_category_and_title_from_href(self, href):
        """
        Extracts the service (platform) and the stream ID from the href.
        Constructs a Stream object with the link.
        """
        parts = href.split('/')
        if len(parts) >= 4 and parts[2] == 'Special:Stream':
            service = parts[3]  # The service category (e.g., 'youtube', 'twitch')
            stream_id = parts[-1]  # The last part is the unique identifier for the stream
            return Stream(service, stream_id)  # Return a Stream object with the link
        return None  # Return None if the format is not valid

if __name__ == "__main__":
    s = Scrape()
    print(*s.events, sep='\n')