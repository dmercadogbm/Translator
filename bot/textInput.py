# Importing the slackConn module.
import slackConn
# Importing the requests module.
import requests
# Importing the regular expression module.
import re

# Importing the GoogleTranslator class from the deep_translator module.
from deep_translator import GoogleTranslator
# Importing the dictionary GOOGLE_LANGUAGES_TO_CODES from the constants file.
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
    return (translator.translate(text))


def checkAcronyms(target_leng: str) -> bool:
    """
    If the target language is in the values of the dictionary, or if the target language is in the keys
    of the dictionary, then return True. Otherwise, return False

    :param target_leng: str = The language you want to translate to
    :type target_leng: str
    :return: A boolean value.
    """
    if target_leng in GOOGLE_LANGUAGES_TO_CODES.values():
        return True
    elif target_leng in GOOGLE_LANGUAGES_TO_CODES.keys():
        return True
    else:
        return False


def numberInText(text):
    """
    If the text is all numbers, raise a ValueError

    :param text: The text to be checked
    """
    if text.isnumeric():
        raise ValueError(
            '-> Text must have at least one letter not just numbers<-')


def specialInText(text):
    """
    If the text contains the words #exit or #back, return False. 

    If the text contains any of the following special characters: , . ! + * " # / = } { [ ] ¨, and if
    the text contains at least one letter, return False. 

    If the text contains any of the following special characters: , . ! + * " # / = } { [ ] ¨, and if
    the text does not contain at least one letter, raise a ValueError.

    :param text: The text to be analyzed
    :return: the text that is being passed to it.
    """
    if (re.search('(#exit)', text)) or (re.search('(#back)', text)):
        return False
    elif re.search(r'[\,\.\!\+\*\"\#\/\=\}\{\[\]\¨]', text):
        if re.search(r'\w', text):
            return False
        else:
            raise ValueError(
                '-> Text must have at least one letter not just special characters <-')


def sameMeaning(text, text_tralation):
    """
    If the text and the translation are the same, raise a ValueError

    :param text: The text to be translated
    :param text_tralation: The text that you want to translate
    """
    if text == text_tralation:
        raise ValueError('-> Translation is it the same please verify text <-')


def translation():
    """
    It takes a string as input, and if the string is not '#exit' or '#back', it will translate the
    string to the language specified by the user, and print the translation
    """
    acro_counter = True
    target_leng = ""
    while acro_counter == True:
        target_leng = input('Target language -> ').lower()
        if checkAcronyms(target_leng) == True:
            acro_counter = False
        else:
            acro_counter = True

    cicle = True
    while cicle != False:
        text = input('Text to translate -> ')
        try:
            numberInText(text)
            specialInText(text)
            if '#exit' in text:
                quit()
            if '#back' not in text:
                text_tralation = translate(text, target_leng)
                sameMeaning(text, text_tralation)
                print(text_tralation)
                slack = slackConn.connection()
                requests.post(slack[0], json={'text': slack[1]})
            else:
                cicle = False
                translation()
        except Exception as e:
            print(e)
