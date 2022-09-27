# Importación de los módulos necesarios.
from urllib.error import URLError

from auth.sharepoint_credentials import verifier
from connections.email_conn import connection
from connections.wifi_status import connStatus
from scripts.text_input import translation

from datetime import datetime

#@verifier
def main() -> None:
    """
    Si no hay conexión a Internet, genere una excepción; de lo contrario, borra la pantalla, imprime los
    idiomas, conéctese a la API de Google Translate y traduzca el texto.
    """
    try:
        now = datetime.now()
        dateYMD = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        dateYMDHMS = str(dateYMD) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        if not connStatus:
            raise URLError(reason='No Internet connection')
        else:
            #connection()
            error_doc_name = "ERROR-"+dateYMD+".txt"
            print(error_doc_name)
            translation()
    except Exception as e:
        error_doc_name = "ERROR-"+dateYMD+".txt"
        print(error_doc_name)
        with open("bot/log/error/"+error_doc_name, "a", encoding="utf-8") as error_file:
            error_file.write(dateYMDHMS + " [ERROR] = " + str(e))
            error_file.write("\n")


main()
