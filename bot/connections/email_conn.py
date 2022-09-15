# Importing the email.utils module.
import email.utils
# Importing the os module.
import os
# Importing the smtplib module.
import smtplib
# Importing the MIMEText class from the email.mime.text module.
from email.mime.text import MIMEText

import auth.sharepoint_credentials as auth
# Creating a connection to the SMTP server.
__mailserver = smtplib.SMTP('smtp.office365.com', 587)
# Getting the current user name.
__user = os.getlogin()


def connection():
    __mailserver.ehlo()
    __mailserver.starttls()
    __mailserver.login(auth.__Username.get_username(),
                       auth.__Username.get_token())


def sendEmail(text: str = None, text_translation=None):
    """
    It takes two strings as arguments, and sends an email with the two strings as the body of the email
    
    :param text: str = None, text_translation=None
    :type text: str
    :param text_translation: The translated text
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
    It closes the connection to the mail server
    """
    __mailserver.quit()
