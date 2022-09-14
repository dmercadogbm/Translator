# Importing the urllib module.
import urllib


def connStatus() -> bool:
    """
    It tries to open a connection to google.com, and if it succeeds, it returns True, otherwise it
    returns False
    :return: A boolean value.
    """
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
