from websocket import websocket 
from exception import VSCPException, VSCPNoException 
from time import sleep
import vscp as constant
import socket
import signal


		
class vscp:
	def __init__(self, hostname='127.0.0.1', port='8080', user='admin', password='secret', domain='mydomain.com', timeout=1):
		self.authenticated = False
		self.timeout = timeout
		self.ws = websocket(hostname=hostname, port=port, eventCallback = self.__eventCallback, debug=True) #Open websocket
		self.passwordHash = md5(user+":"+domain+":"+password).hexdigest()
		self.user = user
		sleep(0.5) #Wait for authentication seed
		if self.ws.seed == None:
			raise VSCPException(constant.VSCP_ERROR_COMMUNICATION, "No AUTH0 is received by websocket")
		else:
			key = md5(self.user+":"+self.passwordHash+":"+seed).hexdigest()
			answer = self.doCommand("AUTH", [user, key])
			if answer.isFailed():
				raise VSCPException(constant.VSCP_ERROR_NOT_AUTHORIZED, answer.getFullErrorMessage())
			self.authenticated = True

	def isConnected(self):
		if self.ws.connected:
			return constant.VSCP_ERROR_SUCCESS
		else:
			return constant.VSCP_ERROR_ERROR
	def isAuthenticated(self):
		return self.authenticated
	def doCommand(self, command="NOOP", args=None):
		"""
		"""
		if self.isConnected()==False:
			return constant.VSCP_ERROR_NOT_OPEN
		return self.ws.send("C;"+command+";"+args.join(';'))
			
	def __eventCallback(self, answer):
		pass
		
	def setResponseTimeOut(self, timeout):
		self.ws.setTimeout(timeout)
	
	def checkReply(self):
		pass
	
	def clearLocalInpuQueue(self):
		self.doCommand("CLRQUEUE")
	def enterReceiveLoop(self):
		self.doCommand("OPEN")
	def quitReceiveLoop(self):
		self.doCommand("CLOSE")
	def noop(self):
		self.doCommand("NOOP")
	
	def clearDaemonEventQueue(self):
		pass
	
	def sendEvent(self):
		pass
	
	def receiveEvent(self):
		pass
	
	def isDataAvailable(self):
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