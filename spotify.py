"""This module allows Spotify urls to be used and the equivalent song is searched on YouTube from details of the spotify track"""
import re
import requests

bearer = None
def getSpotifyBearer():
    url = "https://accounts.spotify.com/api/token"
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ZTdmNjNjYjg5M2QwNDA5MzljOTFlOWE1ZjBiMTRkNTQ6ZDQ2MjBhMjEwNzdkNDU1ZTllMWY1MTkzNzBhOGQxYTY=',
    }

    response = requests.request("POST", url, headers=headers, data='grant_type=client_credentials', timeout=5)
    if (response.status_code == 200):
        return response.json()['access_token']
    else :
        raise ValueError("Failed to get Spotify Bearer token")


def getTrackDetails(trackURL):
    pattern = r"https:\/\/open\.spotify\.com\/track\/([a-zA-Z0-9]+)"
    track_id = None
    match = re.search(pattern, trackURL)
    if match:
        track_id = match.group(1)
    else:
        print("Spotify Track ID not found in URL")
        return None

    global bearer
    if bearer is None:
        bearer = getSpotifyBearer()
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
    'Authorization': 'Bearer ' + bearer
    }
    response = requests.request("GET", url, headers=headers, timeout=5)
    if (response.status_code == 200):
        return response.json()
    else :
        raise ValueError("Failed to get track details")