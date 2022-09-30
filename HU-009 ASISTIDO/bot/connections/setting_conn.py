import configparser
from os import mkdir
from pathlib import Path
from scripts.date import dateYMDHMS, dateYMD
from connections.email_conn import sendEmail


def getProjectRootPath():
    return str(Path(__file__).parent.parent) + "\\"


config_reader = configparser.ConfigParser()

config_reader.read(getProjectRootPath()+'auth\\settings.ini')

doc_name = "ACTION-"+dateYMD()+".log"

error_doc_name = "ERROR-"+dateYMD()+".log"

def setLogFolder():
    try:
        mkdir(getProjectRootPath()+"log")
    except:
        pass

def setDailyFolder():
    try:
        mkdir(Path(getProjectRootPath()).joinpath(f'log\\{dateYMD()}\\'))
    except:
        pass


def getActionPath():
    return str(getProjectRootPath()+f'log\\{dateYMD()}\\')


def getErrorPath():
    return str(getProjectRootPath()+f'log\\{dateYMD()}\\')


def getExcelPath():
    info = config_reader.items("FilesPath")
    return info[0][1]


def getParentFolderPath(path: str):
    return str(Path(path).parent) + "\\"


def getSettingsStartStatus():
    return (config_reader["NotificationsStatus"]["start_status"])


def getSettingsEndStatus():
    return (config_reader["NotificationsStatus"]["end_status"])


def getSettingsTransactionStatus():
    return (config_reader["NotificationsStatus"]["transaction_status"])


def getSettingsErrorStatus():
    return (config_reader["NotificationsStatus"]["error_status"])


def getSettingsStartMessage():
    return (config_reader["NotificationsMessages"]["start_message"])


def getSettingsEndMessage():
    return (config_reader["NotificationsMessages"]["end_message"])


def getSettingsTransactionMessage():
    return (config_reader["NotificationsMessages"]["transaction_message"])


def getSettingsErrorMessage():
    return (config_reader["NotificationsMessages"]["error_message"])


def sendStartEmail() -> None:
    if getSettingsStartStatus() == "True":
        sendEmail(getSettingsStartMessage(), config_reader["NotificationsMessages"]["start_bodymessage"])


def sendErrorEmail(error: str):
    if getSettingsErrorStatus() == "True":
        sendEmail(getSettingsErrorMessage(), error)


def sendEndEmail():
    if getSettingsEndStatus() == "True":
        sendEmail(getSettingsEndMessage(), config_reader["NotificationsMessages"]["end_bodymessage"])


def sendTransactionEmail(text, text_tralation):
    if getSettingsTransactionStatus() == "True":
        sendEmail(getSettingsTransactionMessage(), 'Base text:' + text + ' \n ' +'Translated text:' + text_tralation)


def setErrorMessage(message):
    with open(getActionPath()+doc_name, "a", encoding="utf-8") as action_file:
        with open(getErrorPath()+error_doc_name, "a", encoding="utf-8") as error_file:
            action_file.write(
                dateYMDHMS() + " [ACTION] = ERROR " + str(message))
            action_file.write("\n")
            error_file.write(dateYMDHMS() + " [ERROR] = " + str(message))
            error_file.write("\n")
