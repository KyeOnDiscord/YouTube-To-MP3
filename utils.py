import subprocess
import requests
from urllib.parse import urlparse, parse_qs


def get_image_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def is_ffmpeg_installed():
    try:
        # Try to run ffmpeg version command
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        # Check the return code (0 indicates success)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def isValidYouTubeURL(url):
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        return True
    return False


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


if is_ffmpeg_installed():
    print("FFmpeg is installed!")
else:
    print("FFmpeg is not installed.")
