import configparser
from os import mkdir
from pathlib import Path
import re

from scripts.text_input import translate
from scripts.date import dateYMDHMS, dateYMD

from connections.email_conn import sendEmail


def getProjectRootPath():
    return str(Path(__file__).parent.parent) + "\\"


config_reader = configparser.ConfigParser(interpolation=None)

config_reader.read(getProjectRootPath()+'auth\\settings.ini')

doc_name = "ACTION-"+dateYMD()+".log"

error_doc_name = "ERROR-"+dateYMD()+".log"


def getCredentials() -> str:
    credential = config_reader["SharepointCredentials"]["credentials"]
    return credential


def setLogFolder() -> str:
    try:
        mkdir(getProjectRootPath()+"log")
    except:
        pass


def setDailyFolder() -> str:
    try:
        mkdir(Path(getProjectRootPath()).joinpath(f'log\\{dateYMD()}\\'))
    except:
        pass


def getActionPath() -> str:
    return str(getProjectRootPath()+f'log\\{dateYMD()}\\')


def getErrorPath() -> str:
    return str(getProjectRootPath()+f'log\\{dateYMD()}\\')


def getExcelPath():
    info = config_reader.items("FilesPath")
    return info[0][1]


def getParentFolderPath(path: str):
    return str(Path(path).parent) + "\\"


def getSettingsStartStatus() -> str:
    return (config_reader["NotificationsStatus"]["start_status"])


def getSettingsEndStatus() -> str:
    return (config_reader["NotificationsStatus"]["end_status"])


def getSettingsTransactionStatus() -> str:
    return (config_reader["NotificationsStatus"]["transaction_status"])


def getSettingsErrorStatus() -> str:
    return (config_reader["NotificationsStatus"]["error_status"])


def getSettingsStartMessage() -> str:
    return (config_reader["NotificationsMessages"]["start_message"])


def getSettingsEndMessage() -> str:
    return (config_reader["NotificationsMessages"]["end_message"])


def getSettingsTransactionMessage() -> str:
    return (config_reader["NotificationsMessages"]["transaction_message"])


def getSettingsErrorMessage() -> str:
    return (config_reader["NotificationsMessages"]["error_message"])


def sendStartEmail() -> None:
    if getSettingsStartStatus() == "True":
        body_message = config_reader["NotificationsMessages"]["start_bodymessage"]
        sendEmail(getSettingsStartMessage(), body_message)


def sendTransactionEmail(file_name: str) -> None:
    if getSettingsTransactionStatus() == "True":
        sendEmail(getSettingsTransactionMessage(), "documento : " + file_name)

def setErrorMessage(error_type: str) -> None:
    with open(getActionPath()+doc_name, "a", encoding="utf-8") as action_file:
        with open(getErrorPath()+error_doc_name, "a", encoding="utf-8") as error_file:
            action_file.write(
                str(dateYMDHMS()) + " [ACTION] = ERROR " + str(error_type))
            action_file.write("\n")
            error_file.write(
                str(dateYMDHMS()) + " [ERROR] = " + str(error_type))
            error_file.write("\n")    

def sendErrorEmail(error_type: str) -> None:
    error_message = ""
    if error_type == "extension_error":
        error_message = config_reader["NotificationsMessages"]["extension_error"]
    elif error_type == "lenguaje_error":
        error_message = config_reader["NotificationsMessages"]["lenguaje_error"]
    else:
        error_message = config_reader["NotificationsMessages"]["error_message"]
    setErrorMessage(str(error_message))

    if getSettingsErrorStatus() == "True":
        sendEmail(getSettingsErrorMessage(), error_message)


def sendEndEmail() -> None:
    if getSettingsEndStatus() == "True":
        body_message = config_reader["NotificationsMessages"]["end_bodymessage"]
        sendEmail(getSettingsEndMessage(), body_message)


def setAccionMessage(data) -> None:

    for idioma, path in data.items():
        tranlated_path = getParentFolderPath(path)
        name_compiler = re.compile(r'((\w+.txt)+)')
        name_compiled = name_compiler.search(path)
        file_name = name_compiled.group(1)
        tranlated_file_name = tranlated_path+idioma.upper()+"_"+file_name
        with open(getActionPath()+doc_name, "a", encoding="utf-8") as action_file:
            with open(path, "r", encoding="utf-8") as text_file:
                with open(tranlated_file_name, "a", encoding="utf-8") as text_translation:
                    for line in text_file:
                        text_translation.write(
                            translate(line, idioma)+"\n")
                    action_file.write(
                        dateYMDHMS() + " [ACTION] = TRANSLATE " + file_name + " TO " + idioma)
                    action_file.write("\n")
                sendTransactionEmail(str(file_name))
