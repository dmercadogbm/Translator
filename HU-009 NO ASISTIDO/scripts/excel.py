import pandas


def getTextPath(path):
    df = pandas.read_excel(path, index_col=False)
    return df
