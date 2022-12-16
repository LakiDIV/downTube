@ECHO OFF

:: This CMD script install all the requirement packages to run downTube.

TITLE Installing packages

ECHO Please wait... Gathering package names.

ECHO =========================

pip install pytube pathlib termcolor argparse

PAUSE