# Importación de los módulos necesarios.
import os
from urllib.error import URLError

from connections import email_conn
from connections import setting_conn

from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

from auth.sharepoint_credentials import verifier
from connections.email_conn import connection
from connections.wifi_status import connStatus
from scripts.text_input import translation


#@verifier
def main() -> None:
    """
    Si no hay conexión a Internet, genere una excepción; de lo contrario, borra la pantalla, imprime los
    idiomas, conéctese a la API de Google Translate y traduzca el texto.
    """
    try:
        setting_conn.setLogFolder()
        setting_conn.setDailyFolder()
        if not connStatus:
            raise URLError(reason='No Internet connection')
        else:
            os.system('cls')
            connection()
            if __name__ == '__main__':
                for key, value in GOOGLE_LANGUAGES_TO_CODES.items():
                    print(key, "->", value)
            setting_conn.sendStartEmail()
            translation()
    except Exception as e:
        setting_conn.setErrorMessage(str(e))
        setting_conn.sendErrorEmail(str(e))


main()
