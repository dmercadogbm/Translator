import urllib


def connStatus() -> bool:
    """
    Intenta abrir una conexión a google.com, y si tiene éxito, devuelve True, de lo contrario, devuelve
    False
    :return: Un valor booleano.
    """
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
