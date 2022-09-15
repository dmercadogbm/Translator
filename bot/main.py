# Importing the os module.
import os
# Importing the URLError class from the urllib.error module.
from urllib.error import URLError

# Importing the GOOGLE_LANGUAGES_TO_CODES dictionary from the constants.py file.
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

# Importing the verifier function from the sharepoint_credentials.py file.
from auth.sharepoint_credentials import verifier
# Importing the connection function from the email_conn.py file.
from connections.email_conn import connection
# Importing the connStatus variable from the wifi_status.py file.
from connections.wifi_status import connStatus
# Importing the translation function from the text_input.py file.
from scripts.text_input import translation


@verifier
def main() -> None:
    """
    If the connection status is false, raise an exception, otherwise, clear the screen, print the
    languages, and call the connection and translation functions.
    """
    try:
        if connStatus == False:
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


# A function that is being called by the `verifier` decorator.
main()
