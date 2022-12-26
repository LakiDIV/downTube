# downTube
#### Video Demo:  https://www.youtube.com/watch?v=qdU-cHqeHBk
#### Description: This is a command-line application that allows you to download videos from YouTube. It is built using the PyTube library, which is a powerful Python library for interacting with YouTube.
<hr />

The application reads URLs from a URL.txt file and downloads all the videos listed in the file. The downloaded videos are saved in the user's download folder.

In addition to downloading videos from a text file, the application also supports adding URLs to the text file and clearing the text file using command-line arguments. It also allows you to download a specific number of videos directly from the command line, without using the text file.

## Installation
To install the dependencies for this application, run the following command:

`pip install -r requirements.txt`

## Usage
To use this application, run the following command:

`python downnTube.py`

This will download all the videos listed in the `URL.txt` file and save them in the user's download folder.

To add URLs to the text file, use the `-a` argument followed by the number of URLs you want to add:

`python downTube.py -a 3`

To clear the text file, use the `-c` or `--clear` argument:

`python downTube.py -c`

To download a specific number of videos directly from the command line, use the `-n` argument followed by the number of videos you want to download:

`python downTube.py -n 5`

## Configuration

You can configure the application by modifying the following constants in the `downTube.py` file:

- VIDEO_FORMAT: The video format to download (e.g. 'mp4', 'webm').
- AUDIO_FORMAT: The audio format to download (e.g. 'mp3', 'aac').
- RESOLUTION: The resolution of the video to download (e.g. '720p', '1080p').

## Credits

PyTube library: https://github.com/nficano/pytube

## License

This application is licensed under the MIT License. See the LICENSE file for details.
