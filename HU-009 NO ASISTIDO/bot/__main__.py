from urllib.error import URLError

from auth.sharepoint_credentials import verifier
from connections import setting_conn
from connections.email_conn import connection, closeConnection
from connections.wifi_status import connStatus
from scripts.text_input import translation

# @verifier


def main() -> None:
    try:
        if not connStatus:
            raise URLError(reason='No Internet connection')
        else:
            connection()
            setting_conn.sendStartEmail()
            translation()
            closeConnection()
    except Exception as e:
        setting_conn.setErrorMessage(str(e))


main()
