import unittest
from tests.server import TestServer
from vscphelper.exception import *
from vscphelper.websocket import websocket, answer
from vscphelper import VSCPConstant as const
from time import sleep
import logging

class createAnswer:
    def __init__(self, message):
        self.is_binary = False
        self.data = message
        
class websocketFailedTests(unittest.TestCase):
    def callback(self, message):
        pass
    def test_wrongDestination(self, ):
        with self.assertRaises(VSCPException):
            websocket(eventCallback = self.callback)
    def test_noCallback(self, ):
        with self.assertRaises(ValueError):
            websocket()

class websocketConnectionLost(unittest.TestCase):
    def callback(self, message):
        pass
    
    def test_ConnectionLost(self, ):
        server = TestServer(port=8081)
        ws = websocket(port=8081, eventCallback = self.callback, timeout=1)
        server.shutdown()
        with self.assertRaises(VSCPNoCommException):
            ws.send("C;NOOP")
        sleep(ws.timeout+0.1)         
        ws.close()
        
        
class websocketTests(unittest.TestCase):
    def callback(self, message):
        self.message = message
    
    def setUp(self):
        self.server = TestServer(port=8080)
        self.ws = websocket(eventCallback = self.callback)       
    def test_timeout(self):
        with self.assertRaises(ValueError):
            self.ws.setTimeout(0)
    def test_sendWithAnswer(self):
        answer = self.ws.send("+;NOOP")
        self.assertTrue(answer.isValid())  
    def test_sendWithoutAnswer(self, ):
        self.ws.setTimeout(2)
        with self.assertRaises(VSCPException):
            self.ws.send("^C;NOOP")
    def test_receiveSeed(self):
        self.ws.received_message(createAnswer("+;AUTH0;d002c278b35c152eed9ee2f475a561f1"))
        self.assertEqual(self.ws.seed, "d002c278b35c152eed9ee2f475a561f1")   
    def test_receiveAnswer(self, ):
        self.ws.received_message(createAnswer("+;NOOP"))
        self.assertIsInstance(self.ws.answer, answer)   
    def test_receiveEvent(self, ):
        self.message = None
        self.ws.received_message(createAnswer("E;0,9,1,1,523627200,FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00,0,1,2,3"))
        self.assertIsInstance(self.message, answer)
    def tearDown(self):
        self.ws.close()
        self.server.shutdown()

            
if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
