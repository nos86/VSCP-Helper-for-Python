from vscphelper.vscplib import *
import vscphelper.VSCPConstant as constant
from vscphelper.VSCPUtils import *
from vscphelper.exception import *
import logging
import time
import signal

logger = logging.getLogger(__name__)

class DecisionMatrixRow(object):
    """Contains all information about decision matrix row of a node
    It can be used to
    -   save information coming from remote node
    -   create a decision matrix row for your virtual node
    
    Variables are:
    -   oaddr: origin address
    -   flags: flags byte (raw data)
    -   class_mask: mask for class (already completed with additional bit written in flags byte)
    -   class_filter: filter for class (already completed with additional bit written in flags byte)
    -   type_mask: mask for type
    -   type_filter: filter for type
    -   action: it can be a number (in case of copy of remote node) or a callable function (in case of
                of virtual node) that will be executed when incoming event will match with criteria
    -   action_parameter: it can be a number (in case of copy of remote node) or a set of parameters to
                pass to action function when action is executed
    """
    logger = logging.getLogger(__name__+'.DecisionMatrixRow')
    def __init__(self,
                 oaddr,
                 flags,
                 class_mask,
                 class_filter,
                 type_mask,
                 type_filter,
                 action,
                 action_parameter):
        self.logger.debug("New DMRow: {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(oaddr,
                                                                                    flags,
                                                                                    class_mask,
                                                                                    class_filter,
                                                                                    type_mask,
                                                                                    type_filter,
                                                                                    action,
                                                                                    action_parameter))
        if checkRangeOfInt(oaddr, "Originating Address"):
            self.oaddr = oaddr
        if checkRangeOfInt(flags, "Flags"):
            self.flags = flags
        if checkRangeOfInt(class_mask, "Class Mask"):
            self.class_mask = class_mask + 256 * ((self.flags & 0x02)>0)
        if checkRangeOfInt(class_filter, "Class Filter"):
            self.class_filter = class_filter + 256 * ((self.flags & 0x01)>0)
        if checkRangeOfInt(type_mask, "Type Mask"):
            self.type_mask = type_mask
        if checkRangeOfInt(type_filter, "Type Filter"):
            self.type_filter = type_filter
        if callable(action):
            self.action = action
            self.action_parameter = action_parameter
        elif checkRangeOfInt(action, "Action") and checkRangeOfInt(action_parameter, "Action Parameter"):
            self.action = action
            self.action_parameter = action_parameter
        
    def isEnabled(self, ):
        """Return True if this row is enabled
        """
        return (self.flags & 0x80) > 0
    def isAddressMatchRequired(self, ):
        """Return True if originating address is checked to trigger DM
        """
        return (self.flags & 0x40) > 0
    def isAddressHardCoded(self, ):
        """Return True if originating address is hard-coded expected
        """
        return (self.flags & 0x20) > 0
    def matchZoneRequired(self, ):
        """Return True if zone is checked to trigger DM
        """
        return (self.flags & 0x10) > 0
    def matchSubzoneRequired(self, ):
        """Return True if subzone is checked to trigger DM
        """
        return (self.flags & 0x08) > 0
    
    @classmethod
    def makeFlagsByte(cls,
                      isEnabled,
                      checkOriginAddress,
                      isHardCodedAddress,
                      matchZone,
                      matchSubzone,
                      class_mask,
                      class_filter
                      ):
        """ Make flags byte starting from single information:
        -   isEnabled: Row is enabled if set to True
        -   checkOriginAddress: oaddr should match nickname of event (=True) or don't care (=False)
        -   isHardCoded: Indicates hard-coded originating address if set to True
        -   matchZone: match Zone to trigger DM if set to True
        -   matchSubzone: match Sub-Zone to trigger DM if set to True
        -   class_mask: entire class mask in order to extract bit 8
        -   class_filter: entire class filter in order to extract bit 8
        """
        result = 0 + \
                0x80 * isEnabled + \
                0x40 * checkOriginAddress + \
                0x20 * isHardCodedAddress + \
                0x10 * matchZone + \
                0x08 * matchSubzone + \
                0x02 * (class_mask>255) + \
                0x01 * (class_filter>255)
        return result
    
