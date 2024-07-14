import tkinter
from tkinter import ttk

import sv_ttk
from utils import get_image_bytes, is_ffmpeg_installed
from pytube import Playlist


class SimplePlaylist:
    def __init__(self, url):
        self.playlist = Playlist(url)
        self.title = self.playlist.title.replace("Album - ", "")
        try:
            self.owner = self.playlist.owner
        except IndexError:
            self.owner = self.playlist.videos[0].author

        self.thumbnail_url = self.playlist.videos[0].thumbnail_url
        self.thumbnailimg = get_image_bytes(self.thumbnail_url)


def download_mp3():
    url = url_entry.get()
    p = SimplePlaylist(url)
    # p = Playlist(url)
    album_name.config(text=p.title)
    album_image.config(data=p.thumbnailimg, format='png')


root = tkinter.Tk()
root.title("YouTube to MP3")

# Set the window size
root.geometry("800x500")

# Create a heading label
heading_label = ttk.Label(
    root, text="YouTube to MP3", font=("Helvetica", 16))
heading_label.pack(pady=10)

# Create a textbox for entering the YouTube URL
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=10)

# Create a download button
download_button = ttk.Button(root, text="Search", command=download_mp3)
download_button.pack(pady=10)

album_name = ttk.Label(root, text="Name", font=("Helvetica", 16))
album_name.pack(pady=10)

album_image = tkinter.PhotoImage()
label = ttk.Label(root, image=album_image)
label.pack()

sv_ttk.set_theme("dark")

# Run the application


if __name__ == "__main__":
    is_ffmpeg_installed()
    root.mainloop()
