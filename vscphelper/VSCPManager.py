from vscphelper.vscplib import *

class Node:
    """This class contains and handles all information about node
    """
    def __init__(self, nodeId, Manager):
        self.id = nodeId
        self.manager = Manager

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
        pass
    
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
            for nodeId in range(startNodeId, stopNodeId):
                for trial in range(3):
                    self.vscp.sendSimpleEvent(vscp_class = 0,
                                              vscp_type = 2,
                                              vscp_data = [nodeId])
                    sleep(1)
                    for node in self.nodes:
                        if i == node.id:
                            continue
                        
                
            
        