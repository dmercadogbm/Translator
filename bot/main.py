# Importing the os module.
import os
# Importing the wifiStatus module.
import wifiStatus


# Importing the translation function from the textInput module.
from textInput import translation
# Importing the constants from the deep_translator module.
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
# Importing the verifier function from the sharepoint_credentials module.
from sharepoint_credentials import verifier
# Importing the URLError class from the urllib.error module.
from urllib.error import URLError
# Importing the connection function from the emailConn module.
from emailConn import connection


# @verifier
def main() -> None:
    """
    If the internet is connected, clear the screen and print the available languages. If the internet is
    not connected, raise an exception.
    """
    try:
        if wifiStatus.connStatus() == False:
            raise URLError(reason='No Internet connection')
        else:
            os.system('cls')
            if __name__ == '__main__':
                for key, value in GOOGLE_LANGUAGES_TO_CODES.items():
                    print(key, "->", value)
            connection()
            translation()
    except Exception as e:
        print(e)


main()
