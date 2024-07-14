import sys
import time
import youtube_core  # local module
from urllib.parse import urlparse, parse_qs
from utils import is_ffmpeg_installed


is_ffmpeg_installed()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


text = "YouTube To MP3 | Made by https://github.com/KyeOnDiscord"
print(f"{bcolors.BOLD + bcolors.OKCYAN}")


def text_animation(text, delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the animation is complete


text_animation(text, 0.015)

url = input(
    f"{bcolors.ENDC}Enter the URL of the video or playlist you want to download: \n>> ")

parsed_url = urlparse(url)

if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
    query_params = parse_qs(parsed_url.query)

    # Check if the 'list' parameter exists
    if 'list' in query_params:
        youtube_core.DownloadPlaylist(url)
    elif 'v' in query_params or parsed_url.netloc == "youtu.be":
        youtube_core.DownloadTrack(url)
else:
    print(f"{bcolors.FAIL}Invalid URL. Please enter a valid YouTube URL.")
