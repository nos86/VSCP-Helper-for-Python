import unittest
from server import TestServer
from vscphelper.websocket import websocket, answer
from vscphelper import VSCPConstant as const

class createAnswer:
    def __init__(self, message):
        self.is_binary = False
        self.data = message
            
class websocketTests(unittest.TestCase):
        
    def test_wrongArgument(self):
        with self.assertRaises(ValueError):
            test = answer("M@1fo4med String!")
        
    def test_malformed(self):
        test = answer(createAnswer("M@1fo4med String!"))
        self.assertFalse(test.isValid())
        
    def test_positive(self):
        test = answer(createAnswer("+;NOOP"))
        self.assertTrue(test.isValid())
        self.assertTrue(test.isPositiveAnswer())
        self.assertFalse(test.isFailed())
        self.assertEqual(test.getType(), "Command")
        self.assertEqual(test.getErrorCode(), const.VSCP_ERROR_SUCCESS)

    def test_negative(self):
        test = answer(createAnswer("-;7;Not Authorized"))
        self.assertTrue(test.isValid())
        self.assertFalse(test.isPositiveAnswer())
        self.assertTrue(test.isFailed())
        self.assertEqual(test.getType(), "Command")
        self.assertEqual(test.getErrorCode(), const.VSCP_ERROR_NOT_AUTHORIZED)

if __name__=="__main__":
    unittest.main()
