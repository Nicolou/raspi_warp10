import logging
import time
import requests
import sys


class Warp10Client(object):
	"""Object to POST data into warp10"""
	def __init__(self, server, readToken, writeToken, appliId):
		self._SERVER=server
		self._TOKEN_READ=readToken
		self._TOKEN_WRITE=writeToken
		self._APPLI=appliId
		self._stringToWrite=""
		self._logger = logging.getLogger(__name__)


	def addValueForWrite( self, name, labels, value ):
		""" prepare value to push on warp10 """
		# write timeStamp in warp10 format , ie microsecond since
		self._stringToWrite += "{0:16.0f}".format(time.time()*1000000 ) + "// "
		self._stringToWrite += self._APPLI + "." + name
		if len(labels) > 0:
			self._stringToWrite += "{"
			for label, val in labels:
				self._stringToWrite += label + "=" + val + ", "
			#remove last ", "
			self._stringToWrite.rstrip(", ")
			self._stringToWrite += "} "
		else:
			self._stringToWrite += "{} "
		#set value
		self._stringToWrite += str(value) + '\n'
		self._logger.debug(" warp10 data string = " + self._stringToWrite )


	def pushValues( self ):
		""" publish value to warp10 by sending http request """
		request_url = self._SERVER + '/api/v0/update'
		request_header = {'X-Warp10-Token' : self._TOKEN_WRITE }
		request_data = self._stringToWrite
		try:

			self._logger.debug(" post data to " + request_url)
			r = requests.request('POST', request_url, headers =request_header, data =request_data)
			self._logger.debug(" response : " + r.text )

		except requests.exceptions as ex:
			self.error("une erreur dans la requete vers " + self._SERVER + " est survenue" , Ex )

		#reinitialize the vlues string
		self._stringToWrite = ""


