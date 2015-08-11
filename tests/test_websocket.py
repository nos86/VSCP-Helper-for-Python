import unittest
from server import TestServer
from vscphelper.websocket import websocket, answer
from vscphelper import VSCPConstant as const
from time import sleep

class websocketTests(unittest.TestCase):
    
    def setUp(self):
        self.server = TestServer(port=8080)

    def test_timeout(self):
        pass

    def test_send(self):
        pass

    def test_authentication(self):
        pass

    def test_receive(self):
        pass
    
    def tearDown(self):
        self.server.shutdown()
        

    
if __name__=="__main__":
    unittest.main()
