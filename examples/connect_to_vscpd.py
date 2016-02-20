from vscphelper.vscplib import vscp
from vscphelper.VSCPManager import Manager

if __name__=="__main__":
    connection = vscp('192.168.1.133')
    manager = Manager(connection)
    manager.discover(stopNodeId = 10)
    print("Number of node found: {}".format(len(manager.nodes))