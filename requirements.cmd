@ECHO OFF

:: This CMD script install all the requirement packages to run downTube.

TITLE Installing packages

ECHO Please wait... Gathering package names.

ECHO =========================

py -m pip install git+https://github.com/pytube/pytube
pip install pathlib termcolor argparse cfonts

PAUSE