import pandas


def getTextPath(path):
    df = pandas.read_excel(path, index_col=False)
    df = df[df['TEXTO'].notna()]
    print(df)
    data = {item[1]: item[2] for item in df.itertuples()}
    return data
