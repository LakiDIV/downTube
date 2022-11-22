from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import sys


# root
SAVE_PATH = str(Path.home() / "Downloads/downTube")
URLS_FILE = 'url.txt'
videos_count = 0
playlist_count = 0


def main():
    
    link = input("Enter the YouTube video URL: ")

    # (?:v=|\/)([0-9A-Za-z_-]{11}).*    pytube exception
    
    links = txt_list(URLS_FILE)
    links_count = len(links)

    print(links_count, 'links added to queue')
    print()

    if links:
        for link in links:
            Download(link)

    Status(links_count)


# Download and Save
def Download(link):
    global videos_count
    global playlist_count
    is_playlist = False
    
    # Checking for playlist
    if 'playlist' in link:
        playlist = Playlist(link)
        print()
        print(f'Searching playlist: {playlist.title}')
        is_playlist = True
    else:
        try:
            video = YouTube(link)
        except:
            print('error! a video skiped')
            return

    # Downloading playlist
    if is_playlist:
        print('Found', len(playlist.video_urls), 'videos')
        playlist_count += 1

        for video in playlist.video_urls:
            Download(video)
        print()

    # Downloading single video
    else:
        print(f'Downloading: {video.title}')
        try:
            video.streams.get_highest_resolution().download(SAVE_PATH)
            videos_count += 1
        except:
            print("An error has occurred")
        else:
            print("- Done")
        
            
# handling the text file
def txt_list(file):
    print('Checking url.txt')
    try:
        with open(file, 'r') as urls:
            return urls.readlines()
    except FileNotFoundError:
        sys.exit(f"url.csv - not found")


# Printing report
def Status(links):
    print()

    if links > videos_count:
        print(links-playlist_count, 'links has rejected.')
        print(videos_count, 'out of', links, "download has completed successfully.")
    
    print(videos_count, 'videos has downloaded.')

    if videos_count >= links:
        print("Download is completed successfully.")
    elif videos_count == 0:
        print("Nothing has downloaded.")
    print()


if __name__ == "__main__":
    main()
