import requests


def get_image_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content
