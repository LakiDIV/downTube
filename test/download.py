from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import sys


class Download:
    def __init__(self) -> None:
        self._download_count = 0
        self._url_count = 0

    @property
    def download_count(self):
        return self._download_count
    
    @property
    def url_count(self):
        return self._url_count

    # This function will convert txt file to a set
    def convert(self):
        ...

    # This function will download a video file or a playlist
    def download(self):
        ...