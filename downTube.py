from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import sys
import re

# root
SAVE_PATH = str(Path.home() / "Downloads/downTube")
URLS_FILE = 'url.txt'
videos_count = 0
playlist_count = 0


def main():
    
    print("Press enter to start searching url.txt")
    
    while True:
        # Getting user inputs
        try: url = input("Enter the YouTube video URL: ")
        except KeyboardInterrupt: sys.exit("Bye!")

        if url == '':
            break

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


# Checking url.txt file
def Convert(file):
    links = set()
    print('Checking url.txt')
    try:
        with open(file, 'r') as txt_file:
            txt = txt_file.readlines()

            # Validating each line in the text file
            for line in txt:
                links.add(check_link(line))
            print(len(links), 'links added to queue')
            print()
            return links
            
    except FileNotFoundError:
        sys.exit(f"url.txt - not found")


# Download and Save
def Download(link):
    global videos_count
    global playlist_count
    is_playlist = False
    
    # Checking for playlist
    if 'list' in link:
        if re.match('(?:v=|\/)([0-9A-Za-z_-]{11}).*', link):
            print('Found a playlist attched to the video...')

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
        except KeyboardInterrupt:
            print("Donwload skipped !")
        except:
            print("An error has occurred")
        else:
            print("- Done")
        
        
# Printing report
def status(links):
    # ! Need to redo this function
    # TODO - Total links -> Playlists -> Videos
    # TODO - How many of links succesfully downloaded

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


# ! add support to different types of links
# TODO - Return modified list to identify video was attached to a playlist

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
