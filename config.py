from os import path, getcwd
from configparser import SafeConfigParser

class Config(object):
    """Clase para obtener las configuraciones de la aplicación"""
    ARCHIVO_CONFIG = 'config.ini'

    def obtiene_config(self, section):
        """Obtiene la configuración del archivo INI\nRecibe la sección a extraer\nRegresa un diccionario con las claves"""
        try:
            parser = SafeConfigParser()
            parser.read(path.join(path.abspath(path.dirname(__file__)), self.ARCHIVO_CONFIG))
            dict = {}
            options = parser.options(section)
            for option in options:
                try:
                    dict[option] = parser.get(section, option)
                except Exception:
                    dict[option] = None
            return dict
        except Exception as ex:
            raise


    def obtiene_config_log(self):
        """Obtiene la configuración del Log de la aplicación del archivo INI\nRegresa un diccionario con las configuraciones"""
        try:
            logFile = self.obtiene_config('LogFile')
            ruta = logFile.get('path', getcwd() + '\\')
            if not path.exists(ruta):
                del logFile['path']
                logFile['path'] = getcwd() + '\\'
            return logFile
        except Exception as ex:
            raise

    def obtiene_config_basedatos(self):
        """Obtiene la configuración de la base de datos del archivo INI de la aplicación\nRegresa una tupla con los parámetros de conexión a la base de datos"""
        try:
            basedatos = self.obtiene_config('DataBase')
            driver = basedatos['driver']
            server = basedatos['server']
            initialcatalog = basedatos['initialcatalog']
            user = basedatos['user']
            password = basedatos['password']

            return (driver, server, initialcatalog, user, password)
        except Exception as ex:
            raise

    def obtiene_config_email(self):
        try:
            email = self.obtiene_config('Email')
            return email
        except Exception as ex:
            raise
