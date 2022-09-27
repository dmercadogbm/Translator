# Importando las bibliotecas que se necesitan para que el programa funcione.
import os
import re
from datetime import datetime

from deep_translator import GoogleTranslator
#import connections.email_conn as emailConn
import scripts.excel as excelInfo


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


def translation():
    """
    Pide un idioma, luego pide un texto para traducir, luego traduce el texto y lo envía a un correo
    electrónico
    """
    try:
        now = datetime.now()
        dateYMD = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        dateYMDHMS = dateYMD + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        df = excelInfo.getTextPath(
            r'C:\Users\dmercado\OneDrive - GBM Corporacion\Documents\Test.xlsx')
        doc_name = "ACTION-"+dateYMD+".txt"

        print(df)

        for row in df.itertuples():
            name_compiler = re.compile(r'((\w+.txt)+)')
            name_compiled = name_compiler.search(row.TEXTO)
            name_compiled.group(1)

            before_path = row.TEXTO.split("\\")
            before_path.pop()
            translated_doc_path = "\\".join(before_path)

            with open("bot/log/action/"+doc_name, "a", encoding="utf-8") as action_file:
                with open(row.TEXTO, "r", encoding="utf-8") as text_file:
                    with open(translated_doc_path+"\\traducido-"+row.IDIOMA+"-"+name_compiled.group(1), "a", encoding="utf-8") as text_translation:
                        for line in text_file:
                            text_translation.write(
                                translate(line, row.IDIOMA)+"\n")
                    action_file.write(dateYMDHMS + " [ACTION] = TRANSLATE ")
                    action_file.write("\n")
            # sendEmail()
    except Exception as e:
        if e == "cehz --> No support for the provided language.":
            print("HOLAAAAAAAAAAAAAAA")
        error_doc_name = "ERROR-"
        with open("bot/log/error/"+error_doc_name, "a", encoding="utf-8") as error_file:
            error_file.write(dateYMDHMS + " [ERROR] = " + str(e))
            error_file.write("\n")
