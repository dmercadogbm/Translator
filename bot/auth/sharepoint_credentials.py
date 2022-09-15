"""
Modulo para conectarse con sharepoint
Autor: Luis Vega
"""

# Importación de las bibliotecas que se necesitan para conectarse a SharePoint.
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from cryptography.fernet import Fernet
import os

BASE_URL = 'https://gbmcorp.sharepoint.com/sites/KnowledgeManagementSW/'
FOLDER_URL = '/sites/KnowledgeManagementSW/Documentos%20compartidos/DOCUMENTACION%20PROYECTOS/CREDENCIALES/'
FILE_NAME = "credenciales.txt"


class __Username:
    __USERNAME = "dmercado@gbm.net"
    __TOKEN = b'gAAAAABjIzIZ6F3wn4c7jGh-vbs4-hzt-EjY2ujDtSDEQU1Yb3Fm6tJerGc7UHvfv8-9gsHXFJhlONKuF-INBf-Pi_6A_zvHHQ=='  # encriptar
    __KEY = b'LdeUDN0E_-rUf2-NhAudpgTUc9cF-8dsC8jp93m9lPQ='

    @classmethod
    def get_username(cls):
        return cls.__USERNAME

    @classmethod
    def get_token(cls):
        return cls.__decrypt(cls.__TOKEN, cls.__KEY)

    @classmethod
    def encrypt(cls, pswd):
        key = Fernet.generate_key()
        encrypted_passwd = Fernet(key).encrypt(pswd.encode("UTF-8"))
        return encrypted_passwd, key

    @classmethod
    def __decrypt(cls, token: bytes, key: bytes):
        return Fernet(key).decrypt(token).decode("UTF-8")

    @classmethod
    def generate_key(cls):
        return Fernet.generate_key()

    @classmethod
    def __get_key(cls):
        return cls.__KEY


def verifier(func, credentials=None):
    """
    Decorador que toma una funcion como argumento y si las credenciales son validas se ejecuta la
    funcion original

    :param func: La función a ser decorada
    :return: Una función
    """
    psswrd_list = get_passwords_list()
    count = 0
    if credentials:
        verify = __isvalid(psswrd_list, credentials)
    else:
        verify = False

    def wrapper(*args, **kwargs):
        """
        Toma una función como argumento y devuelve una función que llamará a la función original si el
        usuario ha ingresado credenciales válidas
        :return: el resultado de la funcion original.
        """
        nonlocal verify
        nonlocal psswrd_list
        nonlocal count
        res = None
        if len(psswrd_list) > 0:
            while count < 3:
                count += 1
                if not verify:
                    password = input("Credenciales: ")
                    verify = __isvalid(psswrd_list, password)
                    if verify:
                        res = func(*args, **kwargs)
                        break
                    else:
                        print("Credenciales no validas")
            else:
                print("Numero maximo de intentos permitidos")
        return res

    return wrapper


def get_credentials(credentials: str) -> bool:
    """
    Toma como parametro un codigo de verificacion alfanumerico, se realiza una conexion
    REST con SharePoint y se accede a un archivo donde se almacenan los codigos de
    verificacion validos para el programa y si el codigo es valido devuelve True

    :param credentials: str
    :return: Un valor booleano
    """

    username = __Username.get_username()
    password = __Username.get_token()
    ctx_auth = AuthenticationContext(BASE_URL)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(BASE_URL, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ', web.properties['Title'])
            file_url_shrpt = FOLDER_URL + FILE_NAME
            response = File.open_binary(ctx, file_url_shrpt)
            passwords = response.content.decode("UTF-8").split("\r\n")
            if credentials in passwords:
                return True
    except Exception:
        print("Fallo al acceder a las credenciales")
    return False


def get_passwords_list():
    """
    Se realiza una conexion REST con SharePoint y se accede a un archivo donde
    se almacenan los codigos de verificacion validos para el programa.
    :return: Una lista de codigos validos
    """
    username = __Username.get_username()
    password = __Username.get_token()
    ctx_auth = AuthenticationContext(BASE_URL)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(BASE_URL, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ', web.properties['Title'])
            file_url_shrpt = FOLDER_URL + FILE_NAME
            response = File.open_binary(ctx, file_url_shrpt)
            credentials = response.content.decode("UTF-8").split("\r\n")
    except Exception:
        print("Fallo al acceder a las credenciales")
        credentials = []
    finally:
        return credentials


def upload_file(path_file, relative_path=""):
    """
    Toma una ruta de archivo y una ruta relativa opcional a una carpeta en SharePoint, y carga el
    archivo en esa carpeta.

    :param path_file: la ruta al archivo que desea cargar
    :param relative_path: la ruta a la carpeta en la que desea cargar
    :return: El archivo está creado en el sitio de Sharepoint.
    """

    username = __Username.get_username()
    password = __Username.get_token()
    ctx_auth = AuthenticationContext(BASE_URL)
    folder_path = FOLDER_URL + relative_path

    try:
        with open(path_file, "rb") as content_file:
            file_content = content_file.read()
        name = os.path.basename(path_file)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(BASE_URL, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()

            target_folder = ctx.web.get_folder_by_server_relative_url(
                folder_path)
            target_folder.upload_file(name, file_content).execute_query()
            return True
    except Exception as e:
        return False


def upload_folder(startpath):
    """
    Toma la ruta a una carpeta y luego carga todos los archivos y carpetas en esa
    carpeta a la carpeta base de SharePoint 

    :param startpath: La ruta a la carpeta que desea cargar
    """

    for root, dirs, files in os.walk(startpath):
        sub_path = root.replace(startpath, '')

        for dir in dirs:
            try:
                add_folder(dir, sub_path)
                print("CARPETA ", sub_path, "AÑADE SUBCARPETA: ", dir)
            except Exception as e:
                print(e)
        for f in files:
            try:
                print("CARPETA ", sub_path, " SUBE: ", f)
                file_path = root + "/" + f
                upload_file(file_path, sub_path)
            except Exception as e:
                print(e)


def add_folder(folder_name, relative_path=""):
    """
    Toma un nombre de carpeta y una ruta relativa a un sitio de SharePoint y crea una carpeta en la ruta
    relativa con el nombre de la carpeta

    :param folder_name: El nombre de la carpeta que desea crear
    :param relative_path: La ruta a la carpeta a la que desea agregar la nueva carpeta
    :return: El folder está creado en el sitio de Sharepoint.
    """

    username = __Username.get_username()
    password = __Username.get_token()
    ctx_auth = AuthenticationContext(BASE_URL)
    folder_path = FOLDER_URL + relative_path
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(BASE_URL, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            target_folder = ctx.web.get_folder_by_server_relative_url(
                folder_path).folders.add(folder_name)
            ctx.execute_query()
            return True
    except Exception as e:
        print("Fallo al acceder a las credenciales")
        print(e)
        return False


def __isvalid(passwords: list, pswd: str):
    """
    Devuelve True si la contraseña está en la lista de contraseñas y False en caso contrario

    :param passwords: lista de contraseñas
    :type passwords: list
    :param pswd: la contraseña para comprobar
    :type pswd: str
    :return: Un valor booleano.
    """
    return pswd in passwords
