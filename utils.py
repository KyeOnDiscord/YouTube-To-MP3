import requests
import subprocess


def get_image_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def is_ffmpeg_installed():
    try:
        # Try to run ffmpeg version command
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        # Check the return code (0 indicates success)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


if is_ffmpeg_installed():
    print("FFmpeg is installed!")
else:
    print("FFmpeg is not installed.")
