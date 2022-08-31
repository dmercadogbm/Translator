from deep_translator import GoogleTranslator

def translate(text: str, to : str):
    translator = GoogleTranslator(source = 'es', target=to)
    result = translator.translate(text)
    print(result)
# tradu = trans.translate('お腹', dest='es')

if __name__ == '__main__':
    while True:
        texto = input('texto: ')
        if 'xxx' not in texto :
            destino = input('destino: ')
        else:
            break
        translate(texto,destino)


