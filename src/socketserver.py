import django
from django.utils import simplejson
from django.core.handlers.wsgi import WSGIHandler
from tornado import websocket
from tornado import web, ioloop, httpserver, wsgi
from neji.models import CodeSession
from wsgi import application as django_wsgi_app

__author__ = 'mturilin'


def create_error(message):
    return simplejson.dumps({
        "command": "error",
        "message": message
    })

sessions = dict()

class Session(object):
    sockets = []
    text = ""
    range = None
    top_row = 0
    code_session = None

    def __init__(self, session_id):
        self.session_id = session_id

    def save_text(self, text):
        if not self.code_session:
            query_set = CodeSession.objects.filter(session_id=self.session_id)
            if query_set.exists():
                self.code_session = query_set[0]
            else:
                self.code_session = CodeSession()
                self.code_session.session_id = self.session_id

        self.text = text
        self.code_session.code = text
        self.code_session.save()


class NejiWebSocket(websocket.WebSocketHandler):
    session_id = None

    def open(self):
        print "WebSocket opened, request=", repr(self.request)


    def get_session(self):
        return sessions.setdefault(self.session_id, Session(self.session_id))

    def send_all_but_me(self, message):
        session_sockets = self.get_session().sockets
        for socket in session_sockets:
            if socket != self:
                socket.write_message(message)

    def on_message(self, message):
        print "Message: " + message

        message_dict = simplejson.loads(message)
        if "command" not in message_dict:
            self.write_message(create_error("'command' is not found in the message!"))

        command = message_dict['command']

        if command == "register":
            self.session_id = message_dict["session_id"]
            session = self.get_session()
            print "New connection to session, session_id=", self.session_id
            session_sockets = session.sockets
            session_sockets.append(self)

            print "Number of clients: %d" % len(session_sockets)

            if session.text:
                self.write_message(simplejson.dumps({
                    "command": "initial_text",
                    "text": session.text
                }))

            if session.range:
                self.write_message(simplejson.dumps({
                    "command": "initial_range",
                    "range": session.range,
                    "top_row": session.top_row
                }))

        elif command == "update":
            session = self.get_session()
            if "text" in message_dict:
                session.save_text(message_dict["text"])
                del message_dict["text"]

            if "range" in message_dict:
                session.range = message_dict["range"]

            if "top_row" in message_dict:
                session.tow_row = message_dict["top_row"]

            self.send_all_but_me(simplejson.dumps(message_dict))

        elif command == "run":
            self.send_all_but_me(message)
        else:
            self.write_message(create_error("Unknown command '%s'" % command))

    def on_close(self):
        print "WebSocket closed, session_id=", self.session_id, ", request=", repr(self.request)
        session_sockets = self.get_session().sockets
        session_sockets.remove(self)
        if not session_sockets:
            self.delete_session()

    def delete_session(self):
        print "Deleting session: " + self.session_id
        del sessions[self.session_id]


application = web.Application([
    (r'/ws', NejiWebSocket),
])

if __name__ == "__main__":
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8888)
    ioloop.IOLoop.instance().start()