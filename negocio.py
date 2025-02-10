# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from time import strptime, strftime
from bs4 import BeautifulSoup
import logger

log = logger.getLogger()

class LogicaNegocio(object):
    """Clase de lógica de negocio"""
    FORMATO_FECHA_MX = "%d/%m/%Y"
    FORMATO_FECHA_ISO = "%Y-%m-%d"
    DICCIONARIO_MONEDAS = {'TDSF43718':"USD", 'DATOSF46410':"EUR", 'DATOSF46406':"JPY", 'DATOSF60632':"CAD"}
    DICCIONARIO_FECHAS = {'USD': "FECHASF43718", 'EUR': 'FECHADIVISAS', 'JPY': "FECHADIVISAS", 'CAD': "FECHADIVISAS"}

    @staticmethod
    def formato_cadena_numero(cadena):
        """Obtiene de una cadena el número que se encuentre en ella\nRecibe como parámetro un String y regresa un objeto float"""
        for caracter in cadena.split():
            try:
                return float(caracter)
            except ValueError:
                return 0
    
    @staticmethod
    def formato_cadena_fecha(cadena):
        """Obtiene de una cadena la fecha que se encuentre en ella\nRecibe como parámetro un String y regresa un objeto datetime"""

        for caracter in cadena.split():
            try:
                return datetime.strptime(caracter, LogicaNegocio.FORMATO_FECHA_MX)
            except ValueError:
                return None

    @staticmethod
    def obtiene_contenido_web(url):
        """Regresa el contenido en HTML de una URL dada\nRecibe como parámetro una URL y regresa un objeto BeautifulSoup"""
        try:
            result = requests.get(url)
        
            c = result.content

            return BeautifulSoup(c, "html.parser")
        except Exception as ex:
            log.error("Error al obtener el contenido del sitio web: %s", ex)
            raise

    @classmethod
    def encuentra_tipos_cambio(cls, url):
        """Encuentra todas los tipos de cambio y las fechas de la página especificada\nRecibe la URL de la página principal\nRegresa un diccionario {moneda:(fecha_publicacion, tipo_cambio)}"""
        fechas = {}
        tipos_cambio = {}
        
        try:
            contenido = LogicaNegocio.obtiene_contenido_web(url)
            if contenido != None:
                coleccion_divs = contenido.find_all("div")
                for div in coleccion_divs:
                    div_id = div.get("id")
                    if div_id != None:
                        if cls.DICCIONARIO_MONEDAS.get(div_id.upper(), "") != "":
                            tipos_cambio[id.upper()] = LogicaNegocio.formato_cadena_numero(str(div.text))
                        elif div_id.upper() in cls.DICCIONARIO_FECHAS.values():
                            fechas[div_id.upper()] = LogicaNegocio.formato_cadena_fecha(str(div.text))
            return LogicaNegocio.convierte_diccionarios(tipos_cambio, fechas)
        except Exception as ex:
            log.error("Error al leer el sitio web: %s", ex)
            raise

    @staticmethod
    def convierte_diccionarios(tipos_cambio, fechas):
        """Convierte los diccionarios de tipos de cambio y fechas de lo que se obtiene de la página web a un diccionario ordenado\nRecibe el diccionario de tipos de cambio y de fechas\nRegresa {moneda:(fecha_publicacion, tipo_cambio)}"""
        diccionario = {}
        if tipos_cambio:
            for key, value in tipos_cambio.items():
                if value > 0:
                    moneda = LogicaNegocio.DICCIONARIO_MONEDAS.get(key, None)
                    key_fecha = LogicaNegocio.DICCIONARIO_FECHAS.get(moneda, "")
                    fecha_publicacion = fechas.get(key_fecha, None)
                    diccionario[moneda] = (fecha_publicacion,value)
        return diccionario

    @staticmethod
    def obtiene_dias_inhabiles():
        """Obtiene los días inhábiles del año, días festivos y fines de semana"""
        
        dias_feriados = (datetime(datetime.now().year, 1, 1),
                         datetime(datetime.now().year, 2, 5),
                         datetime(datetime.now().year, 5, 1),
                         datetime(datetime.now().year, 9, 16),
                         datetime(datetime.now().year, 11, 2),
                         datetime(datetime.now().year, 12, 1),
                         datetime(datetime.now().year, 12, 12),
                         datetime(datetime.now().year, 12, 25))
        dias_feriados_lunes = (datetime(datetime.now().year, 3, 21),
                               datetime(datetime.now().year, 11, 20))
        inicio_anio = datetime(datetime.now().year, 1, 1)
        fin_anio = datetime(datetime.now().year, 12, 31)
        dias_anio = fin_anio - inicio_anio
        fines_semana = ()

        for i in range(dias_anio.days + 1):
            dia = inicio_anio + timedelta(days=i)
            if dia.weekday() >= 5:
                fines_semana = fines_semana + (dia,)
        for dia in dias_feriados_lunes:
            if dia.weekday() > 0:
                dias_feriados = dias_feriados + (dia  + timedelta(days=0-dia.weekday()),)
        for dia in dias_feriados:
            try:
                fines_semana.index(dia)
            except ValueError:
                fines_semana = fines_semana + (dia,)
        return sorted(fines_semana)

    @staticmethod
    def es_dia_habil(fecha):
        """Define si la fecha es un día hábil\nRecibe la fecha a determinar\nRegresa True si es un día hábil y False si no es un día hábil"""
        try:
            dias_inhabiles = LogicaNegocio.obtiene_dias_inhabiles()
            dias_inhabiles.index(fecha)
            return False
        except ValueError:
            return True

    @classmethod
    def obtiene_dias_habiles(cls, fecha_publicacion):
        """Obtiene el número de días inhábiles a partir de la fecha de publicación\nRecibe la fecha de publicación\Regresa el número de días no hábiles por delante"""
        dias = 1
        fecha_aplicacion = fecha_publicacion + timedelta(days=1)
        while LogicaNegocio.es_dia_habil(fecha_publicacion) and not LogicaNegocio.es_dia_habil(fecha_aplicacion):
            dias+=1
            fecha_aplicacion = fecha_publicacion + timedelta(days=dias)
        return dias
   
