import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from models import Match, Stream
from datetime import datetime, timedelta, timezone
import interactive
import os

class Scrape:
    def __init__(self, url):
        # Fetch the data and parse it
        self.soup = self.fetch_data(url)

    def fetch_data(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        # deprecated? 
        #response = requests.get(url, headers=headers)
        #response.raise_for_status()
        
        html = interactive.get_tier_1_source(url)
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
            data_timestamp, data_tz = self.extract_timezone_aware_datetime(match)
            
            match_entry = Match(team_left, team_right, tournament, streams, data_timestamp, data_tz)
            match_entries.append(match_entry)
        
        return match_entries

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
        Handles timezones in +HH:mm or -HH:mm format.
        """
        timer_object = match.find(class_='timer-object')
        if timer_object:
            # Extract the timestamp and timezone offset
            timestamp = int(timer_object.get('data-timestamp', 0))
            tz_string = timer_object.find('abbr').get('data-tz', 'UTC')
            
            # Handle timezone in the format +HH:mm or -HH:mm
            if tz_string.startswith(('+', '-')):
                sign = 1 if tz_string.startswith('+') else -1
                hours_offset = int(tz_string[1:3])
                minutes_offset = int(tz_string[4:6])
                offset = timedelta(hours=sign * hours_offset, minutes=sign * minutes_offset)
                tz = timezone(offset)
            else:
                tz = timezone.utc  # Default to UTC if no valid tz is found
            
            # Convert the Unix timestamp to a timezone-aware datetime object
            dt = datetime.fromtimestamp(timestamp, tz)
            
            return dt, tz
        return None, None
    
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
