from datetime import datetime

now = datetime.now()
doc_name = "ERROR " + str(now.year) + "-" + str(now.month) + "-" + str(now.day)
with open("log/error/"+doc_name, "a", encoding = "utf-8") as action_file:
    action_file.write('hola\n')