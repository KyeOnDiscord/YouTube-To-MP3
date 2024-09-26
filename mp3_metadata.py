""" This file contains functions to apply ID3 tags to the mp3 file."""
from io import BytesIO
import urllib.parse
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, TRCK,SYLT, Encoding,USLT, COMM
from mutagen._constants import GENRES
from pytubefix import YouTube
from PIL import Image
from utils import get_image_bytes

def get_album_cover(yt: YouTube) -> bytes:
    """Gets an album cover in bytes from a YouTube object"""
    # Open the image
    url = f"https://i.ytimg.com/vi/{yt.video_id}/maxresdefault.jpg"
    req = requests.get(url, timeout=5)
    if req.status_code == 404:
        return get_image_bytes(yt.thumbnail_url)
    image = Image.open(BytesIO(req.content))

    # Get the original dimensions
    width, height = image.size
    if image.size != (1280,720):
        return req.content

    # Define the crop box (left, upper, right, lower)
    left = 280
    top = 0
    right = width - 280
    bottom = height

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))
    image_bytes = BytesIO()
    cropped_image.save(image_bytes, format='JPEG')
    return image_bytes.getvalue()

def format_custom_time(seconds):
    """Generates a time string for Flacbox [0:0:0]"""
    minutes = int(seconds // 60)
    seconds_remainder = seconds % 60
    seconds_full = int(seconds_remainder)
    hundredths = int((seconds_remainder - seconds_full) * 100)
    return f"[{minutes:02d}:{seconds_full:02d}.{hundredths:02d}]"

def DownloadSongLyrics(yt: YouTube):
    """Downloads Song Lyrics from textyl api"""
    url = "http://api.textyl.co/api/lyrics?q=" + urllib.parse.quote_plus(yt.title + " " + yt.author.replace(' - Topic', ''))
    response = requests.request("GET", url,verify=False, timeout=5)
    if response.status_code != 200:
        return None
    return response.json()

def GetSyncedSongLyrics(lyrics): return [(entry['lyrics'],entry['seconds'] * 1000) for entry in lyrics]

def GetSyncedSongLyricsCOMM(lyrics): return "\n".join((format_custom_time(entry['seconds']) + entry['lyrics']) for entry in lyrics)

def GetSongLyrics(lyrics): return "\n".join([entry["lyrics"] for entry in lyrics])

def ApplyID3Tags(filepath, yt: YouTube, AlbumName=None, TrackNumber=None, TrackCount=None, AlbumCover=None):
    tags = ID3(filepath)
    #lyrics = DownloadSongLyrics(yt)
    lyrics = None
    if lyrics:
        tags.setall("SYLT", [SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=GetSyncedSongLyrics(lyrics))])
        tags.add(USLT(encoding=3, lang='eng', desc='desc', text=GetSongLyrics(lyrics)))
        commslyrics = GetSyncedSongLyricsCOMM(lyrics)
        tags.add(COMM(encoding=3, lang='eng', desc='desc', text=commslyrics))
    # genre finder
    for genre in GENRES:
        for keyword in yt.keywords:
            if keyword.lower() in genre.lower():
                tags.add(TCON(encoding=3, genre=genre))
                #print("Genre is: " + genre + " , (tag was " + tag + ")")
                break
    if AlbumCover is None:
        AlbumCover = get_album_cover(yt)
    else :
        AlbumCover = get_image_bytes(AlbumCover)
    tags.add(APIC(
            encoding=3,          # 3 is for utf-8
            mime='image/jpeg',   # image/jpeg or image/png
            type=3,              # 3 is for the cover(front) image
            desc='Cover',
            data=AlbumCover  # Image data
        ))
    tags.add(TPE1(encoding=3, text=yt.author.replace(
        " - Topic", "")))  # Artist
    if AlbumName:
        tags.add(TALB(encoding=3, text=AlbumName))   # Album
    if TrackNumber:
        # Track Number
        tags.add(TRCK(encoding=3, text=f'{TrackNumber}/{TrackCount}'))
    tags.add(TIT2(encoding=3, text=yt.title))   # Title
    tags.add(TYER(encoding=3, text=str(
        yt.publish_date.year)))        # Year

    # Save the changes
    tags.save(v2_version=3)
