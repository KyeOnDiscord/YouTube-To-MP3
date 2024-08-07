# Description: This file contains functions to apply ID3 tags to the mp3 file.
import urllib.parse
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, TRCK,SYLT, Encoding,USLT, COMM
from mutagen._constants import GENRES
from utils import get_image_bytes


def format_custom_time(seconds):
    minutes = int(seconds // 60)
    seconds_remainder = seconds % 60
    seconds_full = int(seconds_remainder)
    hundredths = int((seconds_remainder - seconds_full) * 100)
    
    return f"[{minutes:02d}:{seconds_full:02d}.{hundredths:02d}]"

def DownloadSongLyrics(yt):
    url = "http://api.textyl.co/api/lyrics?q=" + urllib.parse.quote_plus(yt.title + " " + yt.author.replace(' - Topic', ''))
    response = requests.request("GET", url,verify=False)
    if response.status_code != 200:
        return None
    return response.json()

def GetSyncedSongLyrics(lyrics): return [(entry['lyrics'],entry['seconds'] * 1000) for entry in lyrics]

def GetSyncedSongLyricsCOMM(lyrics): return "\n".join((format_custom_time(entry['seconds']) + entry['lyrics']) for entry in lyrics)

def GetSongLyrics(lyrics): return "\n".join([entry["lyrics"] for entry in lyrics])

def ApplyID3Tags(filepath, yt, AlbumName=None, TrackNumber=None, TrackCount=None):
    tags = ID3(filepath)
    lyrics = DownloadSongLyrics(yt)
    if lyrics:
        tags.setall("SYLT", [SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=GetSyncedSongLyrics(lyrics))])
        tags.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=GetSongLyrics(lyrics)))
        commslyrics = GetSyncedSongLyricsCOMM(lyrics)
        tags.add(COMM(encoding=3, lang=u'eng', desc=u'desc', text=commslyrics))
    # genre finder
    for genre in GENRES:
        for keyword in yt.keywords:
            if keyword.lower() in genre.lower():
                tags.add(TCON(encoding=3, genre=genre))
                #print("Genre is: " + genre + " , (tag was " + tag + ")")
                break

    tags.add(APIC(
            encoding=3,          # 3 is for utf-8
            mime='image/jpeg',   # image/jpeg or image/png
            type=3,              # 3 is for the cover(front) image
            desc='Cover',
            data=get_image_bytes(yt.thumbnail_url)  # Image data
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
