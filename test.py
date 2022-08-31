from deep_translator import GoogleTranslator
import os


def translate(text: str, target_leng: str) -> str:
    translator = GoogleTranslator(
        source='auto', target=target_leng)
    result = translator.translate(text)
    return (result)


def translateProcess(output_lenguage: str):
    while True:
        text = input('text:')
        if 'xx' not in text:
            print(translate(text, output_lenguage))
        else:
            break


if __name__ == '__main__':
    os.system('cls')
    output_lenguage = input("Acronimo del lenguaje de salida / output language acronym:")
    translateProcess(output_lenguage)


# tradu = trans.translate('お腹', dest='es')
