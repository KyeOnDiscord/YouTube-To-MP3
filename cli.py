"""The Command Line Interface (CLI) for Kye's YouTube to MP3"""

import sys
import time
from pytubefix import YouTube, Search
import youtube_core  # local module
from utils import *
class Bcolors:
    """Colors for printing"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def text_animation(text, delay):
    """Prints out text character by character"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the animation is complete


if __name__ == "__main__":
    if not is_ffmpeg_installed():
        print("FFmpeg is not installed! Please install FFmpeg to use this program.")
        sys.exit(1)
    TITLE = "YouTube To MP3 | Made by https://github.com/KyeOnDiscord"
    print(f"{Bcolors.BOLD + Bcolors.OKCYAN}")

    text_animation(TITLE, 0.015)
    while True:
        url = input(
            f"{Bcolors.ENDC}Enter the URL of the video or playlist you want to download: \n>> ")

        if isValidYouTubeURL(url):
            if isPlaylist(url):
                youtube_core.DownloadPlaylist(url)
            elif isVideo(url):
                downloaded = youtube_core.DownloadTrack(YouTube(url))
                print("Downloaded " + downloaded.title)
        elif isValidSpotifyURL(url):
            if isSpotifyTrack(url):
                import spotify
                spotify_track = spotify.getTrackDetails(url)
                results = Search(spotify_track['name'] + " " + spotify_track['artists'][0]['name'])
                if len(results.videos) == 0:
                    print(f"{Bcolors.FAIL}No results found for the Spotify track.")
                youtube_core.DownloadTrack(results.videos[0],AlbumCover=spotify_track['album']['images'][0]['url'])
        else:
            print(f"{Bcolors.FAIL}Invalid URL. Please enter a valid YouTube URL.")
