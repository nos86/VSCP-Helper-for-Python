
class VSCPException(Exception):
	"""Raised when an error with VSCP happens
	
	Attributes are:
		code
		message - string that describe the error
	"""
	
	def __init__(self, errorCode, message):
		self.code = errorCode
		self.message = message
	
	def __str__(self):
		return self.message

class VSCPNoException(Exception):
	"""This exception is raisen when an asyncronous operation is
	completed with success
	"""
	pass