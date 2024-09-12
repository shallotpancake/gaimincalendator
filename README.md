# GaiminCalendator

## Overview

**GaiminCalendator** is a Python-based application that grabs Dota 2 match schedules from liquipedia and adds them to a calendar.

[See the calendar here](https://calendar.google.com/calendar/u/0?cid=MGEwN2M5MTdhZjg0YzgxYWY5NTc1ODZhZDU2MTMwMmQyMmZiYTJhMTc5OWI3NjUzMTA1MjIxNDVjNDNhNjJkYUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t)
## Features

- Web Scraping: Scrapes match data such as teams, tournament names, and stream information from a given URL.
- Timezone-Aware Events: Handles match times with proper timezone offsets to ensure accurate scheduling.
- Google Calendar Integration: Automatically creates and syncs events to a Google Calendar.
- Event Management: Ability to delete all events from a Google Calendar for clean-up.
- ICS Export: Generates an `.ics` file for exporting the match calendar.

## Requirements

- Python 3.7+
- Google Calendar API credentials
- Access to the website being scraped (such as Liquipedia)
- `credentials.json` for Google API authentication (follow instructions below to set this up)

## Installation

### Step 1: Clone the Repository

```
git clone https://github.com/your-repo/gaimincalendator.git  
cd gaimincalendator
```

### Step 2: Install Required Python Packages

Install the required dependencies using `pip`:
```
pip install -r requirements.txt
```
### Step 3: Google Calendar API Setup

1. Enable the Google Calendar API:  
   Go to the Google Cloud Console, create a project, and enable the Google Calendar API.

2. Create Credentials:  
   Create OAuth 2.0 credentials for a desktop application.  
   Download the `credentials.json` file and place it in the root directory of the project.

3. Authentication:  
   The first time you run the program, it will prompt you to log in via a web browser.  
   A `token.pickle` file will be generated and stored for future use, so you won't need to log in again unless the token expires.

## Usage

### Step 1: Scraping and Syncing Matches

You can run the main script to scrape matches and sync them to your Google Calendar:

```
python main.py
```
Make sure to update the `main.py` file with your Google Calendar ID:
```
GOOGLE_CALENDAR_ID = 'your_calendar_id_here'  # Replace with your actual calendar ID
```
### Step 2: Deleting All Events from the Calendar

If you want to clear the calendar of all events (e.g., after testing), you can run the following command:
```
python delete_events.py
```
This script will delete all events on the specified calendar.

### Step 3: Exporting Calendar as ICS

To export the scraped matches to an `.ics` file, the program automatically generates a file called `matches_calendar.ics`:

# Generated in the main.py script  
with open("matches_calendar.ics", "w") as f:  
    f.write(calendar.export_ics())

### Step 4: Schedule Regular Syncing

You can automate syncing the calendar at regular intervals using:
- Cron (Linux/macOS): To run the script every hour:
```
0 * * * * /usr/bin/python3 /path/to/gaimincalendator/main.py
```
- Task Scheduler (Windows): Create a task that runs the `main.py` file at your desired intervals.

## Project Structure

```
project/  
├── cache.py              # Handles caching for web scraping  
├── calendar_manager.py   # Manages calendar creation and ICS export  
├── delete_events.py      # Script to delete all events from Google Calendar  
├── google_sync.py        # Handles syncing events with Google Calendar  
├── main.py               # Main script to scrape, manage, and sync calendar events  
├── models.py             # Defines the Match and Stream classes  
├── scraper.py            # Web scraping logic  
├── utils.py              # Utility functions like extracting stream information  
├── requirements.txt      # Python dependencies  
├── credentials.json      # Google API credentials
└── README.md             # This file
```





## Development

If you want to contribute or modify the project:

1. Fork this repository.  
2. Create a new feature branch: `git checkout -b feature/new-feature`.  
3. Commit your changes: `git commit -m 'Add some feature'`.  
4. Push to the branch: `git push origin feature/new-feature`.  
5. Create a pull request.

## Contributing

Feel free to contribute by submitting a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
