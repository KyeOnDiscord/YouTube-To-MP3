import os
from pytubefix import YouTube, Playlist
import ffmpeg
from mp3_metadata import ApplyID3Tags


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
    print("Downloading: " + yt.title)
    # extract only audio from the video
    video = yt.streams.get_audio_only()

    output_path = "Downloads"
    if AlbumName:
        output_path = os.path.join(output_path, AlbumName)
    out_file = video.download(output_path=output_path)

    base = os.path.splitext(out_file)[0]
    new_file = f"{base}.mp3"
    # convert to mp3  (out file is .mp4 extension)
    ffmpeg.input(out_file).output(
        new_file, acodec='libmp3lame', compression_level=6, audio_bitrate="160k", loglevel="quiet").run(overwrite_output=True)
    # delete out_file
    os.remove(out_file)

    # edit tags
    ApplyID3Tags(new_file, yt, AlbumName, TrackNumber, TrackCount)

    # result of success
    print(yt.title + " has been successfully downloaded.")
