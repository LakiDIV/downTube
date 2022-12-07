from termcolor import colored


class Tracker:
    """
    All trackers
    """

    def __init__(self, url_count=0, playlist_count=0) -> None:
        if not url_count:
            raise ModuleNotFoundError(colored(f'Missing URLs\n', 'red'))
        self.url_count = url_count
        self.playlist_count = playlist_count

        # self.url_pass_count = 0
        # self.url_fail_count = 0
        # self.url_skipped_count = 0
        # self.playlist_count = 0

    def __str__(self) -> str:
        return colored(f'{self.url_count} URLs have found.\n', 'green')


    def status():
        """Reports the summery of the program to the user"""
        ...
