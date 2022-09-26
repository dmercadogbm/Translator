# Importación de los módulos necesarios.
import os
from urllib.error import URLError

from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

from auth.sharepoint_credentials import verifier
from connections.email_conn import connection
from connections.wifi_status import connStatus
from scripts.text_input import translation


@verifier
def main() -> None:
    """
    Si no hay conexión a Internet, genere una excepción; de lo contrario, borra la pantalla, imprime los
    idiomas, conéctese a la API de Google Translate y traduzca el texto.
    """
    try:
        if not connStatus:
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
