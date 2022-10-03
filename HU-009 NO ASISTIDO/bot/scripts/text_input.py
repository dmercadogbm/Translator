from deep_translator import GoogleTranslator
import scripts.excel as excelInfo
from connections import setting_conn


def translate(text: str, target_leng: str) -> str:
    translator = GoogleTranslator(
        source='auto', target=target_leng)
    return (translator.translate(text))


def translation():
    try:
        data = excelInfo.getTextPath(setting_conn.getExcelPath())
        setting_conn.setAccionMessage(data)
        setting_conn.sendEndEmail()
    except:
        setting_conn.sendErrorEmail("error_message")
