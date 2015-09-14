import unittest
from tests.server import TestServer
from vscphelper.vscplib import vscp, vscpEvent
from vscphelper.exception import *
from vscphelper import VSCPConstant as constant
from time import sleep


class vscplibMalfunctionTests(unittest.TestCase):
    def test_seedNotSent(self):
        a = TestServer(port=8080)
        with self.assertRaises(VSCPNoCommException):
            vscp()
        a.shutdown()
    
    def test_noCommunicationInit(self, ):
        with self.assertRaises(VSCPNoCommException):
            vscp()

class vscplibFunctionalTests(unittest.TestCase):
    def setUp(self, ):
        self.server = TestServer(port=8080,
                                 welcomeMessage = "+;AUTH0;d002c278b35c152eed9ee2f475a561f1|+;AUTH1")
        self.client = vscp(user='admin', password='secret', domain='mydomain.com')
        
    def __receiveMessage(self):
        self.receivedMessage = True
    
    def test_checkAuthenticated(self, ):
        self.assertTrue(self.client.authenticated)
        
    def test_checkSeedAndKey(self, ):
        self.assertEqual(self.client.ws.seed, "d002c278b35c152eed9ee2f475a561f1")
        self.assertEqual(self.client.calculateKey('admin', 'secret', 'mydomain.com'),
                         '1aaabe6d6af390f9729618ad3af4782f')
    
    def test_setResponseTimeout(self):
        self.client.setResponseTimeOut(1)
        self.assertEqual(self.client.ws.timeout, 1)
        with self.assertRaises(ValueError):
            self.client.setResponseTimeOut(0)
    
    def test_setHandler(self):
        self.assertIsNone(self.client.handler)
        with self.assertRaises(ValueError):
            self.client.setHandler("Malformed")
        self.client.setHandler(self.receivedMessage)
        event = "E;0,9,1,1,523627200,FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00,0,1,2,3"
        self.client.ws.send(event, False)
        sleep(0.1)
        self.assertTrue(self.receivedMessage)

    def test_doCommand(self, ):
        self.client.ws.send("^+;NOOP", False)
        self.assertEqual(self.client.isConnected(),
                         constant.VSCP_ERROR_SUCCESS)
        self.assertEqual(self.client.doCommand(),
                         constant.VSCP_ERROR_SUCCESS)
        self.client.ws.send("^-;2;Unkown command",False)
        self.assertEqual(self.client.doCommand(),
                         constant.VSCP_ERROR_ERROR)
        self.client.ws.connected = False
        self.assertEqual(self.client.doCommand(),
                         constant.VSCP_ERROR_CONNECTION)
        self.client.ws.connected = True
    
    def test_sendEvent(self, ):
        event = vscpEvent(0, 2, 0, 0, 0, "", [1])
        with self.assertRaises(ValueError):
            self.client.sendEvent("Malformed Arg")
        self.client.ws.connected = False
        self.assertEqual(self.client.doCommand(),
                         constant.VSCP_ERROR_CONNECTION)
        self.client.ws.connected = True
        self.client.ws.send("^+;EVENT", False)
        self.assertEqual(self.client.isConnected(),
                         constant.VSCP_ERROR_SUCCESS)
        self.assertEqual(self.client.sendEvent(event),
                         constant.VSCP_ERROR_SUCCESS)
        self.client.ws.send("^-;2;Unkown command",False)
        self.assertEqual(self.client.sendEvent(event),
                         constant.VSCP_ERROR_ERROR)
        
        
    def test_ReceiveLoop(self, ):
        self.assertFalse(self.client.eventStreaming)
        self.client.ws.send("^+;OPEN|+;CLOSE", False)
        self.client.enterReceiveLoop()
        self.assertTrue(self.client.eventStreaming)
        self.client.quitReceiveLoop()
        self.assertFalse(self.client.eventStreaming)
        
    def test_receiveData(self, ):
        GUID = "FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00"
        event = "E;0,9,1,2,523627200,"+GUID+",0,1,2,3"
        self.assertFalse(self.client.isDataAvailable())
        self.assertEqual(self.client.receiveEvent(), None)
        self.client.ws.send(event, False)
        sleep(0.05)
        self.assertTrue(self.client.isDataAvailable())
        self.assertIsInstance(self.client.receiveEvent(), vscpEvent)
        
    def test_blockingReceiveData(self, ):
        event = "E;0,9,1,1,523627200,FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00,0,1,2,3"
        with self.assertRaises(VSCPException):
            self.client.blockingReceiveEvent()
        self.client.eventStreaming = True
        self.client.authenticated = False
        self.assertFalse(self.client.isDataAvailable())
        with self.assertRaises(VSCPException):
            self.client.blockingReceiveEvent()
        self.client.authenticated = True
        self.client.ws.connected = True
        self.client.ws.send(event, False)
        self.assertIsInstance(self.client.blockingReceiveEvent(),
                              vscpEvent)
    
    
    def tearDown(self, ):
        self.client.ws.close() 
        self.server.shutdown()
    
    
if __name__ == '__main__':
    unittest.main()