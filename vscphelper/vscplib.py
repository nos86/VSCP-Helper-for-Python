from websocket import websocket 
from exception import VSCPException, VSCPNoException 
from time import sleep
import vscp as constant
import socket
import signal

class answer:
	def __init__(self, answer, errorCode = constant.VSCP_ERROR_SUCCESS, errorMessage = ""):
		self.errorCode = errorCode
		self.answer = answer
		self.errorMessage = errorMessage
		
		def isPositiveAnswer(self):
			return self.answer[0]=="+"
		
		def command(self):
			return self.answer[1]
		
class vscp:
	def __init__(self, hostname='127.0.0.1', port='8080', user='admin', password='secret', domain='mydomain.com', timeout=1):
		self.authenticated = False
		self.timeout = timeout
		self.answer = None
		self.ws = websocket(hostname=hostname, port=port, callback = self.__threadCallback, debug=True) #Open websocket
		self.passwordHash = md5(user+":"+domain+":"+password).hexdigest()
		self.user = user
		sleep(0.5) #Wait for authentication seed
		if answer == None:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, "No AUTH0 is received by websocket")
		if answer.command() == "AUTH0":
			key = md5(self.user+":"+self.passwordHash+":"+seed).hexdigest(
			
			if self.sendCommand("AUTH", key).command() == "AUTH1":
				self.authenticated = True
				return constant.VSCP_ERROR_SUCCESS
			else:
				return 

		
	"""
	if msg[1] == "AUTH0":
				self.__sendAuthentication(msg[2])
			elif msg[1] == "AUTH1":
				self.authenticated = True
				if self.debugMessage:
					print("Authorized..!")
				self.callback(constant.VSCP_ERROR_SUCCESS, "")
			elif msg[1] == "OK":
	"""
	def __sendAuthentication(self, seed):
		if self.connected == False:
			pass
		
		self.send("C;AUTH;"+self.user+";"+key)
		pass
	
	def waitForAnswer(self):
		signal.signal(signal.SIGALRM, self.__timeout)
		signal.alarm(self.timeout) #set time-out
		self.exception = None
		while(self.exception == None):
			sleep(0.1)
		signal.alarm(0)
		
		
	def setResponseTimeOut(self, timeout):
		""" Set response time-out for answer coming from websocket
		"""
		self.timeout = timeout
	
	def isConnected(self):
		return self.ws.connected
	
	def doCommand(self, command, args):
		"""
		"""
		if self.isConnected()==False:
			return constant.VSCP_ERROR_NOT_OPEN
		signal.signal(signal.SIGALRM, self.__timeout)
		signal.alarm(self.timeout)
		self.ws.send("C;"+command+";"+args.join(';'))
		self.exception == None
		while(self.exception == None):
			sleep(0.01)
		signal.alarm(0)
		return self.exception['code']
			
	def __timeout(self, a, b):
		""" Internal function used to raise the timeout exception
		in case answer from websocket is not provited within maximum time
		"""
		raise VSCPException(constant.VSCP_ERROR_TIMEOUT, "Timeout occured during connection establishing")
			
	def __threadCallback(self, errorCode, message):
		self.exception = {'code': errorCode, 'message':message}
		
	def setResponseTimeOut(self):
		pass
	
	def isConnected(self):
		pass
	
	def doCommand(self):
		pass
	
	def checkReply(self):
		pass
	
	def clearLocalInpuQueue(self):
		pass
	
	def open(self):
		pass
	
	def openInterface(self):
		pass
		
	def close(self):
		pass
	
	def noop(self):
		pass
	
	def clearDaemonEventQueue(self):
		pass
	
	def sendEvent(self):
		pass
	
	def receiveEvent(self):
		pass
	
	def isDataAvailable(self):
		pass
	
	def enterReceiveLoop(self):
		pass
	
	def quitReceiveLoop(self):
		pass
		
	def blockingReceiveEvent(self):
		pass
	
	def setFilter(self):
		pass
	
	def getStatistics(self):
		pass
	
	def getStatus(self):
		pass
	
	def getVersion(self):
		pass
	
	def getDLLVersion(self):
		pass
	
	def getVendorString(self):
		pass
		
	def getDriverInfo(self):
		pass
	
	def doCmdShutDown(self):
		pass