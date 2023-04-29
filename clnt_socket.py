import socket
class Clnt:
    def __init__(self):
        self.s=socket.socket()
        self.s.connect(('127.0.0.1',5000))
clnt=Clnt()
