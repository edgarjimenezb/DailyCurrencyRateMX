# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from negocio import LogicaNegocio
from datos import BaseDatos
from emailer import EMailer

def main():
    formato_fecha_mx = LogicaNegocio.FORMATO_FECHA_MX

    try:
        url = "https://www.banxico.org.mx/tipcamb/llenarTiposCambioAction.do?idioma=sp"
        tipos_cambio = LogicaNegocio.encuentra_tipos_cambio(url)

        if tipos_cambio:
            for key, value in tipos_cambio.items():
                moneda = key
                fecha_publicacion = value[0]
                tipo_cambio_dia = value[1]

                if BaseDatos.existe_tipo_cambio(moneda, fecha_publicacion) == 0:
                    dias = LogicaNegocio.obtiene_dias_habiles(fecha_publicacion)
                    for x in range(1, dias + 1):
                        fecha_aplicacion = fecha_publicacion + timedelta(days=x)
                        if BaseDatos.inserta_tipo_cambio(fecha_publicacion, fecha_aplicacion, tipo_cambio_dia, moneda):
                            print("Se inserta el tipo de cambio: Moneda '{0}', Valor '{1}' del día '{2}'".format(moneda, tipo_cambio_dia, datetime.strftime(fecha_aplicacion, formato_fecha_mx)))
                        else:
                            print("No se ha podido insertar el tipo de cambio: Moneda '{0}', Valor '{1}' del día '{2}'".format(moneda, tipo_cambio_dia, datetime.strftime(fecha_aplicacion, formato_fecha_mx)))
                else:
                    print("El tipo de cambio está actualizado para: Moneda '{0}' del día '{1}'".format(moneda, datetime.strftime(fecha_publicacion, formato_fecha_mx)))
        else:
            EMailer.envia_correo("ERROR", "Error al leer el sitio web {0}. No se encontraron datos!".format(url))
        
    except Exception as ex:
        EMailer.envia_correo("ERROR", str(ex))
        raise
        

if __name__ == "__main__":
    main()