class Node:
    """This class contains and handles all information about node
    """
    def __init__(self, nodeId, vscp_obj):
        if not isinstance(nodeId, int):
            raise TypeError("NodeId must be an integer")
        if int(nodeId)<0 or int(nodeId)>255:
            raise ValueError("NodeId is out of range [0, 255]")
        self.id = nodeId
        if not isinstance(vscp_obj, vscp):
            raise TypeError("vscp_obj is not a vscphelper.vscplib.vscp object")
        self.vscp = vscp_obj
        self.lastPing = time.time()
        self.mdf = None
        self.guid = None
        self.regs = {}
        self.DM = None
        
    def receiveEvent(self, event):
        if event.vscp_class == constant.VSCP_CLASS1_INFORMATION:
            if event.vscp_type == constant.VSCP_TYPE_INFORMATION_NODE_HEARTBEAT:
                self.lastPing = time.time()
        elif event.vscp_class == constant.VSCP_CLASS1_PROTOCOL:
            if event.vscp_type == constant.VSCP_TYPE_PROTOCOL_PROBE_ACK:
                self.lastPing = time.time()
            elif event.vscp_type == constant.VSCP_TYPE_PROTOCOL_RW_RESPONSE:
                self.regs[event.getData()[0]] = event.getData()[1]
            elif event.vscp_Type == constant.VSCP_TYPE_PROTOCOL_MATRIX_INFO_RESPONSE:
                self.DM = {'size': event.getData()[0],
                           'offset': event.getData()[1],
                           'rows': {}}
                if len(event.getData())>2:
                    self.DM['offsetPageStart'] = event.getData()[3]*255 + event.getData()[2]
                else:
                    self.DM['offsetPageStart'] = 0
    
    def readRegister(self, address, cache = False, timeout=2):
        """Return the value of register at [address] location
        if timeout is elapsed, NoneValue is returned
        """
        if not isinstance(address, int):
            raise TypeError("Address must be an integer")
        if int(address)<0 or int(address)>255:
            raise ValueError("Address is out of range [0, 255]")
        if address in self.regs.keys() and cache:
            if not self.regs[address] == None:
                return self.regs[address]
        self.regs[address] = None
        self.vscp.sendSimpleEvent(vscp_class = constant.VSCP_CLASS1_PROTOCOL,
                                  vscp_type = constant.VSCP_TYPE_PROTOCOL_READ_REGISTER,
                                  vscp_data = [self.id, address])
        try:
            signal.signal(signal.SIGALRM, self.__timeout)
            signal.alarm(timeout)
            while(self.regs[address]==None):
                time.sleep(0.02)
            signal.alarm(0)
            return self.regs[address]
        except VSCPException:
            return None   
    def writeRegister(self, address, value, timeout=2):
        """Return True if value is correctly written
        if timeout is elapsed, False is returned
        """
        if not isinstance(address, int):
            raise TypeError("Address must be an integer")
        if int(address)<0 or int(address)>255:
            raise ValueError("Address is out of range [0, 255]")
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if int(value)<0 or int(value)>255:
            raise ValueError("Value is out of range [0, 255]")
        self.regs[address] = None
        self.vscp.sendSimpleEvent(vscp_class = constant.VSCP_CLASS1_PROTOCOL,
                                  vscp_type = constant.VSCP_TYPE_PROTOCOL_WRITE_REGISTER,
                                  vscp_data = [self.id, address, value])
        try:
            signal.signal(signal.SIGALRM, self.__timeout)
            signal.alarm(timeout)
            self.regs[address] = None
            while(self.regs[address]==None):
                time.sleep(0.02)
            signal.alarm(0)
            return self.regs[address]==value
        except VSCPException:
            return False
    
    def downloadDM(self, timeout = 2, cached = False):
        self.DM = None
        self.vscp.sendSimpleEvent(vscp_class=constant.VSCP_CLASS1_PROTOCOL,
                                  vscp_type=constant.VSCP_TYPE_PROTOCOL_GET_MATRIX_INFO,
                                  vscp_data=[self.nodeId])
        signal.signal(signal.SIGALRM, self.__timeout)
        signal.alarm(timeout)
        try:
            while(self.DM == None):
                time.sleep(0.02)
            signal.alarm(0)
            for i in range(self.DM['size']):
                self.DM['rows'][i] = self.getRowOfDM(i)
            
        except:
            return constant.VSCP_ERROR_ERROR
    
    def getRowOfDM(self, row, cached = False, timeout=2):
        pass
    
        
    def __timeout(self, a, b):
        raise VSCPException(constant.VSCP_ERROR_TIMEOUT)
    
        
class Manager:
    """This class is an util for main activity on VSCP like:
    - Discover nodes
    - Get node information
    - Read/Write registers of node
    - Configure Node
    """
    def __init__(self, vscp_object):
        if not isinstance(vscp_object, vscp):
            raise ValueError("vscp_object must be a vscphelper.vscplib.vscp object)")
        self.vscp = vscp_object
        self.nodes = []
        vscp_object.clearDaemonEventQueue()
        vscp_object.enterReceiveLoop()
        vscp_object.setHandler(self.__receivedMessage)
              
    def __receivedMessage(self):
        event = self.vscp.receiveEvent()
        logger.debug(str(event))
        addressed = False
        for node in self.nodes:
            if event.getNodeId() == node.id:
                node.receiveEvent(event)
                addressed = True
        if addressed == False: #Create node
            node = Node(event.getNodeId(), self.vscp)
            node.receiveEvent(event)
            self.nodes.append(node)
            logger.info("New Node found. ID = {0}".format(event.getNodeId()))
                
    def getNode(self, nodeId):
        """Return the object of node with specific address
        
        None is returned in case of no node found
        """
        for node in self.nodes:
            if node.id == nodeId:
                return node
        self.discover(startNodeId = nodeId, stopNodeId = nodeId)
        for node in self.nodes:
            if node.id == nodeId:
                return node
        return None
    
    def getNumberOfNode(self, ):
        return self.nodes.count
    
        
    
    def discover(self, fast = False, startNodeId = 1, stopNodeId = 254):
        """This function is designed in order to discover all nodes on the network
        Discover can be done in two different ways:
        - Slow discover (fast = False), where function send a probe for each address
        - Fast discover (fast = True), where function will send a <Who is there?> message
        """
        if startNodeId<1:
            raise ValueError("StartNodeId must be greater than 0")
        if stopNodeId>254:
            raise ValueError("StopNodeId must be less than 255")
        if startNodeId>stopNodeId:
            raise ValueError("StartNodeId must be less or at least equal to StopNodeId")
        if fast:
            self.vscp.sendSimpleEvent(vscp_class=0,
                                      vscp_type = 31,
                                      vscp_data= [255])
        else:
            for nodeId in range(startNodeId, stopNodeId+1):
                for trial in range(3):
                    logger.info("Looking for node #{0}, trial {1}".format(nodeId, trial))
                    self.vscp.sendSimpleEvent(vscp_class = 0,
                                              vscp_type = 2,
                                              vscp_data = [nodeId])
                    sleep(1)
                    try:
                        for node in self.nodes:
                            if nodeId == node.id:
                                raise ValueError()
                    except ValueError:
                        break
                        
                
            
        