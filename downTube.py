from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import csv
import sys

# root
SAVE_PATH = str(Path.home() / "Downloads/downTube")
URLS_FILE = 'url.csv'
count = 0

def main():
    link = input("Enter the YouTube video URL: ")

    if link:
        Download(link)
        sys.exit()

    links = Csv_to_list(URLS_FILE)
    links_count = len(links)
    print(links_count, 'added to queue')

    if links:
        for link in links:
            Download(str(link))
    Status(links_count)


# Download and Save
def Download(link):
    global count
    is_playlist = False
    
    # Checking for playlist
    # ! BUG - Not working
    if 'playlist' in link:
        playlist = Playlist(link)
        print(f'Playlist: ')
        is_playlist = True
    else:
        video = YouTube(link)
    
    # Downloading playlist
    if is_playlist:
        print(len(playlist.video_urls), 'videos in the playlist')
        for url in playlist.video_urls:
            print(url)
        for video in playlist.videos:
            print(f'Downloading: ')
            try:
                video.streams.get_highest_resolution().download(SAVE_PATH)
            except:
                print("An error has occurred")
        count += 1

        # ! Recursion - Extract url one by one

    # Downloading single video
    else:
        print(f'Downloading: {video.title}')
        video = video.streams.get_highest_resolution()
        try:
            video.download(SAVE_PATH)
            count += 1
            print("Done")
        except:
            print("An error has occurred")
        
            

# Converting CSV to a list
def Csv_to_list(file):
    print('Checking url.csv')
    try:
        with open(file, 'r') as urls:
            reader = csv.reader(urls)
            return list(reader)
    except FileNotFoundError:
        sys.exit(f"url.csv - not found")

# Printing report
def Status(links):
    if links == count:
        print("Download is completed successfully.")
    elif count > 0:
        print(count, 'out of', links, "download has completed successfully.")
    else:
        print("Nothing has downloaded.")




if __name__ == "__main__":
    main()
