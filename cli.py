import sys
import time
import youtube_core  # local module
from utils import is_ffmpeg_installed, isValidYouTubeURL, isPlaylist, isVideo

if not is_ffmpeg_installed():
    print("FFmpeg is not installed! Please install FFmpeg to use this program.")
    sys.exit(1)


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

if isValidYouTubeURL(url):
    if isPlaylist(url):
        youtube_core.DownloadPlaylist(url)
    elif isVideo(url):
        youtube_core.DownloadTrack(url)
else:
    print(f"{bcolors.FAIL}Invalid URL. Please enter a valid YouTube URL.")
