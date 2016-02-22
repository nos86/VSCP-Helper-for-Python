###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Musumeci Salvatore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from ws4py.client.threadedclient import WebSocketClient
from eventlet.timeout import Timeout
from hashlib import md5
from .exception import *
from time import sleep
from . import VSCPConstant as constant
import socket
import logging

logger = logging.getLogger(__name__)

class answer:
	errors = {
		'1': constant.VSCP_ERROR_SYNTAX,
		'2': constant.VSCP_ERROR_NOT_SUPPORTED,
		'3': constant.VSCP_ERROR_TRM_FULL,
		'4': constant.VSCP_ERROR_DEFINED_VAR,
		'5': constant.VSCP_ERROR_VAR_NOT_FOUND,
		'6': constant.VSCP_ERROR_PASSWORD,
		'7': constant.VSCP_ERROR_NOT_AUTHORIZED
	}
	def __init__(self, message):
		try:
			self.message = message.data if isinstance(message.data, str) else message.data.decode('utf-8')
			self.msg = self.message.split(';')
		except AttributeError as err:
			raise ValueError("Expected object with ws4py.messaging.Message class") #from err
	def isPositiveAnswer(self):
		if self.msg[0]=="+" or self.msg[0]=="E":
			return constant.VSCP_ERROR_SUCCESS
		else:
			return constant.VSCP_ERROR_ERROR
	def isFailed(self):
		return self.msg[0]=="-"
	def getType(self):
		if self.msg[0]=="E":
			return "Event"
		elif self.msg[0]=="+" or self.msg[0]=="-":
			return "Command"
		else:
			return "unknown"
	def isValid(self):
		if self.msg[0] == "+" and len(self.msg)>1:
			return True
		elif self.msg[0] == "-" and len(self.msg)==3:
			return True
		elif self.msg[0]=="E" and len(self.msg)==2 :
			return len(self.msg[1].split(','))>=7
		else:
			return False
	def getErrorMessage(self):
		if self.msg[1] in self.errors.keys():
			return constant.error_description[self.errors[self.msg[1]]]
		else:
			return "Undefined error"
	def getFullErrorMessage(self):
		if self.msg[1] in self.errors.keys():
			message =  constant.error_description[self.errors[self.msg[1]]]
		else:
			message = "Undefined error"
		return message + " (" + str(self.message)+")"

	def getErrorCode(self):
		if self.msg[0]=="+" or self.msg[0]=="E":
			return constant.VSCP_ERROR_SUCCESS
		elif self.msg[1] in self.errors.keys():
			return self.errors[self.msg[1]]
		else:
			return constant.VSCP_ERROR_ERROR

class websocket(WebSocketClient):
	def __init__(self, hostname='localhost', port=8080, timeout=2, eventCallback=None):
		self.setTimeout(timeout)
		self.connected = False
		self.seed = None
		if eventCallback:
			self.eventCallback = eventCallback
		else:
			raise ValueError("Please, define eventCallback")
		try:
			super(websocket, self).__init__("ws://"+str(hostname)+":"+str(port))
			self.connect()
		except ConnectionError as err:
			raise VSCPNoCommException(str(err)) #from None
		except socket.error as err:
			raise VSCPNoCommException(str(err)) #from None
		
		
	def setTimeout(self, timeout):
		if timeout > 0:
			self.timeout = timeout
		else:
			raise ValueError("Timeout must be greater than zero")

	def send(self, msg, waitForResponse = True):
		try:
			self.answer = None
			if self.connected:
				timeout = Timeout(self.timeout, self.__timeout)
				super(websocket, self).send(str(msg), False)
			else:
				raise VSCPNoCommException("Websocket is closed")
			if waitForResponse == False:
				timeout.cancel()
				return None
			while(self.answer == None):
				sleep(0.01)
			timeout.cancel() #switch-off the time-out alarm
			if self.answer.isFailed():
				raise VSCPException(self.answer.getErrorCode(), self.answer.getFullErrorMessage())
			return self.answer
		except socket.error as err:
			raise VSCPNoCommException(str(err))

	def __timeout(self,a,b):
		""" Internal function used to raise the timeout exception
		in case answer from websocket is not provited within maximum time
		"""
		raise VSCPException(constant.VSCP_ERROR_TIMEOUT, "Timeout occured during answer waiting")

	def opened(self):
		self.connected = True
		logger.info("Websocket opened with success")
	def closed(self, code, reason=None):
		self.connected = False
		logger.info("WebSocket closed")
	def received_message(self, message):
		logger.info("Received Message: " + str(message))
		obj = answer(message)
		if obj.getType() == "Command":
			if obj.msg[1] == "AUTH0":
				self.seed = obj.msg[2]
			else:
				self.answer = obj
		elif obj.getType() == "Event":
			self.eventCallback(obj)
		else:
			raise VSCPException(constant.VSCP_ERROR_NOT_SUPPORTED, "I can't understand last incoming message :"+obj.message)
	

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
