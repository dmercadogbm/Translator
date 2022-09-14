# Importing the smtplib module.
import smtplib

# Creating a connection to the SMTP server.
mailserver = smtplib.SMTP('smtp.office365.com', 587)

def connection():
    """
    It connects to the mail server.
    """
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('dmercado@gbm.net', 'DaMeTa026#')

def sendEmail():
    """
    It sends an email to the address specified in the second argument, from the address specified in the
    first argument, with the subject specified in the third argument
    """
    mailserver.sendmail('dmercado@gbm.net', 'damttrabajos@gmail.com', 'Subject: Translation succefully  translate')

def closeConnection():
    """
    It closes the connection to the mail server
    """
    mailserver.quit()