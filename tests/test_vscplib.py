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
        
    

#class vscplibFunctionalTests(unittest.TestCase):
    # def setup(self, ):
    #     self.server = TestServer(port=8080)
    #     self.client = vscp()
    #     self.server.send("^+;AUTH1")
    #     self.server.send("+;AUTH0;d002c278b35c152eed9ee2f475a561f1")
    # 
    # def test_seedNotSent(self, ):
    #     #self.assert vscp()
    #     pass
    #     
    # 
    # def teardown(self, ):
    #     self.server.shutdown()
    
    
if __name__ == '__main__':
    unittest.main()