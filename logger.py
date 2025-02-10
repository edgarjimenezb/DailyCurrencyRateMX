from logging.handlers import TimedRotatingFileHandler
from config import Config
from os import getcwd
import logging

#Se genera el Log con las configuraciones del INI de la aplicación
#Si no se pueden encontrar las configuraciones intenta crear un Log por default
#El Log se rola automáticamente al cambiar el día
configLog = Config.obtiene_config_log()
log = logging.getLogger(configLog.get('loggername', 'LogTipoCambio'))
loggerHandler = TimedRotatingFileHandler(configLog.get('path', getcwd() + "\\") + configLog.get('filename', 'tiposcambio2.log'), configLog.get('rotatetime', 'midnight'), 1, backupCount=5)
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
loggerHandler.setFormatter(formatter)
loggerHandler.setLevel(configLog.get('loglevel', logging.DEBUG))
log.addHandler(loggerHandler)
log.setLevel(configLog.get('loglevel', logging.DEBUG))

def get_logger():
    return log
