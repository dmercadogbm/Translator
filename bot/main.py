import os
import requests
import slackConn

from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES


def translate(text: str, target_leng: str) -> str:
    """
    It takes a string of text and a target language and returns the translated text

    :param text: The text you want to translate
    :type text: str
    :param target_leng: The language you want to translate to
    :type target_leng: str
    :return: A string
    """
    translator = GoogleTranslator(
        source='auto', target=target_leng)
    result = translator.translate(text)
    return (result)


def checkAcronyms(target_leng):
    """
    It checks if the language is supported by the translator

    :param target_leng: The language you want to translate to
    :return: a boolean value.
    """
    try:
        translate('prueba', target_leng)
    except LanguageNotSupportedException:
        return False
    return True


def translateProcess():
    """
    It takes an acronym as input, checks if it's in the list of acronyms, if it is, it takes a text as
    input, checks if it contains the string 'xx', if it doesn't, it translates the text and posts it to
    slack, if it does, it starts the function again
    """
    if __name__ == '__main__':
        for key, value in GOOGLE_LANGUAGES_TO_CODES.items():
            print(key," : ", value)

    target_leng = input('Type an acronym:')
    while True:
        if checkAcronyms(target_leng) == True:
            text = input('text:').lower()
            if 'xx' not in text:
                print(translate(text, target_leng))
                slack = slackConn.connection()
                requests.post(slack[0], json={'text': slack[1]})
            else:
                translateProcess()
        else:
            print("Acronym not found, please try again")
            translateProcess()


# It's a way to make sure that the code is only executed when the file is run directly.
if __name__ == '__main__':
    os.system('cls')
    translateProcess()
