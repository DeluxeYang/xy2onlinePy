import socket
import socketserver

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        print("from conn:",self.request)

s1=socketserver.ThreadingTCPServer(("127.0.0.1",9999), MyServer)
s1.serve_forever()