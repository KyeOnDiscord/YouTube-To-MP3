from utils import get_image_bytes
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, TRCK
from mutagen.mp3 import MP3


def ApplyID3Tags(filepath, yt, AlbumName=None, TrackNumber=None, TrackCount=None):
    audio = MP3(filepath, ID3=ID3)
    audio.tags.add(
        APIC(
            encoding=3,          # 3 is for utf-8
            mime='image/jpeg',   # image/jpeg or image/png
            type=3,              # 3 is for the cover(front) image
            desc='Cover',
            data=get_image_bytes(yt.thumbnail_url)  # Image data
        )
    )
    audio.tags.add(TPE1(encoding=3, text=yt.author.replace(
        " - Topic", "")))  # Artist
    if AlbumName:
        audio.tags.add(TALB(encoding=3, text=AlbumName))   # Album
    if TrackNumber:
        # Track Number
        audio.tags.add(TRCK(encoding=3, text=f'{TrackNumber}/{TrackCount}'))
    audio.tags.add(TIT2(encoding=3, text=yt.title))   # Title
    audio.tags.add(TYER(encoding=3, text=str(
        yt.publish_date.year)))        # Year

    # Save the changes
    audio.save(v2_version=3)
