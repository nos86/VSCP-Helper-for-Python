import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import threading

class websocket_server():
    def __init__(self):
        log.startLogging(sys.stdout)
    
        self.factory = WebSocketServerFactory("ws://localhost:8080", debug=False)
        self.factory.protocol = MyServerProtocol
        self.port = reactor.listenTCP(8080, self.factory)
        self.t = threading.Thread(target=self.listener)
        self.t.setDaemon(True)
        self.t.start()
    
    def listener(self):
        reactor.run(installSignalHandlers=0)
        
    def stop(self):
        self.port.stopListening()
        reactor.removeAll()  
        reactor.stop()
        self.t.join(timeout=5)
    
    def __del__(self):
        print("Addio")

class MyServerProtocol(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
