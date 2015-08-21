import unittest
from tests.server import TestServer
from vscphelper.websocket import websocket, answer
import vscphelper.VSCPConstant as const

class createAnswer:
    def __init__(self, message):
        self.is_binary = False
        self.data = message
            
class websocketAnswerTests(unittest.TestCase):
        
    def test_wrongArgument(self):
        with self.assertRaises(ValueError):
            test = answer("M@1fo4med String!")
        
    def test_malformed(self):
        test = answer(createAnswer("M@1fo4med String!"))
        self.assertFalse(test.isValid())
        
    def test_positive(self):
        test = answer(createAnswer("+;NOOP"))
        self.assertTrue(test.isValid())
        self.assertEqual(test.isPositiveAnswer(),const.VSCP_ERROR_SUCCESS)
        self.assertFalse(test.isFailed())
        self.assertEqual(test.getType(), "Command")
        self.assertEqual(test.getErrorCode(), const.VSCP_ERROR_SUCCESS)

    def test_negative(self):
        test = answer(createAnswer("-;7;Not Authorized"))
        self.assertTrue(test.isValid())
        self.assertEqual(test.isPositiveAnswer(), const.VSCP_ERROR_ERROR)
        self.assertTrue(test.isFailed())
        self.assertEqual(test.getType(), "Command")
        self.assertEqual(test.getErrorCode(), const.VSCP_ERROR_NOT_AUTHORIZED)
    
    def test_event(self):
        test = answer(createAnswer("E;0,9,1,1,523627200,FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00, 0,1,2, 3"))
        self.assertTrue(test.isValid())
        self.assertEqual(test.isPositiveAnswer(),const.VSCP_ERROR_SUCCESS)
        self.assertFalse(test.isFailed())
        self.assertEqual(test.getType(),"Event")
        self.assertEqual(test.getErrorCode(), const.VSCP_ERROR_SUCCESS)
        
if __name__=="__main__":
    unittest.main()
