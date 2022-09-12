# It's importing the modules that are going to be used in the tests.
import unittest
import textInput as tex
import slackConn as conn
import requests
import wifiStatus


# This class tests the translate function, the checkAcronyms function, and the connection function.
class TranslateTestCase(unittest.TestCase):

    def test_check_translate(self):
        """
        The function takes a string and a language code, and returns the string translated into the
        language specified by the language code
        """
        result = tex.translate('hello world i dont know what i supposed to print here but here we come', 'es')
        self.assertEqual(result, 'hola mundo, no sé qué se supone que debo imprimir aquí, pero aquí vamos')

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

    def test_slack_conn(self):
        """
        It's a function that tests the connection to Slack
        """
        slack = conn.connection()
        result = requests.post(slack[0], json={'text': slack[1]})
        self.assertEqual(result.text, 'ok')

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
