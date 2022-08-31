from deep_translator import GoogleTranslator
from colorama import Fore
import os


def translate(text: str, target_leng: str, source_leng: str) -> str:
    translator = GoogleTranslator(
        source=source_leng, target=target_leng)
    result = translator.translate(text)
    return (result)


def translateProcess(input_lenguage: str, output_lenguage: str):
    while True:
        text = input('text: ')
        if 'xx' not in text:
            print(translate(text, output_lenguage, input_lenguage))
        else:
            break

if __name__ == '__main__':
    os.system('cls')
    spanish = input(
        Fore.BLUE + "Desea continuar con Español como lenguaje base? / Do you want to continue with Spanish as base lenguaje?\nYes / No : ").lower()
    input_lenguage=input(
        Fore.BLUE + "Acronimo del lenguaje de entrada / output language acronym : ")
    output_lenguage=input(
        Fore.BLUE + "Acronimo del lenguaje de salida / output language acronym : ")
    print(type(input_lenguage))
    translateProcess(output_lenguage=output_lenguage) if spanish == 'yes' else translateProcess(input_lenguage, output_lenguage)


# tradu = trans.translate('お腹', dest='es')
