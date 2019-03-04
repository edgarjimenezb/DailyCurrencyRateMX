# -*- coding: utf-8 -*-

from datetime import datetime
from time import strftime
from pyodbc import connect
from config import Config
import logger

log = logger.getLogger()

class BaseDatos(object):
    """Clase de acceso a datos"""

    @classmethod
    def conecta(cls):
        """Conecta a la base de datos de pruebas\nRegresa un objeto con la conexión"""
        try:
            configuracion = Config.obtiene_config_basedatos()
            conn = connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % configuracion)
            return conn
        except BaseException as ex:
            log.error("Error al conectar a base de datos: %s", ex)
            raise
    
    @classmethod
    def existe_tipo_cambio(cls, moneda, fecha):
        """Consulta el tipo de cambio del día en la base de datos\nRecibe la conexión a BD, la moneda y la fecha a consultar\nRegresa el número de registros coincidentes"""
        try:
            conn = cls.conecta()
            cursor = conn.cursor()
            cadena_select = """SELECT COUNT(TIPO_CAMBIO_MXN)
            FROM [dbo].[TipoCambioMonedas]
            WHERE CODIGO =? AND FECHA_PUBLICACION =? AND Activo = 1"""
            params = [moneda, fecha]
            cursor.execute(cadena_select, params)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result == None:
                return 0
            else:
                return result[0]
        except Exception as ex:
            log.error("Error al consultar el tipo de cambio en base de datos: %s", ex)
            raise

    @classmethod
    def inserta_tipo_cambio(cls, fecha_publicacion, fecha_aplicacion, tipo_cambio, moneda):
        """Inserta el nuevo tipo de cambio del día en la base de datos\nRecibe la conexión a BD, la fecha, los días de vigencia, el valor del nuevo tipo de cambio y la moneda\nRegresa el número de registros insertados"""
        try:
            conn = cls.conecta()
            cursor = conn.cursor()
            cadena_insert = """INSERT INTO [dbo].[TipoCambioMonedas]
                            (CODIGO, FECHA_PUBLICACION, FECHA_APLICACION, TIPO_CAMBIO_USD, TIPO_CAMBIO_MXN, ACTIVO)
                            VALUES (?, ?, ?, ?, ?, ?)"""
            params = [moneda, fecha_publicacion, fecha_aplicacion, 1, tipo_cambio, 1]
            cursor.execute(cadena_insert, params)
            conn.commit()
            log.info("Se inserta el tipo de cambio: Moneda '%s', Tipo de cambio '%s' del día '%s'", moneda, tipo_cambio, fecha_aplicacion)
            cursor.close()
            conn.close()
            return True
        except Exception as ex:
            log.error("Error al insertar el tipo de cambio en base de datos: %s", ex)
            raise