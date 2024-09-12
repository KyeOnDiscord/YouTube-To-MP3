import os
from pytubefix import YouTube, Playlist
import ffmpeg
from mp3_metadata import ApplyID3Tags



# https://stackoverflow.com/a/64277310/12897035
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(percentage_of_completion)
    
def DownloadPlaylist(url):
    p = Playlist(url)
    playlistName = p.title.replace("Album - ", "")
    from cli import bcolors
    print(f"{bcolors.HEADER}Downloading Playlist: " + playlistName)

    for index, track in enumerate(p.videos):
        print(f"{track.title} [{index + 1}/{len(p.videos)}]")
        DownloadTrack(track.watch_url, track, playlistName,
                    index + 1, len(p.videos))


def DownloadTrack(url, yt_obj=None, AlbumName=None, TrackNumber=None, TrackCount=None) -> YouTube:
    yt = None
    if yt_obj:
        yt = yt_obj
    else:
        yt = YouTube(url)
    # extract only audio from the video
    video = yt.streams.get_audio_only()
    #yt.register_on_progress_callback(on_progress)

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
    return yt