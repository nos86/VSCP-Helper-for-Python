from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import threading
import logging

logger = logging.getLogger(__name__)
welcomeMessages = None

class createAnswer:
    def __init__(self, message):
        self.is_binary = False
        self.data = message

class TestWebSocket(WebSocket):
    def __init__(self, *args):
        global welcomeMessages
        super(TestWebSocket, self).__init__(*args)
        if welcomeMessages is not None:
            self.response = welcomeMessages.split("|")
            threading.Timer(0.01,
                            self.received_message).start() 
        else:
            self.response = []       
    
    def received_message(self, message = createAnswer(b"Dummy")):
        data = message.data.decode('ascii')
        if data[0] == '^':
            self.response = data[1:].split("|")
        elif len(self.response)==0:
            self.send(message.data, message.is_binary)
        else:
            if len(self.response[0])>1:
                self.send(self.response[0], message.is_binary)
            self.response = self.response[1:]

    def opened(self):
        logger.info("Server is opened")
        
    def closed(self, code, reason=None):
        self.connected = False
        logger.info("Server is closed")

class TestServer:
    def __init__(self, hostname='127.0.0.1', port=8080, welcomeMessage = None):
        self.server = make_server(hostname,\
                             port,\
                             server_class=WSGIServer,\
                             handler_class=WebSocketWSGIRequestHandler,\
                             app=WebSocketWSGIApplication(handler_cls=TestWebSocket)\
                             )
        global welcomeMessages
        welcomeMessages = welcomeMessage
        self.server.initialize_websockets_manager()
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
    

    def shutdown(self):
        self.server.server_close()
        self.server.shutdown()
        

if __name__ == "__main__":
    a = TestServer()
