import configparser
from os import mkdir
from pathlib import Path
from sys import excepthook
from scripts.date import dateYMDHMS, dateYMD


def getProjectRootPath():
    return str(Path(__file__).parent.parent) + "\\"


config_reader = configparser.ConfigParser()

config_reader.read(getProjectRootPath()+'auth\\settings.ini')

doc_name = "ACTION-"+dateYMD()+".log"

error_doc_name = "ERROR-"+dateYMD()+".log"


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

def getParentFolderPath(path:str):
    return str(Path(path).parent) + "\\"

def setErrorMessage(message):
    with open(getActionPath()+doc_name, "a", encoding="utf-8") as action_file:
        with open(getErrorPath()+error_doc_name, "a", encoding="utf-8") as error_file:
            action_file.write(
                dateYMDHMS() + " [ACTION] = ERROR " + str(message))
            action_file.write("\n")
            error_file.write(dateYMDHMS() + " [ERROR] = " + str(message))
            error_file.write("\n")


