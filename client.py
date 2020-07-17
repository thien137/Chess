import socket
import pickle
class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = '192.168.0.16'
		self.port = 5590
		self.addr = (self.server, self.port)
	
	def connect(self):
		self.client.connect(self.addr)

	def sendall(self, data):
		self.client.sendall(pickle.dumps(data))
	def recv(self, bytes):
		return self.client.recv(bytes)