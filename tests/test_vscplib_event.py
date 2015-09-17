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

class vscplibEventMalformedTests(unittest.TestCase):
    def test_createEventFromMalformedAnswer(self):
        with self.assertRaises(ValueError):
            event.fromAnswer("abcdef")
            

class vscplibEventDataFromFieldsTests(unittest.TestCase):
    def setUp(self):
        self.GUID = "FF:FF:FF:FF:FF:FF:FF:FE:00:26:55:CA:00:06:00:00"
        self.event = event(vscp_class = 9,
                           vscp_type = 1,
                           vscp_data = [0,1,2,3],
                           timestamp = 523627200,
                           GUID = self.GUID,
                           obid = 2,
                           head = 0)
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
    def test_checkNodeID(self):
        self.assertEqual(self.event.getNodeId(), int(self.GUID[-2:],16))
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

if __name__ == '__main__':
    unittest.main()
    