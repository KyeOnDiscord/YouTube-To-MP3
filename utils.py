import subprocess
import requests
from urllib.parse import urlparse, parse_qs


def get_image_bytes(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.content


def is_ffmpeg_installed():
    try:
        # Run the ffmpeg command to check if it is installed
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        print("ffmpeg is installed, but returned an error")
    except FileNotFoundError:
        print("ffmpeg is not installed")
    return False


def isValidYouTubeURL(url):
    parsed_url = urlparse(url)
    return "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc
def isValidSpotifyURL(url):
    parsed_url = urlparse(url)
    return "spotify.com" in parsed_url.netloc or "open.spotify.com" in parsed_url.netloc
def isSpotifyTrack(url):
    parsed_url = urlparse(url)
    return "track" in parsed_url.path


def isPlaylist(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Check if the 'list' parameter exists
    return 'list' in query_params


def isVideo(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Check if the 'v' parameter exists
    return 'v' in query_params or parsed_url.netloc == "youtu.be"