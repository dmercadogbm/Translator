# Importing the smtplib module.
import os
import smtplib
from email.mime.text import MIMEText
import email.utils

# Creating a connection to the SMTP server.
__mailserver = smtplib.SMTP('smtp.office365.com', 587)
__user = os.getlogin()

def connection():
    """
    It connects to the mail server.
    """
    __mailserver.ehlo()
    __mailserver.starttls()
    __mailserver.login('dmercado@gbm.net', 'DaMeTa026#')

def sendEmail(text :str= None, text_translation = None):
    """
    It sends an email to the address specified in the second argument, from the address specified in the
    first argument, with the subject specified in the third argument
    """
    msg = MIMEText('Base text:' + text + ' \n ' + ' Translated text:' + text_translation, _charset='UTF-8')
    msg['Subject'] = 'Translation succefully'
    msg['Message-ID'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate(localtime=1)
    msg['From'] = "dmercado@gbm.net"
    msg['To'] = __user+"@gbm.net"
    
    __mailserver.sendmail(msg['From'], msg['To'], msg.as_string())

def closeConnection():
    """
    It closes the connection to the mail server
    """
    __mailserver.quit()