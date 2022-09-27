"""
Modulo para conectarse con sharepoint
Autor: Luis Vega
"""

# Importación de las bibliotecas que se necesitan para conectarse a SharePoint.
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from cryptography.fernet import Fernet
import pathlib
import os
import configparser


class Username:

    def __init__(self, email, token:bytes, key:bytes) -> None:
        self.email = email
        self.token = token
        self.key = key

    def get_username(self):
        return self.email

    def get_token(self):
        return self.__decrypt()

    def encrypt(cls, pswd):
        key = Fernet.generate_key()
        encrypted_passwd = Fernet(key).encrypt(pswd.encode("UTF-8"))
        return encrypted_passwd, key

    def __decrypt(self):
        return Fernet(self.key).decrypt(self.token).decode("UTF-8")

    def generate_key(self):
        pswd = self.__decrypt()
        self.token, self.key = self.encrypt(pswd)

    def __get_key(self):
        return self.key


def init_settings():
        
        def parse_url(plain_url:str):
            return plain_url.replace(" ","%20")
        script_path = str(pathlib.Path(__file__).parent.resolve()) + "/"
        configs = configparser.ConfigParser()
        configs.read(script_path+"settings.ini")
        base_url = parse_url(configs["SharepointCredentials"]["base_url"])
        folder_url = parse_url(configs["SharepointCredentials"]["folder_url"])
        file_name = configs["SharepointCredentials"]["file_name"]
        user = configs["Username"]["email"]
        token = configs["Username"]["token"].encode("UTF-8")
        key = configs["Username"]["key"].encode("UTF-8")
        username = Username(user, token, key)
        return base_url, folder_url, file_name, username


base_url, folder_url, file_name, sharepoint_auth = init_settings()


def verifier(func, credentials=None):
    """
    Decorador que toma una funcion como argumento y si las credenciales son validas se ejecuta la
    funcion original

    :param func: La función a ser decorada
    :param credentials: Si se quiere mandar como argumento las credenciales
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
            while count < 5:
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
        else:
            print("Finalizando ejecución...")
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

    username = sharepoint_auth.get_username()
    password = sharepoint_auth.get_token()
    ctx_auth = AuthenticationContext(base_url)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(base_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ', web.properties['Title'])
            # try:
            #     folder = ctx.web.get_folder_by_server_relative_url(folder_url)
            #     fold_names = []
            #     sub_folders = folder.files #Replace files with folders for getting list of folders
            #     ctx.load(sub_folders)
            #     ctx.execute_query()

            #     for s_folder in sub_folders:
            #         fold_names.append(s_folder.properties["Name"])
            # except Exception as e:
            #     print('Problem printing out library contents: ', e)

            file_url_shrpt = folder_url + file_name
            response = File.open_binary(ctx, file_url_shrpt)
            passwords = response.content.decode("UTF-8").split("\r\n")
            if credentials in passwords:
                return True
    except Exception:
        print("Fallo al acceder a las credenciales")


def get_passwords_list():
    """
    Se realiza una conexion REST con SharePoint y se accede a un archivo donde
    se almacenan los codigos de verificacion validos para el programa.
    :return: Una lista de codigos validos
    """
    username = sharepoint_auth.get_username()
    password = sharepoint_auth.get_token()
    credentials = []
    try:
        ctx_auth = AuthenticationContext(base_url)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(base_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ', web.properties['Title'])
            file_url_shrpt = folder_url + file_name
            response = File.open_binary(ctx, file_url_shrpt)
            credentials = response.content.decode("UTF-8").split("\r\n")
    except Exception:
        print("Fallo al acceder a las credenciales")
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

    username = sharepoint_auth.get_username()
    password = sharepoint_auth.get_token()
    ctx_auth = AuthenticationContext(base_url)
    folder_path = folder_url + relative_path

    try:
        with open(path_file, "rb") as content_file:
            file_content = content_file.read()
        name = os.path.basename(path_file)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(base_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()

            target_folder = ctx.web.get_folder_by_server_relative_url(folder_path)
            target_folder.upload_file(name, file_content).execute_query()
            return True
    except Exception:
        print("Fallo al acceder a las credenciales")


def upload_folder(startpath):
    """
    Toma la ruta a una carpeta y luego carga todos los archivos y carpetas en esa
    carpeta a la carpeta base de SharePoint 
    
    :param startpath: La ruta a la carpeta que desea cargar
    """
    root_folder = os.path.basename(startpath)
    add_folder(root_folder)
    for root, dirs, files in os.walk(startpath):
        sub_path = root.replace(startpath, '')
        sub_path = "\\"+root_folder + sub_path
        for folder in dirs:
            try:
                add_folder(folder, sub_path)
                print("CARPETA ", sub_path, "AÑADE SUBCARPETA: ", folder)
            except Exception as e:
                print(e)
        for f in files:
            try:
                print("CARPETA ", sub_path, " SUBE: ", f)
                file_path = root + "/" + f
                upload_file(file_path, sub_path)
            except Exception:
                print("Fallo al acceder a las credenciales")


def add_folder(folder_name, relative_path=""):
    """
    Toma un nombre de carpeta y una ruta relativa a un sitio de SharePoint y crea una carpeta en la ruta
    relativa con el nombre de la carpeta
    
    :param folder_name: El nombre de la carpeta que desea crear
    :param relative_path: La ruta a la carpeta a la que desea agregar la nueva carpeta
    :return: El folder está creado en el sitio de Sharepoint.
    """

    username = sharepoint_auth.get_username()
    password = sharepoint_auth.get_token()
    ctx_auth = AuthenticationContext(base_url)
    folder_path = folder_url + relative_path
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(base_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            ctx.web.get_folder_by_server_relative_url(folder_path).folders.add(folder_name)
            ctx.execute_query()
            return True
    except Exception:
        print("Fallo al acceder a las credenciales")


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
