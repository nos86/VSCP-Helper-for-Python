from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import threading
import logging

logger = logging.getLogger(__name__)


class TestWebSocket(WebSocket):
    def __init__(self, *args):
        self.response = []
        super(TestWebSocket, self).__init__(*args)
    
    def received_message(self, message):
        data = message.data.decode('ascii')
        if data[0] == '^' and len(data)>1:
            self.response = data[1:].split("|")
        elif len(self.response)==0:
            self.send(message.data, message.is_binary)
        else:
            self.send(self.response[0], message.is_binary)
            self.response = self.response[1:]

        
    def closed(self, code, reason=None):
        self.connected = False
        logger.info("WebSocket closed")

class TestServer:
    def __init__(self, hostname='127.0.0.1', port=8080):
        self.server = make_server(hostname,\
                             port,\
                             server_class=WSGIServer,\
                             handler_class=WebSocketWSGIRequestHandler,\
                             app=WebSocketWSGIApplication(handler_cls=TestWebSocket)\
                             )
        self.server.initialize_websockets_manager()
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
    

    def shutdown(self):
        self.server.server_close()
        self.server.shutdown()
        

if __name__ == "__main__":
    a = TestServer()
