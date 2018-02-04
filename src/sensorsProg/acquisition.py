# -*- coding: utf-8 -*-

import logging
import logging.config
import sys, getopt, time
# lib sensors
import tsl2591  #module capteur lux
from  BMP280 import BMP280   #module capteur temp et pression

import warp10Client

""" Acquisition des données provenant de capteurs branchés sur le bus I2C  

les capteurs sont :
- BMP280 : température et pression atmosphérique
- TLS2591 : luminuosité

le données sont ensuite envoyées sur warp10 via http
et les dernières mesures sont écrites dans le fichier /tmp/lastMeasures.log

si l'appli est lancée avcec le paramètre -d ( debug ), alors un seul cycle de mesures est effectué
et les actions sont décrites sur la console (sortie standard )
"""


WAIT_SECONDE = 30
DEBUG=False
WARP10_READ_TOKEN="ici le tocken warp10 de lecture de l'appli"
WARP10_WRITE_TOKEN="ici le tocken d'écritrure de l'appli"
WARP10_SERVER="http://127.0.0.1:8080"
WARP10_APPLI_ID="io.warp10.bootstrap"

QNH_ALTI=55.0  #altitude du capteur pour ramener la pression atmospherique au niveau de la mer QNH



logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def boucleMesure():
	
	sensorTsl = tsl2591.Tsl2591()  # initialize
	sensorBMP = BMP280.BMP280()
	wp10 = warp10Client.Warp10Client(WARP10_SERVER, WARP10_READ_TOKEN, WARP10_WRITE_TOKEN, WARP10_APPLI_ID)

	while True:
		#get Lux
		full, ir = sensorTsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
		lux = sensorTsl.calculate_lux(full, ir)  # convert raw values to lux
		wp10.addValueForWrite( "lux", [ ("sensor", "1") ], lux )
		logger.debug("capteur luminuosité : lux:{0} ,total:{1} , infraRouge:{2}".format(lux,full,ir))

		#get Temp end presure
		temp = sensorBMP.read_temperature()
		pres = sensorBMP.read_sealevel_pressure(altitude_m=QNH_ALTI) / 100  # div 100 = converion en hecto pascal
		logger.debug("capteur BMP280 : température:{0}, pression niveau de la mer:{1}".format(temp, pres))
		wp10.addValueForWrite( "temp", [ ("sensor", "1") ], temp )
		wp10.addValueForWrite( "pressure", [ ("sensor", "1") ], pres )

		wp10.pushValues()

		time.sleep(WAIT_SECONDE)


def main(argv):

	logger.info("programme started")
	boucleMesure()



if __name__ == "__main__":
	main(sys.argv[1:])
