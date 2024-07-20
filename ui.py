import tkinter
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io

import sv_ttk
from utils import get_image_bytes, is_ffmpeg_installed, isValidYouTubeURL, isPlaylist, isVideo
from pytubefix import Playlist, YouTube


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


class SimpleVideo:
    def __init__(self, url):
        self.video = YouTube(url)
        self.title = self.video.title
        self.owner = self.video.author

        self.thumbnail_url = self.video.thumbnail_url
        self.thumbnailimg = get_image_bytes(self.thumbnail_url)


def search_url():
    url = url_entry.get()
    if isValidYouTubeURL(url):
        if isPlaylist(url):
            playlist = SimplePlaylist(url)
            image = Image.open(io.BytesIO(playlist.thumbnailimg))
            tk_image = ImageTk.PhotoImage(image)
            image = ImageTk.PhotoImage(file=tk_image)
            imagebox.config(image=image)
            imagebox.image = image
           # album_image.config(image=playlist.thumbnailimg)

        elif isVideo(url):
            video = SimpleVideo(url)
            image = Image.open(io.BytesIO(video.thumbnailimg))
            tk_image = ImageTk.PhotoImage(image)
            image = ImageTk.PhotoImage(file=tk_image)
            imagebox.config(image=image)
            imagebox.image = image
    else:
        # messagebox tkinter
        messagebox.showerror(
            "Error", "Invalid URL. Please enter a valid YouTube URL.")


if not is_ffmpeg_installed():
        messagebox.showerror("Error", "FFmpeg is not installed! Please install FFmpeg to use this program.")
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
download_button = ttk.Button(root, text="Search", command=search_url)
download_button.pack(pady=10)

album_name = ttk.Label(root, text="Name", font=("Helvetica", 16))
album_name.pack(pady=10)


imagebox = ttk.Label(root)
imagebox.pack()

sv_ttk.set_theme("dark")

# Run the application


if __name__ == "__main__":
    root.mainloop()