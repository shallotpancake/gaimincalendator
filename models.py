class Stream:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Stream(title='{self.title}')"

class Match:
    def __init__(self, team_left, team_right, tournament, streams, data_timestamp, data_tz):
        self.team_left = team_left
        self.team_right = team_right
        self.tournament = tournament
        self.streams = streams  # Dictionary of categories to lists of Stream objects
        self.data_timestamp = data_timestamp
        self.data_tz = data_tz

    def __repr__(self):
        return (f"Match(team_left='{self.team_left}', team_right='{self.team_right}', "
                f"tournament='{self.tournament}', streams={self.streams}, "
                f"data_timestamp='{self.data_timestamp}', data_tz='{self.data_tz}')")
