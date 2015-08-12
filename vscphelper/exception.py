import vscphelper.VSCPConstant as constant

class VSCPException(Exception):
	"""Raised when an error with VSCP happens
	
	Attributes are:
		code
		message - string that describe the error
	"""
	
	def __init__(self, errorCode, message=None):
		self.code = errorCode
		if message:
			self.message = message
		else:
			if errorCode in constant.error_description.keys():
				self.message = constant.error_description[errorCode]
			else:
				self.message = ""
	
	def __str__(self):
		return self.message

class VSCPNoException(Exception):
	"""This exception is raisen when an asyncronous operation is
	completed with success
	"""
	pass