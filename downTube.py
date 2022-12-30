from pytube import YouTube, Playlist
from pytube.cli import on_progress #this module contains the built in progress bar. 
from pathlib import Path
from termcolor import colored
import argparse
import sys
import re

from cfonts import render, say

import tkinter as tk
import subprocess

# import tkinter.filedialog

chunk_size = 1024

# root
SAVE_PATH = str(Path.home() / "Downloads/downTube")
URLS_FILE = 'url.txt'
VIDEO_FORMAT = 'mp4'
AUDIO_FORMAT = 'mp3'
RESOLUTION = 'BEST'

# options
skip_repeated_playlist_videos = False
always_download_playlist = True

# global
queued = set()
file_size = 0

# trackers
url_count = 0

 # Create the main window
window = tk.Tk()
# Prevent the window from being resized
window.resizable(width=False, height=False)

bg_color = "#282828"

# Create a label and pack it into the window
logo_image = tk.PhotoImage(file="logo.png")
label = tk.Label(image=logo_image, bg="#282828")

def main():

    welcome = render('downTube', colors=['red', 'yellow'], align='center')
    print(welcome)

    # Change the background color of the window
    window.config(bg="#282828")

    # Set the window title
    window.title("downTube")

    # Set the size of the window
    window.geometry("800x500")

    # Create the button
    button = tk.Button(window, text="💡", width=4, height=2, command=change_color, fg="black", bg="#ECA869", activeforeground="#FFFFFF", activebackground="#B08BBB")

    # Place the button in the top right corner of the screen
    button.pack(side="top", anchor="nw")
    
    label.pack()

    # Create a button and pack it into the window
    button1 = tk.Button(text="OPEN", padx=52, pady=5, fg="white", bg="#0072C6", activeforeground="#FFFFFF", activebackground="#0072C6", command=open_text_file)
    button2 = tk.Button(text="CLEAR", padx=50, pady=5, fg="white", bg="#0072C6", activeforeground="#FFFFFF", activebackground="#0072C6", command=clear_text_file)
    button3 = tk.Button(text="BULK DOWNLOAD", padx=100, pady=5, fg="white", bg="#0072C6", activeforeground="#FFFFFF", activebackground="#0072C6", command=text_file_download_clicked)
    button1.pack()
    button2.pack()
    button3.pack()

    # Create a separator and pack it into the window
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    # Create a text box and pack it into the window
    text_box = tk.Entry(fg="#0072C6", bg="#FFFFFF", font=("Arial", 14), insertbackground="#0072C6", justify=tk.CENTER, state=tk.NORMAL)
    text_box.pack()
    button = tk.Button(text="Download", fg="white", bg="#0072C6", font=("Arial", 14), activeforeground="#FFFFFF", activebackground="#0072C6", highlightcolor="#0072C6", highlightthickness=2, highlightbackground="#FFFFFF", relief=tk.SUNKEN, padx=100, pady=5, command=lambda: download_click(text_box.get()))
    button.pack()
    # Show the window
    window.mainloop()

    userInputs()

def change_color():
  global bg_color
  # Toggle the background color between white and red
  if bg_color == "#282828":
    bg_color = "white"
  else:
    bg_color = "#282828"
  # Change the background color of the window
  window.configure(bg=bg_color)
  label.configure(bg=bg_color)

def open_text_file():
  # Open the text file in the default text editor
  subprocess.run(["notepad.exe", "url.txt"])

def clear_text_file():
    with open(URLS_FILE, 'w') as txt_file:
            txt_file.writelines("\n")
            print(colored(f'{URLS_FILE} CLEANED !', 'green'))

def text_file_download_clicked():
    # This function will be called when the button is clicked
    
    print("Downloading from txt")
    global queued
    queued = convert(URLS_FILE)

    if queued:
        for link in queued:
            download(link)
    
    print()
    sys.exit(input("Press enter to exit..."))

def download_click(raw_url):

    # This function will be called when the button is clicked
    print("Downloading from txt")
    url = validate(raw_url)
    download(url)
        


