from datetime import datetime

now = datetime.now()


def dateYMD() -> str:
    return (str(now.year) + "-" + str(now.month) + "-" + str(now.day))


def dateYMDHMS() -> str:
    return (dateYMD() + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
