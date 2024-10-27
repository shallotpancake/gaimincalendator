class Match:
    def __init__(self, team_left, team_right, tournament, streams, data_timestamp):
        self.team_left = team_left
        self.team_right = team_right
        self.tournament = tournament
        self.streams = streams  
        self.data_timestamp = data_timestamp
    def __repr__(self):
        return (f"Match(team_left='{self.team_left}', team_right='{self.team_right}', "
                f"tournament='{self.tournament}', streams={self.streams}, "
                f"data_timestamp='{self.data_timestamp}'")

if __name__ == "__main__":
    pass