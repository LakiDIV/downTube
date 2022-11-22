from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import sys


class Download:
    def __init__(self) -> None:
        pass
    
    # Checking link
    def check_link(self, link):
        if 'playlist' in link:
            playlist = Playlist(link)
            print()
            print(f'Searching playlist: {playlist.title}')
        else:
            try:
                video = YouTube(link)
                download_video(video)
            except:
                print('error! a video skiped')
                return

    # Downloading playlist
    def download_playlist(self, playlist):
        print('Found', len(playlist.video_urls), 'videos')

        for video in playlist.video_urls:
            download_video(video)
        print()

    # Downloading single video
    def download_video(self, video):
        print(f'Downloading: {video.title}')
        try:
            video.streams.get_highest_resolution().download(SAVE_PATH)
        except:
            print("An error has occurred")
        else:
            print("- Done")
