# Importando las bibliotecas que se necesitan para que el programa funcione.
import re

import connections.email_conn as emailConn
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES


def translate(text: str, target_leng: str) -> str:
    """
    Toma una cadena de texto y un idioma de destino y devuelve el texto traducido

    :param text: El texto que quieres traducir
    :type text: str
    :param target_leng: El idioma al que desea traducir
    :type target_leng: str
    :return: str
    """

    translator = GoogleTranslator(
        source='auto', target=target_leng)
    return (translator.translate(text))


def checkAcronyms(target_leng: str) -> bool:
    """
    Comprueba si el idioma de destino está en el diccionario de idiomas y sus siglas

    :param target_leng: str = El idioma al que desea traducir
    :type target_leng: str
    :return: bool.
    """

    if target_leng in GOOGLE_LANGUAGES_TO_CODES.values():
        return True
    elif target_leng in GOOGLE_LANGUAGES_TO_CODES.keys():
        return True
    else:
        return False



def numberInText(text):
    """
    Si el texto es numérico, genere un ValueError.
    
    :param text: El texto a revisar
    """
    if text.isnumeric():
        raise ValueError(
            '-> El texto debe contener letras ademas de numeros <-')


def specialInText(text):
    """
    Si el texto contiene un carácter de palabra (a-z, A-Z, 0-9, _) y un carácter especial, devuelve
    Falso.

    Si el texto contiene un carácter de palabra y ningún carácter especial, devuelva True.

    Si el texto no contiene caracteres de palabra y uno o más caracteres especiales, genera un error.

    Si el texto no contiene caracteres de palabra ni caracteres especiales, genera un error.

    Si el texto contiene un carácter de palabra y uno o más caracteres especiales, genera un error.

    :param text: El texto a analizar
    """

    if (re.search('(#exit)', text)) or (re.search('(#back)', text)):
        return False
    elif re.search(r'[\,\.\!\+\*\"\#\/\=\}\{\[\]\¨]', text):
        if re.search(r'\w', text):
            return False
        else:
            raise ValueError(
                '-> El texto debe contener letras ademas de caracteres especiales <-')


def sameMeaning(text, text_tralation):
    """
    Si el texto y la traducción son iguales, genera un error.

    :param text: El texto a traducir
    :param text_tralation: El texto traducido
    """

    if text == text_tralation:
        raise ValueError(
            '-> Traducion igual a texto de entrada, por favor revisar <-')


def translation():
    """
    Pide un idioma, luego pide un texto para traducir, luego traduce el texto y lo envía a un correo
    electrónico
    """

    acro_counter = True
    target_leng = ""
    while acro_counter == True:
        target_leng = input('Idioma objetivo -> ')
        if checkAcronyms(target_leng) == True:
            acro_counter = False
        else:
            acro_counter = True

    cicle = True
    while cicle != False:
        text = input('Texto a traducir -> ')
        try:
            numberInText(text)
            specialInText(text)
            if '#exit' in text:
                emailConn.closeConnection()
                quit()
            if '#back' not in text:
                text_tralation = translate(text, target_leng)
                sameMeaning(text, text_tralation)
                print(text_tralation)
                emailConn.sendEmail(text, text_tralation)
            else:
                cicle = False
                translation()
        except Exception as e:
            print(e)
