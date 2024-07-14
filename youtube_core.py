import os
from pytube import YouTube, Playlist
import ffmpeg
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, TRCK
from mutagen.mp3 import MP3
from utils import get_image_bytes


def DownloadPlaylist(url):
    p = Playlist(
        url)
    playlistName = p.title.replace(
        "Album - ", "")
    print("Downloading Playlist: " + playlistName)

    for index, track in enumerate(p.videos):
        DownloadTrack(track.watch_url, track, playlistName,
                      index + 1, len(p.videos))
        print(f"Downloaded {index + 1}/{len(p.videos)}")


def DownloadTrack(url, yt_obj=None, AlbumName=None, TrackNumber=None, TrackCount=None):
    yt = None
    if yt_obj:
        yt = yt_obj
    else:
        yt = YouTube(url)
    # extract only audio from the video
    video = yt.streams.filter(
        only_audio=True, mime_type="audio/mp4").first()

    output_path = "Downloads"
    if AlbumName:
        output_path = os.path.join(output_path, AlbumName)
    out_file = video.download(output_path=output_path)

    base = os.path.splitext(out_file)[0]
    new_file = f"{base}.mp3"
    # convert to mp3  (out file is .mp4 extension)
    ffmpeg.input(out_file).output(
        new_file, acodec='libmp3lame', compression_level=6, audio_bitrate="160k").run(overwrite_output=True)
    # delete out_file
    os.remove(out_file)

    # edit tags

    audio = MP3(new_file, ID3=ID3)
    audio.tags.add(
        APIC(
            encoding=3,          # 3 is for utf-8
            mime='image/jpeg',   # image/jpeg or image/png
            type=3,              # 3 is for the cover(front) image
            desc='Cover',
            data=get_image_bytes(yt.thumbnail_url)  # Image data
        )
    )
    audio.tags.add(TPE1(encoding=3, text=yt.author))  # Artist
    if AlbumName:
        audio.tags.add(TALB(encoding=3, text=AlbumName))   # Album
    if TrackNumber:
        # Track Number
        audio.tags.add(TRCK(encoding=3, text=f'{TrackNumber}/{TrackCount}'))
    audio.tags.add(TIT2(encoding=3, text=video.title))   # Title
    audio.tags.add(TYER(encoding=3, text=str(
        yt.publish_date.year)))        # Year

    # Save the changes
    audio.save(v2_version=3)

    # result of success
    print(yt.title + " has been successfully downloaded.")
