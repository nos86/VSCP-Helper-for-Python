import unittest
import datetime
from vscphelper.vscplib import vscpEvent as event
from vscphelper.vscplib import vscp
from vscphelper.websocket import answer
from tests.server import TestServer

class createAnswer:
    def __init__(self, message):
        self.is_binary = False
        self.data = message

class vscplibEventHackingTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_prova(self, ):
        pass
    
    
    def tearDown(self):
        pass

class vscplibEventDataFromFieldsTests(unittest.TestCase):
    def setUp(self):
        self.GUID = "FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00"
        self.event = event(0, 9, 1, 2, 523627200,self.GUID, [0,1,2,3])
    def test_checkHead(self):
        self.assertEqual(self.event.getHead(), 0)
        self.assertEqual(self.event.head, 0)
    def test_checkClass(self):
        self.assertEqual(self.event.getClass(), 9)
        self.assertEqual(self.event.vscp_class, 9)
    def test_checkType(self):
        self.assertEqual(self.event.getType(), 1)
        self.assertEqual(self.event.vscp_type, 1)
    def test_checkObdID(self):
        self.assertEqual(self.event.getObID(), 2)
        self.assertEqual(self.event.obid, 2)
    def test_checkGUID(self):
        self.assertEqual(self.event.getGUID(), self.GUID)
        self.assertEqual(self.event.guid, self.GUID)
    def test_checkTimestamp(self):
        self.assertEqual(self.event.getTimestamp(), 523627200)
        self.assertEqual(self.event.timestamp, 523627200)
        format = "%d-%m-%Y %H:%M:%S"
        self.assertEqual(self.event.getUTCDateTime(),
                         datetime.datetime.utcfromtimestamp(523627200).strftime(format))
        self.assertEqual(self.event.getLocalDateTime(),
                         datetime.datetime.fromtimestamp(523627200).strftime(format)) 
    def test_checkData(self):
        self.assertEqual(self.event.getDataLength(), 4)
        self.assertEqual(len(self.event.data), 4)
        self.assertEqual(self.event.getData(), [0,1,2,3])
        self.assertEqual(self.event.data, [0,1,2,3])
    def test_stringify(self):
        self.assertEqual(str(self.event), "E;0,9,1,2,523627200,"+self.GUID+",0,1,2,3")
class vscplibEventDataFromAnswerTests(unittest.TestCase):
    def setUp(self):
        self.GUID = "FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00"
        self.event = event.fromAnswer(answer(createAnswer("E;0,9,1,2,523627200,"+self.GUID+",0,1,2,3")))
    def test_checkHead(self):
        self.assertEqual(self.event.getHead(), 0)
        self.assertEqual(self.event.head, 0)
    def test_checkClass(self):
        self.assertEqual(self.event.getClass(), 9)
        self.assertEqual(self.event.vscp_class, 9)
    def test_checkType(self):
        self.assertEqual(self.event.getType(), 1)
        self.assertEqual(self.event.vscp_type, 1)
    def test_checkObdID(self):
        self.assertEqual(self.event.getObID(), 2)
        self.assertEqual(self.event.obid, 2)
    def test_checkGUID(self):
        self.assertEqual(self.event.getGUID(), self.GUID)
        self.assertEqual(self.event.guid, self.GUID)
    def test_checkTimestamp(self):
        self.assertEqual(self.event.getTimestamp(), 523627200)
        self.assertEqual(self.event.timestamp, 523627200)
        format = "%d-%m-%Y %H:%M:%S"
        self.assertEqual(self.event.getUTCDateTime(),
                         datetime.datetime.utcfromtimestamp(523627200).strftime(format))
        self.assertEqual(self.event.getLocalDateTime(),
                         datetime.datetime.fromtimestamp(523627200).strftime(format)) 
    def test_checkData(self):
        self.assertEqual(self.event.getDataLength(), 4)
        self.assertEqual(len(self.event.data), 4)
        self.assertEqual(self.event.getData(), [0,1,2,3])
        self.assertEqual(self.event.data, [0,1,2,3])
    def test_stringify(self):
        self.assertEqual(str(self.event), "E;0,9,1,2,523627200,"+self.GUID+",0,1,2,3")
class vscplibFunctionalTests(unittest.TestCase):
    def setup(self, ):
        self.server = TestServer(port=8080)
        self.client = vscp()
        self.server.send("^+;AUTH1")
        self.server.send("+;AUTH0;d002c278b35c152eed9ee2f475a561f1")
    
    def test_seedNotSent(self, ):
        #self.assert vscp()
        pass
        
    
    def teardown(self, ):
        self.server.shutdown()
    
    
    


class vscplibEventFunctionTests(unittest.TestCase):
    pass
    
    
if __name__ == '__main__':
    unittest.main()
    