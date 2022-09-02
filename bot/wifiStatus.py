import urllib


def connStatus() -> bool:
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
