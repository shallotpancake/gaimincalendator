class Stream:
    def __init__(self, service, stream_id):
        self.service = service
        self.stream_id = stream_id
        self.link = self.construct_link()

    def construct_link(self):
        """
        Constructs a stream link based on the service (platform).
        """
        if self.service == 'youtube':
            return f"https://youtube.com/watch?v={self.stream_id}"
        elif self.service == 'twitch':
            return f"https://twitch.tv/{self.stream_id}"
        # Add more services as needed
        else:
            return f"Unknown service: {self.service}"

    def __repr__(self):
        return self.link

class Match:
    def __init__(self, team_left, team_right, tournament, streams, data_timestamp, data_tz):
        self.team_left = team_left
        self.team_right = team_right
        self.tournament = tournament
        self.streams = streams  
        self.data_timestamp = data_timestamp
        self.data_tz = data_tz

    def __repr__(self):
        return (f"Match(team_left='{self.team_left}', team_right='{self.team_right}', "
                f"tournament='{self.tournament}', streams={self.streams}, "
                f"data_timestamp='{self.data_timestamp}', data_tz='{self.data_tz}')")

if __name__ == "__main__":
    pass