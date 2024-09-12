import sys
from youtube_core import DownloadTrack
from utils import is_ffmpeg_installed

if not is_ffmpeg_installed():
    print("FFmpeg is not installed! Please install FFmpeg to use this program.")
    sys.exit(1)


text = "YouTube To MP3 | Made by https://github.com/KyeOnDiscord"
print(text)

url = "https://music.youtube.com/watch?v=r5MR7_INQwg&si=it43vlP9s19iy9HO"

DownloadTrack(url)