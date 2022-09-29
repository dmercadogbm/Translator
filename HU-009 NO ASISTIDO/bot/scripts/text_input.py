# Importando las bibliotecas que se necesitan para que el programa funcione.
import os
import re
from datetime import datetime
from typing import Set
from connections.email_conn import sendEmail
from deep_translator import GoogleTranslator
#import connections.email_conn as emailConn
import scripts.excel as excelInfo
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from scripts.date import dateYMDHMS, dateYMD
from connections import setting_conn


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


def checkAcronyms(target_leng: str) -> None:

    if not target_leng in GOOGLE_LANGUAGES_TO_CODES.values() or not target_leng in GOOGLE_LANGUAGES_TO_CODES.keys():
        raise ValueError("Idioma no soportado")


def translation():
    """
    Pide un idioma, luego pide un texto para traducir, luego traduce el texto y lo envía a un correo
    electrónico
    """
    setting_conn.setDailyFolder()
    try:
        data = excelInfo.getTextPath(setting_conn.getExcelPath())

        for idioma, path in data.items():
            tranlated_path = setting_conn.getParentFolderPath(path)
            name_compiler = re.compile(r'((\w+.txt)+)')
            name_compiled = name_compiler.search(path)
            if idioma in GOOGLE_LANGUAGES_TO_CODES.values() or idioma in GOOGLE_LANGUAGES_TO_CODES.keys():
                with open(setting_conn.getActionPath()+setting_conn.doc_name, "a", encoding="utf-8") as action_file:
                    if not name_compiled == None:
                        if name_compiled.group(1).endswith(".txt"):
                            with open(path, "r", encoding="utf-8") as text_file:
                                with open(tranlated_path+idioma.upper()+"_"+name_compiled.group(1), "a", encoding="utf-8") as text_translation:
                                    for line in text_file:
                                        text_translation.write(
                                            translate(line, idioma)+"\n")
                                    action_file.write(dateYMDHMS(
                                    ) + " [ACTION] = TRANSLATE " + name_compiled.group(1) + " TO " + idioma)
                                    action_file.write("\n")
                                setting_conn.sendTransactionEmail(
                                    str(name_compiled.group(1)))
                        else:
                            setting_conn.setErrorMessage(
                                setting_conn.getSettingsErrorMessage())
                            setting_conn.sendErrorEmail(
                                "Archivo con extension invalida")
                    else:
                        setting_conn.setErrorMessage(
                            setting_conn.getSettingsErrorMessage())
                        setting_conn.sendErrorEmail("Archivo No encontrado")
            else:
                setting_conn.setErrorMessage(
                    setting_conn.getSettingsErrorMessage())
                setting_conn.sendErrorEmail("Idioma No soportado")
        setting_conn.sendEndEmail()
    except Exception as e:
        setting_conn.setErrorMessage(e)
        if setting_conn.getSettingsErrorStatus() == "True":
            sendEmail(setting_conn.getSettingsErrorMessage(), str(e))
