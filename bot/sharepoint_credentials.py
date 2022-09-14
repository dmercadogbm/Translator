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
        i = 0
        while i < 3 :
            if not verify :
                password = input("Credenciales: ")
                verify = getcredentials(password)
                if verify :
                    res=func(*args,**kwargs)
                else:
                    i = i + 1
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
    folder_url = '/sites/KnowledgeManagementSW/Documentos%20compartidos/DOCUMENTACION%20PROYECTOS/CREDENCIALES/credenciales.txt'
    ctx_auth = AuthenticationContext(url)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            print('Authenticated into sharepoint: ',web.properties['Title'])
            response = File.open_binary(ctx, folder_url)
            passwords = response.content.decode("UTF-8").split("\r\n")
            if credentials in passwords:
                return True
    except Exception as e:
        print("Fallo al acceder a las credenciales")
    return False
