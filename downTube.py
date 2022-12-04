from pytube import YouTube
from pytube import Playlist
from pathlib import Path
from termcolor import colored
import argparse
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
links = set()


def main():

    parser = argparse.ArgumentParser(description="a YouTube video downloader")
    parser.add_argument("-n", default=0, help="Number of time to ask url", type=int)
    args = parser.parse_args()

    print()

    for _ in range(args.n):
        # Getting user inputs
        try: raw_url = input(colored("Enter the YouTube video URL", attrs=["bold", "underline"]) + ": ")
        except KeyboardInterrupt: sys.exit(colored("Bye!", 'yellow'))

        # validating user inputs
        url = check_link(raw_url)
        if not url == 1:
            Download(url)
        raw_url = None
    
    # convert url.txt file to a set
    Convert(URLS_FILE)

    if links:
        for link in links:
            Download(link)

    status()


def Convert(file):
    """Extract urls from the text file"""
    global url_count
    global links

    print()
    print(colored('Checking:', attrs=["bold"]), URLS_FILE)

    try:
        with open(file, 'r') as txt_file:
            txt = txt_file.readlines()

            # Validating each line in the text file
            for line in txt:
                links.add(check_link(line))

            url_count = len(links)
            if url_count == 0:
                sys.exit(colored(f'NO LINKS FOUND !', 'red'))

            print(colored(f'{url_count} links added to queue', 'green'))
            print()
            
    except FileNotFoundError:
        sys.exit(colored(f'{URLS_FILE} NOT FOUND !', 'red'))


# TODO - If a plylist attached to the video, ask user to download playlist or not
def check_link(link):
    """
    Validate a link and capture the video or playlist URL

    :pytube expression: (?:v=|\/)([0-9A-Za-z_-]{11}).*
    
    Group 1 and 2 - Videos | Group 3 and 4 - Playlist
    """
    search = re.search(r'(?:(?:(?:v=|\/)([0-9A-Za-z_-]{11}))|(^[0-9A-Za-z_-]{11}$)|(?:(?:list=([0-9A-Za-z_-]{34})))|(^[0-9A-Za-z_-]{34}$))', link)

    try:
        if not search.group(1) == None:
            capture = "v=" + str(search.group(1))
        elif not search.group(2) == None:
            capture = "v=" + str(search.group(2))
        elif not search.group(3) == None:
            capture = "playlist?list=" + str(search.group(3))
        elif not search.group(4) == None:
            capture = "playlist?list=" + str(search.group(4))
        else:
            raise AttributeError

    except AttributeError:
        print(colored('AttributeError, Check the URL', 'red'))
        return 1

    return capture


def Download(link):
    """
    Download and save a video or a playlist
    
    :param link: List of URLs
    :type link: text file
    """
    global download_count
    global playlist_count
    
    # Checking for playlist
    if 'list' in link:
        print()
        print(colored('Found a playlist...', 'green'))

        try:
            playlist = Playlist(link)
        except:
            print(colored(f'error! a playlist skiped', 'red'))
            return 2

        print(colored('Searching: ', attrs=["bold"]), 'Playlist -', playlist.title)
        print('Found', len(playlist.video_urls), 'videos')
        playlist_count += 1
        # Downloading playlist
        for video in playlist.video_urls:
            #! skipping not wotking - need to skip reapeted downloadings
            if not video in links:
                Download(video)
            else:
                print(f'Skipped: {video.title}')
        print()
    else:
        try:
            video = YouTube(link)
        except:
            print(colored('error! a video skiped', 'red'))
            return 3
    
    # Downloading a single video
    print(colored(f'Downloading:', attrs=["bold"]), video.title)
    try:
        video.streams.get_highest_resolution().download(SAVE_PATH)
        download_count += 1
    except KeyboardInterrupt:
        print(colored('Donwload skipped !', 'yellow'))
    except:
        print(colored('An error has occurred', 'red'))
    else:
        print(colored('- Done', 'green'))


def status():
    """Reports the summery of the program to the user"""
    print()
    if playlist_count > 0:
        print(playlist_count, 'playlist found !')
    print(download_count, 'videos downloaded succesfully.')
    print()
    # ! Need to redo this function
    # TODO - Total links -> Playlists -> Videos
    # TODO - How many of links succesfully downloaded

    ...


if __name__ == "__main__":
    main()
