import ntplib
from datetime import datetime, timezone

class NTPTimer:
    """
    A class to interact with an NTP server to fetch the current time
    and calculate elapsed time since the instance was created.
    """

    def __init__(self, host: str = 'pool.ntp.org'):
        """
        Initialise the NTPTimer instance and record the initial timestamp
        """
        self.host = host  # Store the NTP server hostname
        self.start = self.get_current_time()  # Record the initial timestamp

    def get_current_time(self) -> datetime:
        """
        Query the NTP server and return the current time as a datetime object.
        If the NTP server is unreachable or times out, fall back to system UTC time.
        """
        client = ntplib.NTPClient() # Create a NTP client instance
        try:
            # Send a request to the NTP server with a 1-second timeout
            resp = client.request(self.host, version=3, timeout=1)
            # resp.tx_time is the time in seconds in UTC time
            return datetime.fromtimestamp(resp.tx_time, tz=timezone.utc)
        except (ntplib.NTPException, TimeoutError, OSError) as e: # Catch NTP errors, timeout, or socket errors
            print(f"NTP request failed or timed out: {e}. Falling back to system time.")
            return datetime.now(timezone.utc) # Fallback to system's current UTC time

    def elapsed_seconds(self) -> float:
        """
        Calculate the number of seconds elapsed since the instance was created.
        """
        now = self.get_current_time()  # Get the current time from the NTP server
        delta = now - self.start  # Calculate the time difference
        return delta.total_seconds()  # Return the elapsed time in seconds