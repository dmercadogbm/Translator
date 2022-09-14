# Importing the os module.
import os

# Importing the wifiStatus module from the connections package.
import connections.wifi_status as ws


# Importing the translation function from the textInput module.
from scripts.text_input import translation

# Importing the GOOGLE_LANGUAGES_TO_CODES dictionary from the constants module in the deep_translator
# package.
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
# Importing the verifier function from the sharepoint_credentials module.
from auth.sharepoint_credentials import verifier
# Importing the URLError class from the urllib.error module.
from urllib.error import URLError
# Importing the connection function from the emailConn module.
from connections.email_conn import connection


@verifier
def main() -> None:
    """
    If the internet is connected, clear the screen and print the available languages. If the internet is
    not connected, raise an exception.
    """
    try:
        if ws.connStatus() == False:
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
