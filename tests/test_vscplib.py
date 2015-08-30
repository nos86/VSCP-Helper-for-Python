import unittest
from tests.server import TestServer
from vscphelper.vscplib import vscp
from vscphelper.exception import *
from vscphelper import VSCPConstant as constant


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
        
    def test_checkAuthenticated(self, ):
        self.assertTrue(self.client.authenticated)
        
    def test_checkSeedAndKey(self, ):
        self.assertEqual(self.client.ws.seed, "d002c278b35c152eed9ee2f475a561f1")
        self.assertEqual(self.client.calculateKey('admin', 'secret', 'mydomain.com'),
                         '1aaabe6d6af390f9729618ad3af4782f')
    
    
    def tearDown(self, ):
        self.client.ws.close() 
        self.server.shutdown()
    
    
if __name__ == '__main__':
    unittest.main()