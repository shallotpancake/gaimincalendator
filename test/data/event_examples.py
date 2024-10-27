from obj.event import Event

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

events = [example_event, example_event2]

