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

from vscphelper import websocket
from vscphelper.exception import * 
from time import sleep
import vscphelper.VSCPConstant as constant
import socket
import signal
import collections
import datetime
from hashlib import md5
import logging

logger = logging.getLogger(__name__)

class vscpEvent:
	def __init__(self, head, vscp_class, vscp_type, obid, timestamp, GUID, data=[]):
		""" Parameters are:
			head
			vscp_class int: VSCP Event Class
			vscp_type  int: VSCP Event Type
			obid
			timestamp  int: timestamp of message
			guid	string: Global Unique IDentifier
			data	int[8]:	Data of message (variable length up to 8)
		"""
		self.head = int(head)
		self.vscp_class = int(vscp_class)
		self.vscp_type = int(vscp_type)
		self.obid = int(obid)
		self.timestamp = int(timestamp)
		self.guid = str(GUID)
		self.data = []
		for i in range(0,len(data)):
			self.data.append(int(data[i]))
	def getHead(self):
		return self.head
	def getClass(self):
		return self.vscp_class
	def getType(self, ):
		return self.vscp_type
	def getObID(self, ):
		return self.obid
	def getGUID(self, ):
		return self.guid
	def getTimestamp(self, ):
		return self.timestamp
	def getUTCDateTime(self, format="%d-%m-%Y %H:%M:%S"):
		return datetime.datetime.utcfromtimestamp(int(self.timestamp)).strftime(format)
	def getLocalDateTime(self, format="%d-%m-%Y %H:%M:%S"):
		return datetime.datetime.fromtimestamp(int(self.timestamp)).strftime(format)
	def getDataLength(self):
		return len(self.data)
	def getData(self, ):
		return self.data           
	
	def __str__(self):
		data = [self.head, self.vscp_class, self.vscp_type, self.obid, self.timestamp, self.guid]
		for i in range(0, len(self.data)):
			data.append(self.data[i])
		for i in range(0, len(data)):
			data[i] = str(data[i])
		return "E;"+','.join(data)
	
	@classmethod
	def fromAnswer(cls, answer):
		if not isinstance(answer, websocket.answer):
			raise ValueError("Answer is not a vscphelper.websocket.answer object")
		if answer.getType()!="Event":
			raise ValueError("Impossible to init a vscpEvent using an answer that is not an Event one")
		temp = str(answer.msg[1]).split(",")
		data = []
		if len(temp)>5:
			for i in range(6, len(temp)):
				data.append(temp[i])
		return cls(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], data)
		
