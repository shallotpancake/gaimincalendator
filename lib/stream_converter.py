import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def find_embedded_stream(url):
    soup = get_soup(url)
    iframe = soup.find("iframe")
    return iframe["src"] if iframe and iframe.has_attr("src") else None

def convert_player_stream(stream_url):
    parsed_url = urlparse(stream_url)
    query_params = parse_qs(parsed_url.query)

    if "twitch.tv" in parsed_url.netloc and "channel" in query_params:
        # Convert Twitch embed to direct link
        channel = query_params["channel"][0]
        return f"https://twitch.tv/{channel}"
    
    elif "youtube.com" in parsed_url.netloc and "v" in query_params:
        # Convert YouTube embed to direct video URL
        video_id = query_params["v"][0]
        return f"https://youtube.com/watch?v={video_id}"
    
    elif "kick.com" in parsed_url.netloc:
        # Convert Kick embed to direct channel link
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) > 0:
            channel = path_parts[-1]
            return f"https://kick.com/{channel}"

    return stream_url  # Return original URL if no conversion is needed

def convert_stream(url):
    stream_url = find_embedded_stream(url)

    if stream_url:
        converted_url = convert_player_stream(stream_url)
        print("Final Stream URL:", converted_url)
        return converted_url
    else:
        print("No embedded stream found.")
        return url
    
