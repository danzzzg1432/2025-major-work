import ntplib, sys
from datetime import datetime, timezone

class NTPTimer:
    """
    A class to interact with an NTP server to fetch the current time
    and calculate elapsed time since the instance was created.
    """

    def __init__(self, host: str = 'pool.ntp.org'):
        """
        Initialise the NTPTimer instance and record the initial timestamp.

        Args:
            host (str): The NTP server hostname to query. Defaults to 'pool.ntp.org'.
        """
        self.host = host  # Store the NTP server hostname
        self.start = self.get_current_time()  # Record the initial timestamp

    def get_current_time(self) -> datetime:
        """
        Query the NTP server and return the current time as a datetime object.

        Returns:
            datetime: The current time in UTC as provided by the NTP server.
        """
        client = ntplib.NTPClient()  # Create an NTP client instance
        try:
            resp = client.request(self.host, version=3)  # Send a request to the NTP server
        except Exception as E:
            print("You require a functional internet connection to play!, or some fucking shitty ass error has occred and it doesnat want to fucking start")
            # sys.exit()
            print("Using saved time... ")
            return datetime.fromisoformat("2025-05-31T10:47:42.094985+00:00")
        # resp.tx_time is the time in seconds since the epoch (UTC)
        return datetime.fromtimestamp(resp.tx_time, tz=timezone.utc)

    def elapsed_seconds(self) -> float:
        """
        Calculate the number of seconds elapsed since the instance was created.

        Returns:
            float: The elapsed time in seconds.
        """
        now = self.get_current_time()  # Get the current time from the NTP server
        delta = now - self.start  # Calculate the time difference
        return delta.total_seconds()  # Return the elapsed time in seconds