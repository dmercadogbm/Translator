# Importación de las bibliotecas necesarias para enviar un correo electrónico.
import email.utils
import os
import smtplib
from email.mime.text import MIMEText

import auth.sharepoint_credentials as auth

# Creación de un objeto SMTP.
__mailserver = smtplib.SMTP('smtp.office365.com', 587)
# Obtener el nombre de usuario actual.
__user = os.getlogin()


def connection():
    """
    Se conecta al servidor e inicia sesión.
    """
    __mailserver.ehlo()
    __mailserver.starttls()
    __mailserver.login(auth.__Username.get_username(),
                       auth.__Username.get_token())


def sendEmail(text: str = None, text_translation: str =None):
    """
    Toma dos cadenas como argumentos y envía un correo electrónico al usuario con las dos cadenas como
    cuerpo del correo electrónico.
    
    :param text: str = Ninguno, traducción_texto: str = Ninguno
    :type text: str
    """
    msg = MIMEText('Base text:' + text + ' \n ' +
                   'Translated text:' + text_translation, _charset='UTF-8')
    msg['Subject'] = 'Translation succefully'
    msg['Message-ID'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate(localtime=1)
    msg['From'] = auth.__Username.get_username()
    msg['To'] = __user+"@gbm.net"
    __mailserver.sendmail(msg['From'], msg['To'], msg.as_string())


def closeConnection():
    """
    Cierra la conexión con el servidor de correo.
    """
    __mailserver.quit()
