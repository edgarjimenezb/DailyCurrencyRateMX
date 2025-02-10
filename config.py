from os import path, getcwd
from configparser import SafeConfigParser

class Config(object):
    """Clase para obtener las configuraciones de la aplicación"""
    ARCHIVO_CONFIG = 'config.ini'

    def obtiene_config(self, section):
        """Obtiene la configuración del archivo INI\nRecibe la sección a extraer\nRegresa un diccionario con las claves"""
        parser = SafeConfigParser()
        parser.read(path.join(path.abspath(path.dirname(__file__)), self.ARCHIVO_CONFIG))
        new_dict = {}
        options = parser.options(section)
        for option in options:
            try:
                new_dict[option] = parser.get(section, option)
            except Exception:
                new_dict[option] = None
        return dict

    def obtiene_config_log(self):
        """Obtiene la configuración del Log de la aplicación del archivo INI\nRegresa un diccionario con las configuraciones"""
        log_file = self.obtiene_config('LogFile')
        ruta = log_file.get('path', getcwd() + '\\')
        if not path.exists(ruta):
            del log_file['path']
            log_file['path'] = getcwd() + '\\'
        return log_file

    def obtiene_config_basedatos(self):
        """Obtiene la configuración de la base de datos del archivo INI de la aplicación\nRegresa una tupla con los parámetros de conexión a la base de datos"""
        basedatos = self.obtiene_config('DataBase')
        driver = basedatos['driver']
        server = basedatos['server']
        initialcatalog = basedatos['initialcatalog']
        user = basedatos['user']
        password = basedatos['password']

        return (driver, server, initialcatalog, user, password)

    def obtiene_config_email(self):
        email = self.obtiene_config('Email')
        return email
