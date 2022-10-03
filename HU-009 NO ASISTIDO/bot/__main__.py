from urllib.error import URLError

from auth.sharepoint_credentials import auto_verifier
from connections import setting_conn
from connections.email_conn import connection, closeConnection
from connections.wifi_status import connStatus
from scripts.text_input import translation

@auto_verifier
def main(credentials = None) -> None:
    try:
        setting_conn.setLogFolder()
        setting_conn.setDailyFolder()
        if not connStatus:
            raise URLError(reason='No Internet connection')
        else:
            connection()
            setting_conn.sendStartEmail()
            translation()
            closeConnection()
    except:
        setting_conn.sendErrorEmail("error_message")


main(credentials = setting_conn.getCredentials())
