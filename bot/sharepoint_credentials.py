# Importación de las bibliotecas que se necesitan para conectarse a SharePoint.
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

class Username:
    __USERNAME__ = "dmercado@gbm.net"
    __PASSWORD__ = "DaMeTa026#"

    @classmethod
    def get_USERNAME(cls):
        return cls.__USERNAME__

    @classmethod
    def get_PASSWORD(cls):
        return cls.__PASSWORD__

def verifier(func, credentials=None):
    """
    Decorador que toma una funcion como argumento y si las credenciales son validas se ejecuta la
    funcion original

    :param func: La función a ser decorada
    :return: Una función
    """
    if credentials:
        verify = getcredentials(credentials)
    else:
        verify = False
    def wrapper(*args,**kwargs):
        """
        Toma una función como argumento y devuelve una función que llamará a la función original si el
        usuario ha ingresado credenciales válidas
        :return: el resultado de la funcion original.
        """
        nonlocal verify
        res = None
        if not verify :
            password = input("Credenciales: ")
            verify = getcredentials(password)
            if verify :
                res=func(*args,**kwargs)
            else:
                print("Credenciales no validas")
        else:
            pass
        return res

    return wrapper

def getcredentials(credentials:str) -> bool:
    """
    Toma como parametro un codigo de verificacion alfanumerico, se realiza una conexion REST con SharePoint
    y se accede a un archivo donde se almacenan los codigos de verificacion validos para el programa
    Si el codigo es valido devuelve True

    :param credentials: calle
    :type credentials: str
    :return: Un valor booleano
    """

    url = 'https://gbmcorp.sharepoint.com/sites/KnowledgeManagementSW/' 
    username = Username.get_USERNAME()
    password = Username.get_PASSWORD()
    folder_url = '/sites/KnowledgeManagementSW/Documentos%20Compartidos/DOCUMENTACION%20INTERNA/PRACTICANTES/GBM2GROW-BAQ-G2-2022/Daniel%20Mercado/Proyecto/'
    ctx_auth = AuthenticationContext(url)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ',web.properties['Title'])
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

            file_url_shrpt = folder_url +'credentials.txt'
            response = File.open_binary(ctx, file_url_shrpt)
            passwords = response.content.decode("UTF-8").split("\r\n")
            if credentials in passwords:
                return True
    except Exception as e:
        print("Fallo al acceder a las credenciales")
    return False
