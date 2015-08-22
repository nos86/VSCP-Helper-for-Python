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

class VSCPNoCommException(VSCPException):
	def __init__(self, message=None):
		super(VSCPNoCommException, self).__init__(constant.VSCP_ERROR_COMMUNICATION, message)
