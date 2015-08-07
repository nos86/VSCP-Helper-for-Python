from ws4py.client.threadedclient import WebSocketClient
from hashlib import md5
import string
from exception import VSCPException, VSCPNoException
import vscp as constant

class answer:
	def __init__(self, answer, errorCode = constant.VSCP_ERROR_SUCCESS, errorMessage = ""):
		self.errorCode = errorCode
		self.answer = answer
		self.errorMessage = errorMessage
		
		def isPositiveAnswer(self):
			return self.answer[0]=="+"
		
		def command(self):
			return self.answer[1]
			
class websocket(WebSocketClient): 	
	def __init__(self, hostname='localhost', port=8080, debug = False, timeout=1):
		self.timeout = timeout
		self.debugMessage = debug
		self.connected = False
		self.authenticated = False
		try:
			super(websocket, self).__init__("ws://"+str(hostname)+":"+str(port))
			self.connect()
		except socket.error, err:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, str(err))
		
	def setDebugOption(self, status):
		self.debugMessage = status
	
	def send(self, msg):
		try:
			super(websocket, self).send(msg)
			if self.debugMessage:
				print "Sent message: ", msg
		except socket.error, err:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, str(err))
	
	def blockingSend(self, msg):
		try:
			signal.signal()
		
	def opened(self):
		self.connected = True
		self.authenticated = False
		if self.debugMessage:
			print("Websocket opened with success")
	
	def closed(self):
		self.connected = False
		self.authenticated = False
		if self.debugMessage:
			print("WebSocket closed")
	
	def received_message(self, message):
		msg = string.split(str(message), ';')
		if self.debugMessage:
			print("Received Message: " + str(msg))
		if msg[0]=="+":
			self.callback(constant.VSCP_ERROR_SUCCESS, message)
		elif msg[0]=="-":
			if msg[1] == "1":
				self.callback(constant.VSCP_ERROR_SYNTAX, str(message))
			elif msg[1] == "2":
				self.callback(constant.VSCP_ERROR_NOT_SUPPORTED, str(message))
			elif msg[1] == "3":
				self.callback(constant.VSCP_ERROR_TRM_FULL, str(message))
			elif msg[1]== "4":
				self.callback(constant.VSCP_ERROR_DEFINED_VAR, str(message))
			elif msg[1] == "5":
				self.callback(constant.VSCP_ERROR_VAR_NOT_FOUND, str(message))
			elif msg[1] == "6":
				self.callback(constant.VSCP_ERROR_PASSWORD, str(message))
			elif msg[1]=="7":
				if self.authenticated:
					self.callback(constant.VSCP_ERROR_AUTHORIZED, str(message))
				else:
					self.callback(constant.VSCP_ERROR_PASSWORD, str(message))
			else:
				self.callback(constant.VSCP_ERROR_GENERIC, str(message))
		else:
			self.callback(constant.VSCP_ERROR_ERROR, str(message))
		
		
if __name__ == "__main__":
	pass