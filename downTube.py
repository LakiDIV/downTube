from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import sys
import re

# root
SAVE_PATH = str(Path.home() / "Downloads/downTube")
URLS_FILE = 'url.txt'

always_download_playlist = False # If a playlist attched to the link of a video, download the playlist

# global variables
url_count = 0
playlist_count = 0
download_count = 0


def main():
    print("Add urls to",URLS_FILE, "and,")
    print("Press enter to start searching", URLS_FILE)
    print("or")

    while True:
        # Getting user inputs
        try: url = input("Enter the YouTube video URL: ")
        except KeyboardInterrupt: sys.exit("Bye!")

        if url == '': break

        # validating user inputs
        if not len(url) < 11:
            Download(check_link(url))
        else:
            print("Check the URL")
        
    # url.txt file
    links = Convert(URLS_FILE)

    if links:
        for link in links:
            Download(link)

    status()

# Checking url.txt file
def Convert(file):
    global url_count
    links = set()
    print('Checking url.txt')
    try:
        with open(file, 'r') as txt_file:
            txt = txt_file.readlines()

            # Validating each line in the text file
            for line in txt:
                links.add(check_link(line))

            url_count = len(links)
            print(url_count, 'links added to queue')
            print()
            return links
            
    except FileNotFoundError:
        sys.exit(f"url.txt - not found")


# Download and Save
def Download(link):
    global download_count
    global playlist_count
    
    # Checking for playlist
    if 'list' in link:
        print('Found a playlist...')

        try:
            playlist = Playlist(link)
        except:
            print('error! a playlist skiped')
            return 2

        print()
        print(f'Searching playlist: {playlist.title}')
        print('Found', len(playlist.video_urls), 'videos')
        playlist_count += 1
        # Downloading playlist
        for video in playlist.video_urls:
            Download(video)
        print()
    else:
        try:
            video = YouTube(link)
        except:
            print('error! a video skiped')
            return 3
    
    # Downloading a single video
    print(f'Downloading: {video.title}')
    try:
        video.streams.get_highest_resolution().download(SAVE_PATH)
        download_count += 1
    except KeyboardInterrupt:
        print("Donwload skipped !")
    except:
        print("An error has occurred")
    else:
        print("- Done")
        
        
# Printing report
def status():
    if playlist_count > 0:
        print(playlist_count, 'playlist found !')
    print(download_count, 'videos downloaded succesfully.')
    # ! Need to redo this function
    # TODO - Total links -> Playlists -> Videos
    # TODO - How many of links succesfully downloaded

    ...


# TODO - If a plylist attached to the video, ask user to download playlist or not
def check_link(link):

    # Group 1 and 2 - Videos | Group 3 and 4 - Playlist
    search = re.search(r'(?:(?:(?:v=|\/)([0-9A-Za-z_-]{11}))|(^[0-9A-Za-z_-]{11}$)|(?:(?:list=([0-9A-Za-z_-]{34})))|(^[0-9A-Za-z_-]{34}$))', link)

    if not search.group(1) == None:
        capture = "v=" + str(search.group(1))
    elif not search.group(2) == None:
        capture = "v=" + str(search.group(2))
    elif not search.group(3) == None:
        capture = "playlist?list=" + str(search.group(3))
    elif not search.group(4) == None:
        capture = "playlist?list=" + str(search.group(4))
    else:
        print('error! a link skiped')
        return 1

    return capture

    # (?:v=|\/)([0-9A-Za-z_-]{11}).*    -pytube expression


if __name__ == "__main__":
    main()
