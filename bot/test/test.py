# It's importing the modules that are going to be used in the tests.
import unittest
import textInput as tex
import requests
import wifiStatus


# This class tests the translate function, the checkAcronyms function, and the connection function.
class TranslateTestCase(unittest.TestCase):

    def test_check_translate(self):
        """
        The function takes a string and a language code, and returns the string translated into the
        language specified by the language code
        """
        result = tex.translate('A total of seven unit tests were developed in order to corroborate the correct functioning of the modules that make up the application, which in order of execution consist of testing the internet connection, the operation of the Deep translator library, the verification of the language objective in terms of the list of languages ​​supported by the library, finally, if it contains only numeric characters, special characters or if the input is equal to the output, processes that are sufficient to determine if the application works as expected.', 'es')
        self.assertEqual(result, 'Se desarrollaron un total de siete pruebas unitarias con el fin de corroborar el correcto funcionamiento de los módulos que componen la aplicación, las cuales por orden de ejecución consisten en probar la conexión a internet, el funcionamiento de la biblioteca Deep traductor, la verificación del idioma objetivo en cuanto a la lista de idiomas soportados por la biblioteca, finalmente, si contiene solo caracteres numéricos, caracteres especiales o si la entrada es igual a la salida, procesos que son suficientes para determinar si la aplicación funciona como se espera.')

    def test_check_acronyms_true(self):
        """
        The function checks if the acronym is in the list of acronyms
        """
        result = tex.checkAcronyms('es')
        self.assertEqual(result, True)

    def test_check_acronyms_false(self):
        """
        This function checks if the input is an acronym
        """
        result = tex.checkAcronyms('tq')
        self.assertEqual(result, False)

    # def test_slack_conn(self):
    #     """
    #     It's a function that tests the connection to Slack
    #     """
    #     slack = conn.connection()
    #     result = requests.post(slack[0], json={'text': slack[1]})
    #     self.assertEqual(result.text, 'ok')

    def test_wifi_status(self):
        """
        The function is supposed to return a boolean value of True or False depending on the status of
        the wifi connection.
        """
        result = wifiStatus.connStatus()
        self.assertEqual(result, True)

# It's a way to run the tests.
if __name__ == '__main__':
    unittest.main()