class vscp:
	def __init__(self, hostname='127.0.0.1', port='8080', user='admin', password='secret', domain='mydomain.com', timeout=2):
		self.queue = collections.deque()
		self.eventStreaming = False
		self.authenticated = False
		self.timeout = timeout
		self.ws = websocket.websocket(hostname=hostname, port=port, eventCallback = self.__eventCallback) #Open websocket
		self.passwordHash = md5((user+":"+domain+":"+password).encode('utf-8')).hexdigest()
		self.user = user
		for i in range(0,50):
			sleep(0.01)
			if self.ws.seed is not None:
				break
		if self.ws.seed == None:
			raise VSCPNoCommException("No AUTH0 is received by websocket")
		else:
			key = md5((self.user+":"+self.passwordHash+":"+seed).encode('utf-8')).hexdigest()
			answer = self.doCommand("AUTH", [user, key])
			if answer.isFailed():
				raise VSCPException(constant.VSCP_ERROR_NOT_AUTHORIZED, answer.getFullErrorMessage())
			self.authenticated = True
	def setResponseTimeOut(self, timeout=2):
		"""This is the timeout in seconds used when checking for replies after commands has been sent to the server.
		The value is also used multiplied with three as a connection timeout.
		It can be changed anytime during a communication session.
		Default value is 2 seconds.
		"""
		if timeout>0:
			self.ws.setTimeout(timeout)
		else:
			raise ValueError("Timeout must be be greater than 0")
	def isConnected(self):
		"""Check if the session is active or not and returns:
		VSCP_ERROR_SUCCESS if websocket is opened and user is authenticated
		VSCP_ERROR_ERROR if at least user is not autheticated
		"""
		if self.ws.connected and self.authenticated:
			return constant.VSCP_ERROR_SUCCESS
		else:
			return constant.VSCP_ERROR_ERROR
	def doCommand(self, command="NOOP"):
		"""Send a command over the communication link.
		The response from the server will be checked for +;COMMAND
		
		Return value should be:
		VSCP_ERROR_SUCCESS if the VSCP daemon respond with +OK after it has received the command
		VSCP_ERROR_ERROR if not (-OK) or no response before the timeout expires.
		VSCP_ERROR_CONNECTION is returned if the communication channel is not open.
		"""
		if self.isConnected()==False:
			return constant.VSCP_ERROR_CONNECTION
		answer = self.ws.send("C;"+command)
		return answer.isPositiveAnswer()
	def clearDaemonEventQueue(self):
		""" Clear the receiving side (to us) event queue on the VSCP daemon
		VSCP_ERROR_SUCCESS if the VSCP daemon cleared the queue
		VSCP_ERROR_ERROR if not or no response is received before the timeout expires.
		VSCP_ERROR_CONNECTION is returned if the communication channel is not open
		"""	
		return self.doCommand("CLRQUEUE")
	def enterReceiveLoop(self):
		"""Enter the receive loop.
		
		Return
		VSCP_ERROR_SUCCESS on success
		VSCP_ERROR_ERROR on failure.
		VSCP_ERROR_CONNECTION If the connection is closed.
		"""
		self.eventStreaming = True
		return self.doCommand("OPEN")
	def quitReceiveLoop(self):
		"""Quit the receive loop.
		
		Return
		VSCP_ERROR_SUCCESS on success
		VSCP_ERROR_ERROR on failure.
		VSCP_ERROR_CONNECTION If the connection is closed.
		"""
		if self.eventStreaming == False:
			self.doCommand("CLOSE")
			self.eventStreaming = False
			
	def noop(self):
		"""This is a command that can be used for test purposes.
		It does not do anything else then to send a command over the interfaces and check the result.
		
		Returns
		VSCP_ERROR_SUCCESS on success
		VSCP_ERROR_ERROR on failure.
		VSCP_ERROR_CONNECTION If the connection is closed.
		"""
		self.doCommand("NOOP")
	
	def sendEvent(self, event):
		pass
	
	def receiveEvent(self):
		"""Receive one VSCP event from the remote VSCP daemon.
		
		Returns VSCPEvent object if available, otherwise None is returned
		"""
		if self.isDataAvailable>0:
			return self.queue.pop()
		else:
			return None
	def isDataAvailable(self):
		"""Check the number of events (if any) that are available in the remote input queue
		
		Returns number of events ready to be read
		"""
		return len(self.queue)
	def blockingReceiveEvent(self):
		"""Blocking receive event.
		
		As soon as a new event is received, it will be returned to caller
		
		In case of connection is closed or user is not authenticated, VSCPException(VSCP_ERROR_CONNECTION) is raised
		In case of ReceiveLoop is closed VSCPException(VSCP_ERROR_OPERATION_FAILED) is raised
		"""
		if self.eventStreaming == False:
			raise VSCPException(constant.VSCP_ERROR_OPERATION_FAILED)
		while(self.isDataAvailable==0):
			if self.authenticated == False or self.ws.connected == False:
				raise VSCPException(constant.VSCP_ERROR_CONNECTION)
			sleep(0.1)
		return self.receiveEvent()
	
	def setFilter(self):
		pass
	
	def __eventCallback(self, answer):
		self.queue.appendleft(vscpEvent.fromAnswer(answer))
		