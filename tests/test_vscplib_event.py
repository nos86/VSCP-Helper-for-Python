import unittest
from vscphelper.vscplib import vscpEvent as event

class vscplibEventHackingTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_prova(self, ):
        pass
    
    
    def tearDown(self):
        pass

class vscplibEventFunctionTests(unittest.TestCase):
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
        print("Implement other check like datetime")
    def test_checkData(self):
        self.assertEqual(self.event.getDataLength(), 4)
        self.assertEqual(len(self.event.data), 4)
        self.assertEqual(self.event.getData(), [0,1,2,3])
        self.assertEqual(self.event.data, [0,1,2,3])
    def test_stringify(self):
        self.assertEqual(str(self.event), "E;0,9,1,2,523627200,"+self.GUID+",0,1,2,3")
    
        
    
    
if __name__ == '__main__':
    unittest.main()
    