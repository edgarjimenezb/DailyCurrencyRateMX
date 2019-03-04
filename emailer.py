import logger
import smtplib
from config import Config
from email.mime.text import MIMEText
from email.utils import formataddr

log = logger.getLogger()

class EMailer(object):
    """Clase para manejo de e-mail"""
    @classmethod
    def envia_correo(cls, nivel, mensaje):
        """Envía el correo de acuerdo a lo configurado en el INI de la aplicación\nRecibe una cadena indicando el nivel del aviso (INFO, ERROR) y el mensaje"""
        try:
            configuracion = Config.obtiene_config_email()
            if configuracion != None:
                msg = MIMEText(mensaje.encode('utf-8'), 'plain', 'utf-8')
                msg['From'] = formataddr(('ProFact', configuracion.get('from')))
                msg['To'] = formataddr(('Recipient', configuracion.get('to')))
                msg['Subject'] = nivel + ' : Tipo de cambio del día'
                server = smtplib.SMTP(host=configuracion.get('host'),
                                      port=configuracion.get('port'))
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(configuracion.get('username'), configuracion.get('password'))
                server.sendmail(configuracion.get('from'), [configuracion.get('to')], msg.as_string())
                server.quit()
            else:
                log.error("Eror al obtener la configuración del email.")
        except Exception as ex:
            log.error("Error al enviar el correo: %s", ex)
            