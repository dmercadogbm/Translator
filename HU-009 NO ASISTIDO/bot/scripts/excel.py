import pandas
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as codes
from connections import setting_conn as sett


def getTextPath(path):
    df = pandas.read_excel(path, index_col=False)
    df = df[df['TEXTO'].notna()]
    df = df[df['IDIOMA'].notna()]
    for item_index, item in df['IDIOMA'].items():
        if str(item).lower() in codes.values() or str(item).lower() in codes.keys():
            pass
        else:
            sett.sendErrorEmail("lenguaje_error")
            df.drop(index=item_index, inplace=True)
    df2 = df[df["TEXTO"].str.endswith(".txt")]
    for index_item, item in df["TEXTO"].str.endswith(".txt").items():
        if item == False:
            sett.sendErrorEmail("extension_error")
    print(df2)
    data = {item[1]: item[2] for item in df2.itertuples()}
    return data
