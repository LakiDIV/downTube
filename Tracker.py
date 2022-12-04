class Tracker:
    """
    All trackers
    """

    def __init__(self, urls_count) -> None:
        if not urls_count:
            raise ModuleNotFoundError("Missing URLs")
        self.urls = urls_count
        # self.url_pass_count = 0
        # self.url_fail_count = 0
        # self.url_skipped_count = 0
        # self.playlist_count = 0

    def __str__(self) -> str:
        return f"{self.url_count} URLs have found."


    def status():
        """Reports the summery of the program to the user"""
        ...
