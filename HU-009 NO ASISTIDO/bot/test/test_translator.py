# Importación de los módulos que se van a probar.
import scripts.text_input as tex
import connections.wifi_status as ws


def test_wifi_status():
    """
    Esta función prueba el estado de conexión del WiFi
    """
    result = ws.connStatus()
    assert result == True


def test_check_translate():
    """
    Esta función prueba la traducción de un texto de inglés a español
    """
    result = tex.translate('A total of seven unit tests were developed in order to corroborate the correct functioning of the modules that make up the application, which in order of execution consist of testing the internet connection, the operation of the Deep translator library, the verification of the language objective in terms of the list of languages ​​supported by the library, finally, if it contains only numeric characters, special characters or if the input is equal to the output, processes that are sufficient to determine if the application works as expected.', 'es')
    assert result == 'Se desarrollaron un total de siete pruebas unitarias con el fin de corroborar el correcto funcionamiento de los módulos que componen la aplicación, las cuales por orden de ejecución consisten en probar la conexión a internet, el funcionamiento de la biblioteca Deep traductor, la verificación del idioma objetivo en cuanto a la lista de idiomas soportados por la biblioteca, finalmente, si contiene solo caracteres numéricos, caracteres especiales o si la entrada es igual a la salida, procesos que son suficientes para determinar si la aplicación funciona como se espera.'


def test_check_acronyms():
    """
    Esta función comprueba si las siglas o el idioma están en el formato correcto
    """
    result = tex.checkAcronyms('es')
    assert result == True

