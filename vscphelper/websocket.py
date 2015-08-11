from ws4py.client.threadedclient import WebSocketClient
from hashlib import md5
from .exception import VSCPException, VSCPNoException
from time import sleep
from . import VSCPConstant as constant
import socket
import signal

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
                self.message = message.data
                self.msg = self.message.split(';')
            except AttributeError as err:
                raise ValueError("Expected object with ws4py.messaging.Message class") from err
	def isPositiveAnswer(self):
            return self.msg[0]=="+"
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
			return constant.error_description[errors[self.msg[1]]]
		else:
			return "Undefined error"
	def getFullErrorMessage(self):
		if self.msg[1] in self.errors.keys():
			message =  constant.error_description[errors[self.msg[1]]]
		else:
			message = "Undefined error"
		return message + " (" + str(self.message)+")"

	def getErrorCode(self):
            if self.message[0]=="+":
                return constant.VSCP_ERROR_SUCCESS
            elif self.msg[1] in self.errors.keys():
                return self.errors[self.msg[1]]
            else:
                return constant.VSCP_ERROR_ERROR

class websocket(WebSocketClient):
	def __init__(self, hostname='localhost', port=8080, debug = False, timeout=1, eventCallback=None):
		self.setTimeout(timeout)
		self.debugMessage = debug
		self.connected = False
		self.seed = None
		if eventCallback:
			self.eventCallback = eventCallback
		else:
			raise ValueError("Please, define eventCallback")
		try:
			super(websocket, self).__init__("ws://"+str(hostname)+":"+str(port))
			self.connect()
		except socket.error as err:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, str(err))
	def setDebugOption(self, status):
		self.debugMessage = status
	def setTimeout(self, timeout):
		if timeout > 0:
			self.timeout = timeout
		else:
			raise ValueError("Timeout must be greater than zero")

	def send(self, msg):
		try:
			signal.signal(signal.SIGALRM, self.__timeout)
			signal.alarm(self.timeout) #set the time-out
			self.answer = None
			super(websocket, self).send(str(msg))
			while(self.answer == None):
				sleep(0.01)
			signal.alarm(0) #switch-off the time-out alarm
			if self.answer.isFailed():
				raise VSCPException(self.answer.getErrorCode(), self.answer.getFullErrorMessage())
			return self.answer
		except socket.error as err:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, str(err))

	def __timeout(self,a,b):
		""" Internal function used to raise the timeout exception
		in case answer from websocket is not provited within maximum time
		"""
		raise VSCPException(constant.VSCP_ERROR_TIMEOUT, "Timeout occured during connection establishing")

	def opened(self):
		self.connected = True
		if self.debugMessage:
			print("Websocket opened with success")
	def closed(self, code, reason=None):
		self.connected = False
		if self.debugMessage:
			print("WebSocket closed")
	def received_message(self, message):
		if self.debugMessage:
			print("Received Message: " + str(message))
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
	pass
