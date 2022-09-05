import os
import requests
import slackConn
import wifiStatus

from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from sharepoint_credentials import verifier
from urllib.error import URLError


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


def checkAcronyms(target_leng) -> bool:
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


def translateProcess() -> None:
    """
    It takes an acronym as input, checks if it's in the dictionary, if it is, it asks for text input, if
    the text input is #exit, it quits, if it's #back, it goes back to the beginning of the function, if
    it's not #back or #exit, it translates the text and posts it to slack
    """

    if __name__ == '__main__':
        for key, value in GOOGLE_LANGUAGES_TO_CODES.items():
            print(key, "->", value)

    target_leng = input('Type an acronym:')
    while checkAcronyms(target_leng) == True:
        text: str = input('text:')
        if '#exit' in text:
            quit()
        if '#back' not in text:
            translation : str = translate(text, target_leng)
            if text == translation:
                print('TranslationError, same meaning')
            else:
                print(translation)
                slack = slackConn.connection()
                requests.post(slack[0], json={'text': slack[1]})
        else:
            translateProcess()
    else:
        print("Acronym not found, please try again")
        translateProcess()


@verifier
def main() -> None:
    """
    It checks if the user is connected to the internet, if not, it raises an exception, if yes, it
    clears the screen and calls the translateProcess() function
    """
    if __name__ == '__main__':
        try:
            if wifiStatus.connStatus() == False:
                raise URLError(reason='No Internet connection')
            else:
                os.system('cls')
                translateProcess()
        except Exception as e:
            print(e)


main()
