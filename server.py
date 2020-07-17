import socket
from _thread import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind(('192.168.0.16', 5590))
except socket.error as e:
	str(e)

moves = [["WPawn1", 0, 0]]
player = False
buffering = moves.copy()
connections = []
s.listen(2)

print("Waiting for a conection, Server Started")

def threaded_client2(conn):
	global moves
	conn[-2].sendall(bytes("W", "utf-8"))
	conn[-1].sendall(bytes("B", "utf-8"))
	while True:
		try:
			for i in range(1,3):
				data = pickle.loads(conn[-i].recv(150))
				if not data:
					pass
				else:
					if data != moves:
						moves = data
						if data != buffering:
							break
						else:
							pass
			for i in range(1,3):
				conn[-i].sendall(pickle.dumps(moves))
		except:
			pass

def threaded_client(conn):
	global moves
	global player
	global connections
	if player == False:
		conn.sendall(bytes("W", "utf-8"))
		player = True
	elif player == True:
		conn.sendall(bytes("B", "utf-8"))
	while True:
		try:
			for connection in connections:
				data = pickle.loads(connection.recv(4096))
				if not data:
					pass
				else:
					if data != moves:
						moves = data
						break
			for connection in connections:
				connection.sendall(pickle.dumps(moves))
		except:
			pass

def threaded_client3(conn):
	global moves
	global player
	global connections
	if player == False:
		conn.sendall(bytes("W", "utf-8"))
		player = True
	elif player == True:
		conn.sendall(bytes("B", "utf-8"))
		player = False
	while True:
		try:
			if player == False:
				for connection in connections:
					data = pickle.loads(connection.recv(4096))
					if not data:
						pass
					else:
						if data != moves:
							moves = data
							if data != buffering:
								break
							else:
								pass
				for connection in connections:
					connection.sendall(pickle.dumps(moves))

		except:
			pass
while True:
	conn, addr = s.accept()
	connections.append(conn)
	print("Connected to:", addr)
	if len(connections) % 2 == 0 and len(connections) != 0:
		start_new_thread(threaded_client2, (connections,))