def convert(file):
    """
    Convert url.txt file to links and add them to global links
    """

    links = set()
    global url_count

    print()
    print(colored('Checking:', attrs=["bold"]), URLS_FILE)

    try:
        with open(file, 'r') as txt_file:
            txt = txt_file.readlines()

            # Validating each line in the text file
            for line in txt:
                if not line.isspace():
                    id = validate(line)
                    
                    if len(id) == 11: link = "v=" + id
                    if len(id) == 34: link = "playlist?list=" + id

                    if not link == 1: links.add(link)
            
            url_count = len(links)
            if url_count == 0:
                print(colored(f'NO LINKS FOUND !', 'red'))
                sys.exit(input("Press enter to exit..."))
            else:
                print(colored(f'{url_count} LINKS FOUND !\n', 'green'))
                return links
            
    except FileNotFoundError:
        print(colored(f'{URLS_FILE} NOT FOUND !', 'red'))
        sys.exit(input("Press enter to exit..."))


def validate(link):
    """
    Validate a link and capture the video or playlist URL

    :pytube expression: (?:v=|\/)([0-9A-Za-z_-]{11}).*
    
    Group 1 and 2 - Videos | Group 3 and 4 - Playlist
    """
    if 'list' in link and 'watch' in link:
        if always_download_playlist:
            print(colored('ALWAYS DOWNLOAD PLAYLIST IS ON \n', 'yellow'))
            search = re.search(r'(?:list=([0-9A-Za-z_-]{34}))', link)
            return str(search.group(1))

    search = re.search(
        r'(?:(?:(?:v=|\/)([0-9A-Za-z_-]{11}))|(^[0-9A-Za-z_-]{11}$)|(?:(?:list=([0-9A-Za-z_-]{34})))|(^[0-9A-Za-z_-]{34}$))', link
    )

    try:
        if not search.group(1) == None:
            return str(search.group(1))
        elif not search.group(2) == None:
            return str(search.group(2))
        elif not search.group(3) == None:
            return str(search.group(3))
        elif not search.group(4) == None:
            return str(search.group(4))
        else:
            raise AttributeError

    except AttributeError:
        print(colored('AttributeError, Check the URL', 'red'))
        return 1


def download(link):
    """
    Download and save a video or a playlist
    
    :param link: List of URLs
    :type link: text file
    """
    
    # Checking for playlist
    if 'list' in link:
        print(colored('Found a playlist...', 'green'))

        try:
            playlist = Playlist(link)
        except:
            print(colored(f'error! a playlist skiped', 'red'))
            return 2

        print(colored('Searching: ', attrs=["bold"]), 'Playlist -', playlist.title)
        print(colored(f'Found {len(playlist.video_urls)} videos from the playlist', 'green'))

        # Downloading playlist
        for video in playlist.video_urls:
            if skip_repeated_playlist_videos:
                # Skipping repeated videos
                search = re.search(r'(v=([0-9A-Za-z_-]{11}))', video)
                if search.group(1) in queued: print(colored(f'A video skipped - already queued.', 'red'))
            else:
                download(video)

        print()
    else:
        # Searches for the video and sets up the callback to run the progress indicator. 
        try: yt = YouTube(link, on_progress_callback=on_progress)
        except:
            print(colored('Error: Video unavaliable!', 'red'))
            return 3

    
    if RESOLUTION == 'BEST':
        #Get the first video type - usually the best quality.
        video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()

    #Gets the title of the video
    title = yt.title

    #Prepares the file for download
    print(colored(f'Downloading:', attrs=["bold"]), title)
    global file_size
    file_size = video.filesize
    print(colored(f"[{round(file_size/1024/1024, 1)}MB]"), end=" ")

    #Starts the download process
    video.download(SAVE_PATH)
    print(colored('- Done', 'green'))




#! Not working 
# # on_progress_callback 2 Example functions

# def progress(stream, chunk, file_handle, bytes_remaining):
#     contentSize = file_size
#     size = contentSize - bytes_remaining

#     print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
#     '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')

# def progress_function(chunk, file_handle, bytes_remaining):
#     global file_size
#     current = ((file_size - bytes_remaining)/file_size)
#     percent = ('{0:.1f}').format(current*100)
#     progress = int(50*current)
#     status = '█' * progress + '-' * (50 - progress)
#     sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
#     sys.stdout.flush()


if __name__ == "__main__":
    main()
