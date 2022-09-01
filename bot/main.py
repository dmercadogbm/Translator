import os
import requests
import slackConn

from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from getmac import get_mac_address as gma


def checkacronymus(target_leng):
    try:
        translate('prueba', target_leng)
    except LanguageNotSupportedException:
        return False
    return True


def translate(text: str, target_leng: str) -> str:
    translator = GoogleTranslator(
        source='auto', target=target_leng)
    result = translator.translate(text)
    return (result)


def translateProcess():

    target_leng=input('Type an acronym:')
    while True:
        if checkacronymus(target_leng) == True:
            text = input('text:')
            if 'xx' not in text:
                print(translate(text, target_leng))
                slack = slackConn.connection()
                requests.post(slack[0], json={'text': slack[1]})
            else:
                translateProcess()
        else:
            print("Acronym not found, please try again")
            translateProcess()



if __name__ == '__main__':
    os.system('cls')
    translateProcess()
else:
    translateProcess()
