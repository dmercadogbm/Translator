from urllib.error import URLError

from auth.sharepoint_credentials import verifier
from connections import setting_conn
from connections.email_conn import connection
from connections.wifi_status import connStatus
from scripts.text_input import translation

from datetime import datetime

# @verifier


def main() -> None:
    """
    Si no hay conexión a Internet, genere una excepción; de lo contrario, borra la pantalla, imprime los
    idiomas, conéctese a la API de Google Translate y traduzca el texto.
    """
    try:

        if not connStatus:
            raise URLError(reason='No Internet connection')
        else:
            connection()
            translation()
    except Exception as e:
        setting_conn.setErrorMessage(str(e))


main()
