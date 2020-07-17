from tkinter import *
from PIL import ImageTk, Image
from ChessImages import images
import socket
import pickle
from client import Network
import threading
import sys
#INTERFACE 

class Pieces(Frame):

#PIECES PLACEMENT
	def reset(self):
		#BASE POSITIONS OF PIECES
		self.base_pieces_positions = {"WPawn1": [0, 6], "WPawn2" : [1, 6],  "WPawn3" : [2, 6], "WPawn4" : [3, 6], "WPawn5" : [4, 6], "WPawn6" : [5, 6], "WPawn7" : [6, 6], "WPawn8" : [7, 6], "WRook1" : [0, 7], "WRook2" : [7, 7], "WKnight1" : [1, 7], "WKnight2" : [6, 7], "WBishop1" : [2, 7], "WBishop2" : [5, 7], "WQueen1" : [3, 7], "WKing1" : [4, 7], "BPawn1": [0, 1], "BPawn2" : [1, 1],  "BPawn3" : [2, 1], "BPawn4" : [3, 1], "BPawn5" : [4, 1], "BPawn6" : [5, 1], "BPawn7" : [6, 1], "BPawn8" : [7, 1], "BRook1" : [0, 0], "BRook2" : [7, 0], "BKnight1" : [1, 0], "BKnight2" : [6, 0], "BBishop1" : [2, 0], "BBishop2" : [5, 0], "BQueen1" : [3, 0], "BKing1" : [4, 0]}

		#RETURNING THE PIECES POSITIONS TO THE ORIGINAL POSITIONS
		self.pieces_positions = self.base_pieces_positions.copy()
		
		#RETURNING THE TURN TO WHITE
		self.turn = "W"
		
		#REMOVING ANY MARKERS OR HIGHLIGHTS
		self.del_markers()

		#DELETING ANY PROMOTED PAWNS
		for item in self.canvas.find_withtag("fake"):
			self.canvas.delete(item)
		
		#MOVING CHESSPIECES BACK TO ORIGINAL POSITIONS
		for item in self.canvas.find_withtag("ChessPiece"):
			self.canvas.move(item, self.base_pieces_positions[self.canvas.gettags(item)[1]][0] * 80 + 40 - self.canvas.coords(item)[0], self.base_pieces_positions[self.canvas.gettags(item)[1]][1] * 80 + 40 - self.canvas.coords(item)[1])
		
		#REMOVING THE CHECKMATE BANNER
		self.del_checkmate()
		
		#RESETTING THE COLOR CHANGES TO THE CHESSBOARD CAUSED BY CHECK
		self.reset_chessboard_colors()
		
		#RESETTING THE RECORD 
		self.moves = [[["WPawn1", 0, 0]]]	
		self.history = [[["WPawn1", 0, 0]]]
		self.stalemate = 0
		#SENDING RESET MESSAGE TO SERVER SO THAT THE OTHER PLAYER RESETS THEIR BOARD AS WELL
		self.history.append([["RESET", self.player]])
		
		self.moved = True

	def server_reset(self):
		#BASE POSITIONS OF PIECES
		self.base_pieces_positions = {"WPawn1": [0, 6], "WPawn2" : [1, 6],  "WPawn3" : [2, 6], "WPawn4" : [3, 6], "WPawn5" : [4, 6], "WPawn6" : [5, 6], "WPawn7" : [6, 6], "WPawn8" : [7, 6], "WRook1" : [0, 7], "WRook2" : [7, 7], "WKnight1" : [1, 7], "WKnight2" : [6, 7], "WBishop1" : [2, 7], "WBishop2" : [5, 7], "WQueen1" : [3, 7], "WKing1" : [4, 7], "BPawn1": [0, 1], "BPawn2" : [1, 1],  "BPawn3" : [2, 1], "BPawn4" : [3, 1], "BPawn5" : [4, 1], "BPawn6" : [5, 1], "BPawn7" : [6, 1], "BPawn8" : [7, 1], "BRook1" : [0, 0], "BRook2" : [7, 0], "BKnight1" : [1, 0], "BKnight2" : [6, 0], "BBishop1" : [2, 0], "BBishop2" : [5, 0], "BQueen1" : [3, 0], "BKing1" : [4, 0]}
		
		#RETURNING HTE PIECES POSITIONS TO THE ORIGINAL POSITIONS
		self.pieces_positions = self.base_pieces_positions.copy()
		
		#RETURNING THE TURN TO WHITE
		self.turn = "W"
		self.stalemate = 0
		#DELETING ANY MARKERS OR HIGHLIGHTS
		self.del_markers()
		for item in self.canvas.find_withtag("fake"):
			self.canvas.delete(item)
		
		#MOVING CHESSPIECES BACK TO ORIGINAL POSITIONS
		for item in self.canvas.find_withtag("ChessPiece"):
			self.canvas.move(item, self.base_pieces_positions[self.canvas.gettags(item)[1]][0] * 80 + 40 - self.canvas.coords(item)[0], self.base_pieces_positions[self.canvas.gettags(item)[1]][1] * 80 + 40 - self.canvas.coords(item)[1])

		#REMOVING THE CHECKMATE/STALEMATE BANNER
		self.del_checkmate()
		
		#RESETTING THE COLOR CHANGES TO THE CHESSBOARD CAUSED BY CHECK
		self.reset_chessboard_colors()
		
		#RESETTING THE RECORD
		self.moves = [[["WPawn1", 0, 0]]]
		self.history = [[["WPawn1", 0, 0]]]

	def place(self):

		#ESSENTIALLY CREATING THE IMAGES ON THE BOARD
		self.BPawn1 = self.canvas.create_image(self.pieces_positions["BPawn1"][0] * 80 + 40, self.pieces_positions["BPawn1"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn1", "B", "BPawn"))
		self.BPawn2 = self.canvas.create_image(self.pieces_positions["BPawn2"][0] * 80 + 40, self.pieces_positions["BPawn2"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn2", "B", "BPawn")) 
		self.BPawn3 = self.canvas.create_image(self.pieces_positions["BPawn3"][0] * 80 + 40, self.pieces_positions["BPawn3"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn3", "B", "BPawn"))   
		self.BPawn4 = self.canvas.create_image(self.pieces_positions["BPawn4"][0] * 80 + 40, self.pieces_positions["BPawn4"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn4", "B", "BPawn")) 
		self.BPawn5 = self.canvas.create_image(self.pieces_positions["BPawn5"][0] * 80 + 40, self.pieces_positions["BPawn5"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn5", "B", "BPawn")) 
		self.BPawn6 = self.canvas.create_image(self.pieces_positions["BPawn6"][0] * 80 + 40, self.pieces_positions["BPawn6"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn6", "B", "BPawn")) 
		self.BPawn7 = self.canvas.create_image(self.pieces_positions["BPawn7"][0] * 80 + 40, self.pieces_positions["BPawn7"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn7", "B", "BPawn")) 
		self.BPawn8 = self.canvas.create_image(self.pieces_positions["BPawn8"][0] * 80 + 40, self.pieces_positions["BPawn8"][1] * 80 + 40, image = self.BPawn, anchor = CENTER, tag = ("ChessPiece", "BPawn8", "B", "BPawn")) 
		self.BKnight1 = self.canvas.create_image(self.pieces_positions["BKnight1"][0] * 80 + 40, self.pieces_positions["BKnight1"][1] * 80 + 40, image = self.BKnight, anchor = CENTER, tag = ("ChessPiece", "BKnight1", "B", "BKnight")) 
		self.BKnight2 = self.canvas.create_image(self.pieces_positions["BKnight2"][0] * 80 + 40, self.pieces_positions["BKnight2"][1] * 80 + 40, image = self.BKnight, anchor = CENTER, tag = ("ChessPiece", "BKnight2", "B", "BKnight")) 
		self.BRook1 = self.canvas.create_image(self.pieces_positions["BRook1"][0] * 80 + 40, self.pieces_positions["BRook1"][1] * 80 + 40, image = self.BRook, anchor = CENTER, tag = ("ChessPiece", "BRook1", "B", "BRook")) 
		self.BRook2 = self.canvas.create_image(self.pieces_positions["BRook2"][0] * 80 + 40, self.pieces_positions["BRook2"][1] * 80 + 40, image = self.BRook, anchor = CENTER, tag = ("ChessPiece", "BRook2", "B", "BRook")) 
		self.BBishop1 = self.canvas.create_image(self.pieces_positions["BBishop1"][0] * 80 + 40, self.pieces_positions["BBishop1"][1] * 80 + 40, image = self.BBishop, anchor = CENTER, tag = ("ChessPiece", "BBishop1", "B", "BBishop")) 
		self.BBishop2 = self.canvas.create_image(self.pieces_positions["BBishop2"][0] * 80 + 40, self.pieces_positions["BBishop2"][1] * 80 + 40, image = self.BBishop, anchor = CENTER, tag = ("ChessPiece", "BBishop2", "B", "BBishop")) 
		self.BQueen1 = self.canvas.create_image(self.pieces_positions["BQueen1"][0] * 80 + 40, self.pieces_positions["BQueen1"][1] * 80 + 40, image = self.BQueen, anchor = CENTER, tag = ("ChessPiece", "BQueen1", "B", "BQueen")) 
		self.BKing1 = self.canvas.create_image(self.pieces_positions["BKing1"][0] * 80 + 40, self.pieces_positions["BKing1"][1] * 80 + 40, image = self.BKing, anchor = CENTER, tag = ("ChessPiece", "BKing1", "B", "BKing"))
		self.WPawn1 = self.canvas.create_image(self.pieces_positions["WPawn1"][0] * 80 + 40, self.pieces_positions["WPawn1"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn1", "W", "WPawn"))
		self.WPawn2 = self.canvas.create_image(self.pieces_positions["WPawn2"][0] * 80 + 40, self.pieces_positions["WPawn2"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn2", "W", "WPawn")) 
		self.WPawn3 = self.canvas.create_image(self.pieces_positions["WPawn3"][0] * 80 + 40, self.pieces_positions["WPawn3"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn3", "W", "WPawn"))   
		self.WPawn4 = self.canvas.create_image(self.pieces_positions["WPawn4"][0] * 80 + 40, self.pieces_positions["WPawn4"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn4", "W", "WPawn")) 
		self.WPawn5 = self.canvas.create_image(self.pieces_positions["WPawn5"][0] * 80 + 40, self.pieces_positions["WPawn5"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn5", "W", "WPawn")) 
		self.WPawn6 = self.canvas.create_image(self.pieces_positions["WPawn6"][0] * 80 + 40, self.pieces_positions["WPawn6"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn6", "W", "WPawn")) 
		self.WPawn7 = self.canvas.create_image(self.pieces_positions["WPawn7"][0] * 80 + 40, self.pieces_positions["WPawn7"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn7", "W", "WPawn")) 
		self.WPawn8 = self.canvas.create_image(self.pieces_positions["WPawn8"][0] * 80 + 40, self.pieces_positions["WPawn8"][1] * 80 + 40, image = self.WPawn, anchor = CENTER, tag = ("ChessPiece", "WPawn8", "W", "WPawn")) 
		self.WKnight1 = self.canvas.create_image(self.pieces_positions["WKnight1"][0] * 80 + 40, self.pieces_positions["WKnight1"][1] * 80 + 40, image = self.WKnight, anchor = CENTER, tag = ("ChessPiece", "WKnight1", "W", "WKnight")) 
		self.WKnight2 = self.canvas.create_image(self.pieces_positions["WKnight2"][0] * 80 + 40, self.pieces_positions["WKnight2"][1] * 80 + 40, image = self.WKnight, anchor = CENTER, tag = ("ChessPiece", "WKnight2", "W", "WKnight")) 
		self.WRook1 = self.canvas.create_image(self.pieces_positions["WRook1"][0] * 80 + 40, self.pieces_positions["WRook1"][1] * 80 + 40, image = self.WRook, anchor = CENTER, tag = ("ChessPiece", "WRook1", "W", "WRook")) 
		self.WRook2 = self.canvas.create_image(self.pieces_positions["WRook2"][0] * 80 + 40, self.pieces_positions["WRook2"][1] * 80 + 40, image = self.WRook, anchor = CENTER, tag = ("ChessPiece", "WRook2", "W", "WRook")) 
		self.WBishop1 = self.canvas.create_image(self.pieces_positions["WBishop1"][0] * 80 + 40, self.pieces_positions["WBishop1"][1] * 80 + 40, image = self.WBishop, anchor = CENTER, tag = ("ChessPiece", "WBishop1", "W", "WBishop")) 
		self.WBishop2 = self.canvas.create_image(self.pieces_positions["WBishop2"][0] * 80 + 40, self.pieces_positions["WBishop2"][1] * 80 + 40, image = self.WBishop, anchor = CENTER, tag = ("ChessPiece", "WBishop2", "W", "WBishop")) 
		self.WQueen1 = self.canvas.create_image(self.pieces_positions["WQueen1"][0] * 80 + 40, self.pieces_positions["WQueen1"][1] * 80 + 40, image = self.WQueen, anchor = CENTER, tag = ("ChessPiece", "WQueen1", "W", "WQueen")) 
		self.WKing1 = self.canvas.create_image(self.pieces_positions["WKing1"][0] * 80 + 40, self.pieces_positions["WKing1"][1] * 80 + 40, image = self.WKing, anchor = CENTER, tag = ("ChessPiece", "WKing1", "W", "WKing"))  
		
		#LIFTING THE IMAGES OF THE CHESSPIECES SO THAT THEY DONT END UP BELOW THE BOARD OR MARKERS
		for piece in self.canvas.find_withtag("ChessPiece"):
			self.canvas.lift(piece)

	def reset_chessboard_colors(self):
		#RESET CHESSBOARD COLORS
		for x in range(8):
			
			for y in range(8):
				
				if (x+y) % 2 == 1: #ODD VALUES ARE BLACK
					self.canvas.itemconfig(self.canvas.find_withtag("" + str(x) + ", " + str(y))[0], fill = "#b58863")
				
				if (x+y) % 2 == 0: #EVEN VALUES ARE WHITE
					self.canvas.itemconfig(self.canvas.find_withtag("" + str(x) + ", " + str(y))[0], fill = "#f0d9b5")

	def undo(self):
		if len(self.moves) > 1:
			#CHECK EACH MOVEMENT IN THE LAST ENTRY TO THE RECORD OF MOVES (AKA SELF.MOVES)
			for piece in self.moves[-1]:
				
				#IF THE PIECE IS A PROMOTED PAWN AND THUS HAS NO MOVEMENT VALUES, DELETE IT
				if "fake" in self.canvas.gettags(piece[0]):
					self.canvas.delete(piece[0])
					del self.pieces_positions[piece[0]]
				
				#MOVE THE PIECES TO THEIR ORIGINAL POSITIONS
				else:
					self.canvas.move(piece[0], -piece[1] * 80, -piece[2] * 80)
					self.pieces_positions[piece[0]] = [int(self.canvas.coords(self.canvas.find_withtag(piece[0])[0])[0]/80), int(self.canvas.coords(self.canvas.find_withtag(piece[0])[0])[1]/80)]
			
			#DELETE ANY MARKERS
			self.del_markers()

			#TELL THE SERVER ABOUT THE UNDO SO THAT THE OPPONENT'S BOARD IS CHANGED
			self.history.append([["UNDO", self.player]])
			self.moved = True
			
			#REMOVE THAT MOVEMENT FROM THE RECORD
			self.moves.remove(self.moves[-1])
			self.stalemate -= 1
			#CHANGING THE TURN
			if self.turn == "W":
				self.turn = "B"
			elif self.turn == "B":
				self.turn = "W"
			
			#REMOVING ANY CHECKMATE BANNER
			self.del_checkmate()
			
			#CHECKING FOR A CHECK, RESETTING THE CHESSBOARD COLORS, THEN HIGHLIGHTING THE KING IF CHECKED
			self.check_attack_positions(thepositions = self.pieces_positions)
			self.reset_chessboard_colors()
			self.actually_check_for_check()
		
	def del_markers(self): #DELETING MARKERS
		for item in self.canvas.find_withtag("marker"):
			self.canvas.delete(item)

	def del_checkmate(self): #DELETING CHECKMATE BANNER
		if len(self.canvas.find_withtag("Checkmate")) > 0:
			self.canvas.delete(self.canvas.find_withtag("Checkmate")[0])
		if len(self.canvas.find_withtag("Stalemate")) > 0:
			self.canvas.delete(self.canvas.find_withtag("Stalemate")[0])

	def server_undo(self):#CHECK EACH MOVEMENT IN THE LAST ENTRY TO THE RECORD OF MOVES (AKA SELF.MOVES), USED BY THE OTHER END OF THE UNDO, SO THAT IT DOESNT SEND BACK ANOTHER UNDO MESSAGE
		if len(self.moves) > 1:	
			for piece in self.moves[-1]:
				
				#IF THE PIECE IS A PROMOTED PAWN AND THUS HAS NO MOVEMENT VALUES, DELETE IT
				if "fake" in self.canvas.gettags(piece[0]):
					self.canvas.delete(piece[0])
					del self.pieces_positions[piece[0]]
				
				#MOVE THE PIECES TO THEIR ORIGINAL POSITIONS
				else:
					self.canvas.move(piece[0], -piece[1] * 80, -piece[2] * 80)
					self.pieces_positions[piece[0]] = [int(self.canvas.coords(self.canvas.find_withtag(piece[0])[0])[0]/80), int(self.canvas.coords(self.canvas.find_withtag(piece[0])[0])[1]/80)]
			
			#DELETE ANY MARKERS
			self.del_markers()

			#RECORD UNDO CHANGE
			self.history.append([["UNDO", self.player]])
			
			#REMOVE THAT MOVEMENT FROM THE RECORD
			self.moves.remove(self.moves[-1])
			
			#CHANGING THE TURN
			if self.turn == "W":
				self.turn = "B"
			elif self.turn == "B":
				self.turn = "W"
			
			#REMOVING ANY CHECKMATE BANNER
			self.del_checkmate()
			self.stalemate -= 1
			#CHECKING FOR A CHECK, RESETTING THE CHESSBOARD COLORS, THEN HIGHLIGHTING THE KING IF CHECKED
			self.check_attack_positions(thepositions = self.pieces_positions)
			self.reset_chessboard_colors()
			self.actually_check_for_check()
	
	def movement_marker(self, pieces): #HIGHLIGHT MOVEMENT
		#DELETE PREVIOUS MOVEMENT
		for item in self.canvas.find_withtag("marker"):
			self.canvas.delete(item)
		
		#CREATE HIGHLIGHTS
		for piece in pieces:
			if piece[1] < 8 and piece[1] > -8 and piece[2] < 8 and piece[2] > -8:
				x, y = self.pieces_positions[piece[0]]
				w, z = self.moves[-1][0][1], self.moves[-1][0][2]
				if x >= 0 and y < 8 and x < 8 and y >= 0:
					self.canvas.itemconfig(self.canvas.find_withtag("" + str(x) + ", " + str(y))[0], fill = "#e8e18e")
					if len(pieces) == 2:
						if pieces[0][0][0] == pieces[1][0][0]:
							pass
					elif x - w >= 0 and y - z < 8 and x - w < 8 and y - z >= 0:
						self.canvas.itemconfig(self.canvas.find_withtag("" + str(x-w) + ", " + str(y-z))[0], fill = "#b8af4e")

# MOUSE MOVEMENT AND MOVEMENT OF PIECES
	def mouse_down(self, event):
		self.moving = False
		if self.player != self.turn and self.player != "S":
			self.can_Click2 = False
		elif self.player == self.turn or self.player == "S":
			self.can_Click2 = True
		if self.canvas.gettags(CURRENT)[1][0] == self.turn and self.can_Click == True and self.can_Click2 == True:
			self.lastx = event.x
			self.lasty = event.y
			self.basex = self.canvas.coords(CURRENT)[0]
			self.basey = self.canvas.coords(CURRENT)[1]
			obstacle = []
			for x in self.pieces_positions.values():
				r, y = x
				obstacle.append([r, y])

			black_obstacles = []
			white_obstacles = []
			for key in self.pieces_positions:
				if key[0] == "B":
					black_obstacles.append(self.pieces_positions[key])
				if key[0] == "W":
					white_obstacles.append(self.pieces_positions[key])

			if self.canvas.gettags(CURRENT)[1][1:-1] == "Queen":
				x = self.queensAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")
			if self.canvas.gettags(CURRENT)[1][1:-1] == "Bishop":
				x = self.bishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")
			if self.canvas.gettags(CURRENT)[1][1:-1] == "Rook":
				x = self.rooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")
			if self.canvas.gettags(CURRENT)[1][1:-1] == "Knight":
				x = self.knightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:	
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")
			if self.canvas.gettags(CURRENT)[1][1:-1] == "King":
				x = self.kingsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")
			if self.canvas.gettags(CURRENT)[1][1:-1] == "Pawn":
				x = self.pawnsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = CURRENT)
				for position in x:
					if self.check_for_check(xposition = position, current = CURRENT) == False:
						self.canvas.create_oval(position[0] * 80 + 40 - 10, position[1] * 80 + 40 - 10, position[0] * 80 + 40 + 10, position[1] * 80 + 40 + 10, fill = "#138209", tag = "marker")

	def mouse_Move(self, event):
		if self.player != self.turn and self.player != "S":
			self.can_Click2 = False
		elif self.player == self.turn or self.player == "S":
			self.can_Click2 = True
		if "immovable" in self.canvas.gettags(CURRENT):
			pass
		elif self.can_Click == True and self.can_Click2 == True:
			if self.canvas.gettags(CURRENT)[1][0] == self.turn:
				event.widget.move(CURRENT, event.x - self.lastx, event.y - self.lasty)
				self.lastx = event.x
				self.lasty = event.y
				self.moving = True
			self.canvas.lift(CURRENT)

	def mouse_Up(self, event):
		if self.player != self.turn and self.player != "S":
			self.can_Click2 = False
		elif self.player == self.turn or self.player == "S":
			self.can_Click2 = True
		if "immovable" in self.canvas.gettags(CURRENT):
			pass
		elif self.canvas.gettags(CURRENT)[1][0] == self.turn and self.can_Click == True and self.can_Click2 == True and self.moving == True:
			YUM = True
			self.lastx = int(event.x/80)
			self.lasty = int(event.y/80)
			self.basex = int(self.basex/80)
			self.basey = int(self.basey/80)
			items = []
			for item in self.canvas.find_withtag("marker"):
				items.append([int(self.canvas.coords(item)[0]/80), int(self.canvas.coords(item)[1]/80)])
			# KILLING OTHER PIECES
			if [self.lastx, self.lasty] in items:
				self.movement = []
				Castled = False
				for piece in self.canvas.find_withtag("ChessPiece"):
					if self.canvas.gettags(piece)[1] != self.canvas.gettags(CURRENT)[1]:
						if self.canvas.gettags(piece)[1][1:-1] == "Rook" and self.canvas.gettags(CURRENT)[1][1:-1] == "King" and [int(self.canvas.coords(piece)[0]/80), int(self.canvas.coords(piece)[1]/80)] == [int(self.lastx), int(self.lasty)]:
							if self.canvas.gettags(piece)[1][-1] == "1":
								self.movement.append([self.canvas.gettags(piece)[1], 3, 0])
								self.movement.append([self.canvas.gettags(CURRENT)[1], 2, 0])
								self.canvas.move(self.canvas.find_withtag(self.canvas.gettags(CURRENT)[1])[0], 160 + 40 - self.canvas.coords(CURRENT)[0], self.lasty * 80 + 40 - self.canvas.coords(CURRENT)[1])
								self.canvas.move(piece, 3 * 80, 0)
								self.pieces_positions[self.canvas.gettags(piece)[1]] = [int(self.canvas.coords(piece)[0]/80), int(self.canvas.coords(piece)[1]/80)]
								self.pieces_positions[self.canvas.gettags(CURRENT)[1]] = [int(self.canvas.coords(CURRENT)[0]/80), int(self.canvas.coords(CURRENT)[1]/80)]
								Castled = True
							if self.canvas.gettags(piece)[1][-1] == "2":
								self.movement.append([self.canvas.gettags(piece)[1], -2, 0])
								self.movement.append([self.canvas.gettags(CURRENT)[1], -1, 0])
								self.canvas.move(self.canvas.find_withtag(self.canvas.gettags(CURRENT)[1])[0], 480 + 40 - self.canvas.coords(CURRENT)[0], self.lasty * 80 + 40 - self.canvas.coords(CURRENT)[1])
								self.canvas.move(piece, -2 * 80, 0)
								self.pieces_positions[self.canvas.gettags(piece)[1]] = [int(self.canvas.coords(piece)[0]/80), int(self.canvas.coords(piece)[1]/80)]
								self.pieces_positions[self.canvas.gettags(CURRENT)[1]] = [int(self.canvas.coords(CURRENT)[0]/80), int(self.canvas.coords(CURRENT)[1]/80)]
								Castled = True
				#CHANGING POSITION IN DATABASE
				if Castled == False:
					self.pieces_positions[self.canvas.gettags(CURRENT)[1]] = [self.lastx, self.lasty]
				#MOVING THE PIECE
				if Castled == False:
					self.movement.append([self.canvas.gettags(CURRENT)[1], self.lastx - self.basex, self.lasty - self.basey])
				for piece in self.canvas.find_withtag("ChessPiece"):
					if self.canvas.gettags(piece)[1] != self.canvas.gettags(CURRENT)[1]:
						if [int(self.canvas.coords(piece)[0]/80), int(self.canvas.coords(piece)[1]/80)] == [int(self.lastx), int(self.lasty)]:
							self.stalemate = 0
							self.movement.append([self.canvas.gettags(piece)[1], 10000/80, 10000/80])
							self.canvas.move(piece, 10000, 10000)
							self.pieces_positions[self.canvas.gettags(piece)[1]] = [int(self.canvas.coords(piece)[0]/80), int(self.canvas.coords(piece)[1]/80)]
							break
				#IF PAWN AT OTHER END, REPLACE And En possant
				if self.canvas.gettags(CURRENT)[1][1: -1] == "Pawn":
					self.stalemate = 0
					if self.canvas.gettags(CURRENT)[1][0] == "W":
						if len(self.moves) <= 2:
							pass
						elif self.moves[-1][0][0][1:-1] == "Pawn" and abs(self.moves[-1][0][2]) == 2:
							c, s = self.pieces_positions[self.canvas.gettags(CURRENT)[1]] 
							r, y = self.pieces_positions[self.moves[-1][0][0]]
							if c == r and s == y - 1:
								self.movement.append([self.canvas.gettags(self.moves[-1][0][0])[1], 10000/80, 10000/80])
								self.canvas.move(self.canvas.find_withtag(self.moves[-1][0][0])[0], 10000, 10000)
						if self.pieces_positions[self.canvas.gettags(CURRENT)[1]][1] == 0:
							self.pop_up(current = self.canvas.gettags(CURRENT)[1])
							self.YUM = False
					if self.canvas.gettags(CURRENT)[1][0] == "B":
						if len(self.moves) <= 2:
							pass
						elif self.moves[-1][0][0][1:-1] == "Pawn" and abs(self.moves[-1][0][2]) == 2:
							c, s = self.pieces_positions[self.canvas.gettags(CURRENT)[1]] 
							r, y = self.pieces_positions[self.moves[-1][0][0]]
							if c == r and s == y + 1:
								self.movement.append([self.canvas.gettags(self.moves[-1][0][0])[1], 10000/80, 10000/80])
								self.canvas.move(self.canvas.find_withtag(self.moves[-2][0]), 10000, 10000)
						if self.pieces_positions[self.canvas.gettags(CURRENT)[1]][1] == 7:
							self.pop_up(current = self.canvas.gettags(CURRENT)[1])
							self.YUM = False
				self.moves.append(self.movement)
				self.history.append(self.movement)
				if Castled == False:
					self.canvas.move(self.canvas.gettags(CURRENT)[1], self.lastx * 80 + 40 - self.canvas.coords(CURRENT)[0], self.lasty * 80 + 40 - self.canvas.coords(CURRENT)[1])
				self.moving = False
				if self.YUM == True:
					self.moved = True
				# CHANGING TURNS
				self.movement_marker(self.movement)
				if self.turn == "W":
					self.turn = "B"
				elif self.turn == "B":
					self.turn = "W"
				#CHECKING
				self.check_attack_positions(thepositions = self.pieces_positions)
				self.reset_chessboard_colors()
				self.movement_marker(self.movement)
				self.actually_check_for_check()
				self.check_for_checkmate()
				self.check_stalemate()	

			else:			
				self.canvas.move(self.canvas.gettags(CURRENT)[1], self.basex * 80 + 40 - self.canvas.coords(CURRENT)[0], self.basey * 80 + 40 - self.canvas.coords(CURRENT)[1])
		for item in self.canvas.find_withtag("marker"):
			self.canvas.delete(item)
# CHECKING IF THE KING IS CHECKED
	def actually_check_for_check(self):
		if self.wking_check == True:
			self.canvas.itemconfig(self.canvas.find_withtag("" + str(self.pieces_positions["WKing1"][0]) + ", " + str(self.pieces_positions["WKing1"][1]))[0], fill = "brown")
			return True
		if self.bking_check == True:
			self.canvas.itemconfig(self.canvas.find_withtag("" + str(self.pieces_positions["BKing1"][0]) + ", " + str(self.pieces_positions["BKing1"][1]))[0], fill = "brown")
			return True

	def check_stalemate(self):
		if self.actually_check_for_check() == True:
			self.stalemate = 0
		else:
			self.stalemate += 1
		if self.stalemate == 50:
			self.canvas.lift(self.canvas.create_image(320, 320, image = self.stalemate_image, anchor = CENTER, tag = "Stalemate"))
	
	def check_for_checkmate(self):
		total_positions = 0
		obstacle = []
		for x in self.pieces_positions.values():
			r, y = x
			obstacle.append([r, y])
		black_obstacles = []
		white_obstacles = []
		for key in self.pieces_positions:
			if key[0] == "B":
				black_obstacles.append(self.pieces_positions[key])
			if key[0] == "W":
				white_obstacles.append(self.pieces_positions[key])
		if self.turn == "W":
			for piece in self.canvas.find_withtag("W"):
				if self.pieces_positions[self.canvas.gettags(piece)[1]][0] < 8 and self.pieces_positions[self.canvas.gettags(piece)[1]][0] >= 0 and self.pieces_positions[self.canvas.gettags(piece)[1]][1] < 8 and self.pieces_positions[self.canvas.gettags(piece)[1]][1] >= 0:		
					if self.canvas.gettags(piece)[1][1:-1] == "Queen":
						x = self.queensAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Bishop":
						x = self.bishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Rook":
						x = self.rooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Knight":
						x = self.knightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:	
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "King":
						x = self.kingsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Pawn":
						x = self.pawnsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
		if self.turn == "B":
			for piece in self.canvas.find_withtag("B"): 
				if self.pieces_positions[self.canvas.gettags(piece)[1]][0] < 8 and self.pieces_positions[self.canvas.gettags(piece)[1]][0] >= 0 and self.pieces_positions[self.canvas.gettags(piece)[1]][1] < 8 and self.pieces_positions[self.canvas.gettags(piece)[1]][1] >= 0:
					if self.canvas.gettags(piece)[1][1:-1] == "Queen":
						x = self.queensAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Bishop":
						x = self.bishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Rook":
						x = self.rooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Knight":
						x = self.knightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:	
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "King":
						x = self.kingsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1
					if self.canvas.gettags(piece)[1][1:-1] == "Pawn":
						x = self.pawnsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = piece)
						for position in x:
							if self.check_for_check(xposition = position, current = piece) == False:
								total_positions += 1					
		if total_positions == 0:
			if self.actually_check_for_check() == True:
				self.canvas.lift(self.canvas.create_image(320, 320, image = self.checkmate, anchor = CENTER, tag = "Checkmate"))
			else:
				self.canvas.lift(self.canvas.create_image(320, 320, image = self.stalemate_image, anchor = CENTER, tag = "Stalemate"))
	
	def check_attack_positions(self, thepositions):
		obstacle = []
		for x in thepositions.values():
			r, y = x
			obstacle.append([r, y])
		black_obstacles = []
		white_obstacles = []
		for key in thepositions:
			if key[0] == "B":
				black_obstacles.append(thepositions[key])
			if key[0] == "W":
				white_obstacles.append(thepositions[key])
		BATTACKPOSITIONS = []
		WATTACKPOSITIONS = []

		self.wking_check = False
		self.bking_check = False


		r_q = thepositions["WKing1"][0]
		c_q = thepositions["WKing1"][1]

		Wking_vertical_positions = self.rooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("WKing1")[1])
		Wking_diagonal_positions = self.bishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("WKing1")[1])
		Wking_knight_positions = self.knightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("WKing1")[1])
		Wking_pawn_positions = [[r_q - 1, c_q - 1], [r_q + 1, c_q - 1]]

		for piece in (self.canvas.find_withtag("BQueen") + self.canvas.find_withtag("BBishop")):
			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Wking_diagonal_positions:
				self.wking_check = True
		for piece in (self.canvas.find_withtag("BKnight")):
			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Wking_knight_positions:
				self.wking_check = True
		for piece in (self.canvas.find_withtag("BRook") + self.canvas.find_withtag("BQueen")):
			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Wking_vertical_positions:
				self.wking_check = True
		for position in self.pieces_positions:
			if position[:-1] == "BPawn":
				if self.pieces_positions[position]in Wking_pawn_positions:
					self.wking_check = True

		r_q = thepositions["BKing1"][0]
		c_q = thepositions["BKing1"][1]

		Bking_vertical_positions = self.rooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("BKing1")[1])
		Bking_diagonal_positions = self.bishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("BKing1")[1])
		Bking_knight_positions = self.knightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = self.canvas.gettags("BKing1")[1])
		Bking_pawn_positions = [[r_q - 1, c_q + 1], [r_q + 1, c_q + 1]]
		for piece in (self.canvas.find_withtag("WQueen") + self.canvas.find_withtag("WBishop")):

			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Bking_diagonal_positions:
				self.bking_check = True
		for piece in (self.canvas.find_withtag("WKnight")):
			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Bking_knight_positions:
				self.bking_check = True
		for piece in (self.canvas.find_withtag("WRook") + self.canvas.find_withtag("WQueen")):
			x = self.canvas.gettags(piece)[1]
			if self.pieces_positions[x] in Bking_vertical_positions:
				self.bking_check = True
		for position in self.pieces_positions:
			if position[:-1] == "WPawn":
				if self.pieces_positions[position] in Bking_pawn_positions:
					self.bking_check = True

#HYPOTHETICALLY CHECKING
	def hypothetical_check_attack_positions(self, thepositions, current):
		hypothetical_wking_check = False
		hypothetical_bking_check = False
		
		for y in thepositions:
			if thepositions[self.canvas.gettags(current)[1]] == thepositions[y] and self.canvas.gettags(current)[1] != y:
				thepositions[y] = [2000, 2000]

		obstacle = []
		for x in thepositions.values():
			r, y = x
			obstacle.append([r, y])
		black_obstacles = []
		white_obstacles = []
		for key in thepositions:
			if key[0] == "B":
				black_obstacles.append(thepositions[key])
			if key[0] == "W":
				white_obstacles.append(thepositions[key])
		BATTACKPOSITIONS = []
		WATTACKPOSITIONS = []

		c_q = thepositions["WKing1"][0]
		r_q = thepositions["WKing1"][1]

		Wking_vertical_positions = self.hypotheticalrooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("WKing1")[2]])
		Wking_diagonal_positions = self.hypotheticalbishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("WKing1")[2]])
		Wking_knight_positions = self.hypotheticalknightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("WKing1")[2]])
		Wking_pawn_positions = [[c_q - 1, r_q - 1], [c_q + 1, r_q - 1]]
		Wking_king_positions = [[c_q - 1, r_q - 1], [c_q + 1, r_q + 1], [c_q - 1, r_q + 1], [c_q + 1, r_q - 1], [c_q, r_q + 1], [c_q, r_q - 1], [c_q + 1, r_q], [c_q - 1, r_q]]

		for piece in (self.canvas.find_withtag("BQueen") + self.canvas.find_withtag("BBishop")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Wking_diagonal_positions:
				hypothetical_wking_check = True
		for piece in (self.canvas.find_withtag("BKnight")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Wking_knight_positions:
				hypothetical_wking_check = True
		for piece in (self.canvas.find_withtag("BRook") + self.canvas.find_withtag("BQueen")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Wking_vertical_positions:
				hypothetical_wking_check = True
		for position in thepositions:
			if position[:-1] == "BPawn":
				if thepositions[position]in Wking_pawn_positions:
					hypothetical_wking_check = True
		for position in thepositions:
			if position[:-1] == "BKing":
				if thepositions[position] in Wking_king_positions:
					hypothetical_wking_check = True

		c_q = thepositions["BKing1"][0]
		r_q = thepositions["BKing1"][1]

		Bking_vertical_positions = self.hypotheticalrooksAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("BKing1")[2]])
		Bking_diagonal_positions = self.hypotheticalbishopsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("BKing1")[2]])
		Bking_knight_positions = self.hypotheticalknightsAttack(n = 7, obstacles = obstacle, bobstacles = black_obstacles, wobstacles = white_obstacles, current = [c_q, r_q, self.canvas.gettags("BKing1")[2]])
		Bking_pawn_positions = [[c_q - 1, r_q + 1], [c_q + 1, r_q + 1]]
		Bking_king_positions = [[c_q - 1, r_q - 1], [c_q + 1, r_q + 1], [c_q - 1, r_q + 1], [c_q + 1, r_q - 1], [c_q, r_q + 1], [c_q, r_q - 1], [c_q + 1, r_q], [c_q - 1, r_q]]

		for piece in (self.canvas.find_withtag("WQueen") + self.canvas.find_withtag("WBishop")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Bking_diagonal_positions:
				hypothetical_bking_check = True
		for piece in (self.canvas.find_withtag("WKnight")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Bking_knight_positions:
				hypothetical_bking_check = True
		for piece in (self.canvas.find_withtag("WRook") + self.canvas.find_withtag("WQueen")):
			x = self.canvas.gettags(piece)[1]
			if thepositions[x] in Bking_vertical_positions:
				hypothetical_bking_check = True
		for position in thepositions:
			if position[:-1] == "WPawn":
				if thepositions[position]in Bking_pawn_positions:
					hypothetical_bking_check = True
		for position in thepositions:
			if position[:-1] == "WKing":
				if thepositions[position] in Bking_king_positions:
					hypothetical_bking_check = True

		return [hypothetical_wking_check, hypothetical_bking_check]

	def check_for_check(self, xposition, current):
		Is_it_Check = False
		hypothetical_positions = self.pieces_positions.copy()
		hypothetical_positions[self.canvas.gettags(current)[1]] = xposition
		if self.hypothetical_check_attack_positions(thepositions = hypothetical_positions, current = current)[0] == True and self.canvas.gettags(current)[2] == "W":
			Is_it_Check = True
		if self.hypothetical_check_attack_positions(thepositions = hypothetical_positions, current = current)[1] == True and self.canvas.gettags(current)[2] == "B":
			Is_it_Check = True
		return Is_it_Check

	def hypotheticalbishopsAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = current[0]  
		r_q = current[1]

		W = False
		B = False

		if current[2] == "W":
			W = True
		if current[2] == "B":
			B = True

		diagonal_positions = []

	    #OBSTACLES
		bottom_right = [None, None]
		top_right = [None, None]
		bottom_left = [None, None]
		top_left = [None, None]
	    #OBSTACLES

	    #GETTING CLOSEST OBSTACLES
		for obstacle in obstacles:
			c, r = obstacle
			if r - r_q > 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_left
				if z == None and m == None:
					bottom_left = [c, r]
				elif r - r_q < m - r_q and c - c_q > z - c_q:
					bottom_left = [c, r]
			if r - r_q < 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_left
				if z == None and m == None:
					top_left = [c, r]
				elif r - r_q > m - r_q and c - c_q > z - c_q:
					top_left = [c, r]
			if r - r_q > 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_right
				if z == None and m == None:
					bottom_right = [c, r]
				elif r - r_q < m - r_q and c - c_q < z - c_q:
					bottom_right = [c, r]
			if r - r_q < 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_right
				if z == None and m == None:
					top_right = [c, r]
				elif r - r_q < m - r_q and c - c_q < z - c_q:
					top_right = [c, r]

		if W == True:
			if top_left in bobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in bobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in bobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in bobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1
		if B == True:
			if top_left in wobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in wobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in wobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in wobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1

	    #GETTING ALL THE POSITIONS
		for i in range(1, n):

			if r_q - i >= 0 and c_q + i <= n:
				if top_right[0] == None:
					diagonal_positions.append([c_q + i, r_q - i])
				elif r_q - i > top_right[1] and c_q + i < top_right[0]:
					diagonal_positions.append([c_q + i, r_q - i])
			if r_q + i <= n and c_q + i <= n:
				if bottom_right[1] == None:
					diagonal_positions.append([c_q + i, r_q + i])
				elif r_q + i < bottom_right[1] and c_q + i < bottom_right[0]:
					diagonal_positions.append([c_q + i, r_q + i])
			if r_q - i >= 0 and c_q - i >= 0:
				if top_left[1] == None:
					diagonal_positions.append([c_q - i, r_q - i])
				elif r_q - i > top_left[1] and c_q - i > top_left[0]:
					diagonal_positions.append([c_q - i, r_q - i])
			if r_q + i <= n and c_q - i >= 0:
				if bottom_left[1] == None:
					diagonal_positions.append([c_q - i, r_q + i])
				elif r_q + i < bottom_left[1] and c_q - i > bottom_left[0]:
					diagonal_positions.append([c_q - i, r_q + i])
		return diagonal_positions

	def hypotheticalknightsAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = current[0]
		r_q = current[1]

		W = False
		B = False

		if current[2] == "W":
			W = True
		if current[2] == "B":
			B = True

		positions = [[c_q - 2, r_q - 1], [c_q - 2, r_q + 1], [c_q - 1, r_q + 2], [c_q + 1, r_q + 2], [c_q + 2, r_q + 1], [c_q + 2, r_q - 1], [c_q - 1, r_q - 2], [c_q + 1, r_q - 2]]
		remove_from_positions = []
		for position in positions:
			if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
				remove_from_positions.append(position)
		if W == True:
			for obstacle in wobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		if B == True:
			for obstacle in bobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		for position in remove_from_positions:
			if position in positions:
				positions.remove(position)
		return positions	

	def hypotheticalrooksAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = current[0]
		r_q = current[1]

		W = False
		B = False

		if current[2] == "W":
			W = True
		if current[2] == "B":
			B = True
		
		vertical_positions = []
		horizontal_positions = []

	    #OBSTACLES
		right = [None, None]
		left = [None, None]
		top = [None, None]
		bottom = [None, None]
	    #OBSTACLES
	    #GETTING CLOSEST OBSTACLES
		for obstacle in obstacles:
			c, r = obstacle
			if c == c_q and r < r_q:
				z, m = top
				if z == None and m == None:
					top = [c, r]
				elif r - r_q > m - r_q:
					top = [c, r]
			if c == c_q and r > r_q:
				z, m = bottom
				if z == None and m == None:
					bottom = [c, r]
				elif r - r_q < m - r_q:
					bottom = [c, r]
			if r == r_q and c > c_q:
				z, m = right
				if z == None and m == None:
					right = [c, r]
				elif c - c_q < z - c_q:
					right = [c, r]
			if r == r_q and c < c_q:
				z, m = left
				if z == None and m == None:
					left = [c, r]
				elif c - c_q > z - c_q:
					left = [c, r]

		if W == True:
			if top in bobstacles:
				top[1] -= 1
			if bottom in bobstacles:
				bottom[1] += 1
			if right in bobstacles:
				right[0] += 1
			if left in bobstacles:
				left[0] -= 1
			
		if B == True:
			if top in wobstacles:
				top[1] -= 1
			if bottom in wobstacles:
				bottom[1] += 1
			if right in wobstacles:
				right[0] += 1
			if left in wobstacles:
				left[0] -= 1

	    #GETTING ALL THE POSITIONS
		for i in range(1, n):
			if c_q + i <= n:
				if right[0] == None:
					horizontal_positions.append([c_q + i, r_q])
				elif c_q + i < right[0]:
					horizontal_positions.append([c_q + i, r_q])
			if c_q - i >= 0:
				if left[0] == None:
					horizontal_positions.append([c_q - i, r_q])
				elif c_q - i > left[0]:
					horizontal_positions.append([c_q - i, r_q])
			if r_q - i >= 0:
				if top[1] == None:
					vertical_positions.append([c_q, r_q - i])
				elif r_q - i > top[1]:
					vertical_positions.append([c_q, r_q - i])
			if r_q + i <= n:
				if bottom[1] == None:
					vertical_positions.append([c_q, r_q + i])
				elif r_q + i < bottom[1]:
					vertical_positions.append([c_q, r_q + i])
			
		return vertical_positions + horizontal_positions

#INDIVIDUAL PIECE MOVEMENT RESTRICTIONS
	
	def pawnsAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = int(self.canvas.coords(current)[0]/80)
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False
		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True
		positions = []
		if (c_q * 80 + 40, r_q * 80 + 40) == (self.base_pieces_positions[self.canvas.gettags(current)[1]][0] * 80 + 40, self.base_pieces_positions[self.canvas.gettags(current)[1]][1] * 80 + 40):
			if self.canvas.gettags(current)[1][0] == "B":
				if [c_q, r_q + 2] in obstacles or [c_q, r_q + 1] in obstacles:
					pass
				else:
					positions.append([c_q, r_q + 2])
			if self.canvas.gettags(current)[1][0] == "W":
				if [c_q, r_q - 2] in obstacles or [c_q, r_q - 1] in obstacles:
					pass
				else:
					positions.append([c_q, r_q - 2])		
		if self.canvas.gettags(current)[1][0] == "B":
			if [c_q, r_q + 1] in obstacles:
				pass
			else:
				positions.append([c_q, r_q + 1])
		if self.canvas.gettags(current)[1][0] == "W":
			if [c_q, r_q - 1] in obstacles:
				pass
			else:
				positions.append([c_q, r_q - 1])
		for obstacle in obstacles:
			r, y = obstacle
			if self.canvas.gettags(current)[1][0] == "B" and ([r, y] == [c_q - 1, r_q + 1] or [r, y] == [c_q + 1, r_q + 1]): 
				positions.append([r, y])
			if self.canvas.gettags(current)[1][0] == "W" and ([r, y] == [c_q - 1, r_q - 1] or [r, y] == [c_q + 1, r_q - 1]): 
				positions.append([r, y])
		remove_from_positions = []
		for position in positions:
			if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
				remove_from_positions.append(position)
		if len(self.moves) == 0:
			pass
		elif self.moves[-1][0][0][1:-1] == "Pawn" and abs(self.moves[-1][0][2]) == 2:
			c, s = self.pieces_positions[self.canvas.gettags(current)[1]] 
			r, y = self.pieces_positions[self.moves[-1][0][0]]
			if s == y and abs(c - r) == 1:
				if W == True:
					if abs(c) - abs(r) < 0:
						positions.append([c_q + 1, r_q - 1])
					if abs(c) - abs(r) > 0:
						positions.append([c_q - 1, r_q - 1])
				if B == True:
					if abs(c) - abs(r) < 0:
						positions.append([c_q + 1, r_q + 1])
					if abs(c) - abs(r) > 0:
						positions.append([c_q - 1, r_q + 1])
		if W == True:
			for obstacle in wobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		if B == True:
			for obstacle in bobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		for position in remove_from_positions:
			if position in positions:
				positions.remove(position)
		return positions

	def kingsAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = int(self.canvas.coords(current)[0]/80)
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False

		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True

		right = [None, None]
		left = [None, None]

		for obstacle in obstacles:
			c, r = obstacle
			if r == r_q and c > c_q:
				z, m = right
				if z == None and m == None:
					right = [c, r]
				elif c - c_q < z - c_q:
					right = [c, r]
			if r == r_q and c < c_q:
				z, m = left
				if z == None and m == None:
					left = [c, r]
				elif c - c_q > z - c_q:
					left = [c, r]

		positions = [[c_q + 1, r_q - 1], [c_q + 1, r_q + 1], [c_q - 1, r_q + 1], [c_q - 1, r_q - 1], [c_q, r_q + 1], [c_q, r_q - 1], [c_q + 1, r_q], [c_q - 1, r_q]]
		remove_from_positions = []
		for position in positions:
			if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
				remove_from_positions.append(position)
		if W == True:
			if len(self.moves) != 0:
				WRook1 = True
				WRook2 = True
			else:
				WRook1 = False
				WRook2 = False
			for obstacle in wobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
			if self.wking_check == False:
				for movement in self.moves:
					if "WRook1" in movement[0] or self.pieces_positions["WRook1"] != left or self.canvas.gettags(current)[1] in movement[0]: 
						WRook1 = False
					if "WRook2" in movement[0] or self.pieces_positions["WRook2"] != right or self.canvas.gettags(current)[1] in movement[0]: 
						WRook2 = False
				if self.check_for_check(xposition = [0, 7], current = "WKing1") == True or self.check_for_check(xposition = [1, 7], current = "WKing1") == True or self.check_for_check(xposition = [2, 7], current = "WKing1") == True or self.check_for_check(xposition = [3, 7], current = "WKing1") == True:
					WRook1 = False
				if self.check_for_check(xposition = [5, 7], current = "WKing1") == True or self.check_for_check(xposition = [6, 7], current = "WKing1") == True or self.check_for_check(xposition = [7, 7], current = "WKing1") == True:
					WRook2 = False
				if WRook1 == True:
					positions.append(self.pieces_positions["WRook1"])
				if WRook2 == True:
					positions.append(self.pieces_positions["WRook2"])
		if B == True:
			BRook1 = True
			BRook2 = True
			for obstacle in bobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
			if self.bking_check == False:
				for movement in self.moves:
					if "BRook1" in movement[0] or self.pieces_positions["BRook1"] != left or self.canvas.gettags(current)[1] in movement[0]: 
						BRook1 = False
					if "BRook2" in movement[0] or self.pieces_positions["BRook2"] != right or self.canvas.gettags(current)[1] in movement[0]:
						BRook2 = False			
				if self.check_for_check(xposition = [0, 0], current = "BKing1") == True or self.check_for_check(xposition = [1, 0], current = "BKing1") == True or self.check_for_check(xposition = [2, 0], current = "BKing1") == True or self.check_for_check(xposition = [3, 0], current = "BKing1") == True:
					BRook1 = False
				if self.check_for_check(xposition = [5, 0], current = "BKing1") == True or self.check_for_check(xposition = [6, 0], current = "BKing1") == True or self.check_for_check(xposition = [7, 0], current = "BKing1") == True:
					BRook2 = False
				if BRook1 == True:
					positions.append(self.pieces_positions["BRook1"])
				if BRook2 == True:
					positions.append(self.pieces_positions["BRook2"])
		for position in remove_from_positions:
			if position in positions:
				positions.remove(position)
		return positions

	def knightsAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = int(self.canvas.coords(current)[0]/80)
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False

		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True

		positions = [[c_q - 2, r_q - 1], [c_q - 2, r_q + 1], [c_q - 1, r_q + 2], [c_q + 1, r_q + 2], [c_q + 2, r_q + 1], [c_q + 2, r_q - 1], [c_q - 1, r_q - 2], [c_q + 1, r_q - 2]]
		remove_from_positions = []
		for position in positions:
			if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
				remove_from_positions.append(position)
		if W == True:
			for obstacle in wobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		if B == True:
			for obstacle in bobstacles:
				for position in positions:
					if position == obstacle:
						remove_from_positions.append(position)
		for position in remove_from_positions:
			if position in positions:
				positions.remove(position)
		return positions	

	def bishopsAttack(self, n, obstacles, bobstacles, wobstacles, current):

		c_q = int(self.canvas.coords(current)[0]/80)  
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False

		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True

		diagonal_positions = []

	    #OBSTACLES
		bottom_right = [None, None]
		top_right = [None, None]
		bottom_left = [None, None]
		top_left = [None, None]
	    #OBSTACLES

	    #GETTING CLOSEST OBSTACLES
		for obstacle in obstacles:
			c, r = obstacle
			if r - r_q > 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_left
				if z == None and m == None:
					bottom_left = [c, r]
				elif r - r_q < m - r_q and c - c_q > z - c_q:
					bottom_left = [c, r]
			if r - r_q < 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_left
				if z == None and m == None:
					top_left = [c, r]
				elif r - r_q > m - r_q and c - c_q > z - c_q:
					top_left = [c, r]
			if r - r_q > 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_right
				if z == None and m == None:
					bottom_right = [c, r]
				elif r - r_q < m - r_q and c - c_q < z - c_q:
					bottom_right = [c, r]
			if r - r_q < 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_right
				if z == None and m == None:
					top_right = [c, r]
				elif r - r_q > m - r_q and c - c_q < z - c_q:
					top_right = [c, r]

		if W == True:
			if top_left in bobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in bobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in bobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in bobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1
		if B == True:
			if top_left in wobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in wobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in wobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in wobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1

	    #GETTING ALL THE POSITIONS
		for i in range(1, 8):

			if r_q - i >= 0 and c_q + i <= n:
				if top_right[0] == None:
					diagonal_positions.append([c_q + i, r_q - i])
				elif r_q - i > top_right[1] and c_q + i < top_right[0]:
					diagonal_positions.append([c_q + i, r_q - i])
			if r_q + i <= n and c_q + i <= n:
				if bottom_right[1] == None:
					diagonal_positions.append([c_q + i, r_q + i])
				elif r_q + i < bottom_right[1] and c_q + i < bottom_right[0]:
					diagonal_positions.append([c_q + i, r_q + i])
			if r_q - i >= 0 and c_q - i >= 0:
				if top_left[1] == None:
					diagonal_positions.append([c_q - i, r_q - i])
				elif r_q - i > top_left[1] and c_q - i > top_left[0]:
					diagonal_positions.append([c_q - i, r_q - i])
			if r_q + i <= n and c_q - i >= 0:
				if bottom_left[1] == None:
					diagonal_positions.append([c_q - i, r_q + i])
				elif r_q + i < bottom_left[1] and c_q - i > bottom_left[0]:
					diagonal_positions.append([c_q - i, r_q + i])
		return diagonal_positions

	def rooksAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = int(self.canvas.coords(current)[0]/80)  
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False

		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True
		
		vertical_positions = []
		horizontal_positions = []

	    #OBSTACLES
		right = [None, None]
		left = [None, None]
		top = [None, None]
		bottom = [None, None]
	    #OBSTACLES
	    #GETTING CLOSEST OBSTACLES
		for obstacle in obstacles:
			c, r = obstacle
			if c == c_q and r < r_q:
				z, m = top
				if z == None and m == None:
					top = [c, r]
				elif r - r_q > m - r_q:
					top = [c, r]
			if c == c_q and r > r_q:
				z, m = bottom
				if z == None and m == None:
					bottom = [c, r]
				elif r - r_q < m - r_q:
					bottom = [c, r]
			if r == r_q and c > c_q:
				z, m = right
				if z == None and m == None:
					right = [c, r]
				elif c - c_q < z - c_q:
					right = [c, r]
			if r == r_q and c < c_q:
				z, m = left
				if z == None and m == None:
					left = [c, r]
				elif c - c_q > z - c_q:
					left = [c, r]

		if W == True:
			if top in bobstacles:
				top[1] -= 1
			if bottom in bobstacles:
				bottom[1] += 1
			if right in bobstacles:
				right[0] += 1
			if left in bobstacles:
				left[0] -= 1
			
		if B == True:
			if top in wobstacles:
				top[1] -= 1
			if bottom in wobstacles:
				bottom[1] += 1
			if right in wobstacles:
				right[0] += 1
			if left in wobstacles:
				left[0] -= 1

	    #GETTING ALL THE POSITIONS
		for i in range(1, 8):
			if c_q + i <= n:
				if right[0] == None:
					horizontal_positions.append([c_q + i, r_q])
				elif c_q + i < right[0]:
					horizontal_positions.append([c_q + i, r_q])
			if c_q - i >= 0:
				if left[0] == None:
					horizontal_positions.append([c_q - i, r_q])
				elif c_q - i > left[0]:
					horizontal_positions.append([c_q - i, r_q])
			if r_q - i >= 0:
				if top[1] == None:
					vertical_positions.append([c_q, r_q - i])
				elif r_q - i > top[1]:
					vertical_positions.append([c_q, r_q - i])
			if r_q + i <= n:
				if bottom[1] == None:
					vertical_positions.append([c_q, r_q + i])
				elif r_q + i < bottom[1]:
					vertical_positions.append([c_q, r_q + i])
			
		return vertical_positions + horizontal_positions

	def queensAttack(self, n, obstacles, bobstacles, wobstacles, current):
		c_q = int(self.canvas.coords(current)[0]/80)  
		r_q = int(self.canvas.coords(current)[1]/80)

		W = False
		B = False

		if self.canvas.gettags(current)[1][0] == "W":
			W = True
		if self.canvas.gettags(current)[1][0] == "B":
			B = True
		
		vertical_positions = []
		horizontal_positions = []
		diagonal_positions = []

	    #OBSTACLES
		bottom_right = [None, None]
		right = [None, None]
		top_right = [None, None]
		bottom_left = [None, None]
		left = [None, None]
		top_left = [None, None]
		top = [None, None]
		bottom = [None, None]
	    #OBSTACLES
		
	    #GETTING CLOSEST OBSTACLES
		for obstacle in obstacles:
			c, r = obstacle
			if c == c_q and r < r_q:
				z, m = top
				if z == None and m == None:
					top = [c, r]
				elif r - r_q > m - r_q:
					top = [c, r]
			if c == c_q and r > r_q:
				z, m = bottom
				if z == None and m == None:
					bottom = [c, r]
				elif r - r_q < m - r_q:
					bottom = [c, r]
			if r == r_q and c > c_q:
				z, m = right
				if z == None and m == None:
					right = [c, r]
				elif c - c_q < z - c_q:
					right = [c, r]
			if r == r_q and c < c_q:
				z, m = left
				if z == None and m == None:
					left = [c, r]
				elif c - c_q > z - c_q:
					left = [c, r]
			if r - r_q > 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_left
				if z == None and m == None:
					bottom_left = [c, r]
				elif r - r_q < m - r_q and c - c_q > z - c_q:
					bottom_left = [c, r]
			if r - r_q < 0 and c - c_q < 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_left
				if z == None and m == None:
					top_left = [c, r]
				elif r - r_q > m - r_q and c - c_q > z - c_q:
					top_left = [c, r]
			if r - r_q > 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = bottom_right
				if z == None and m == None:
					bottom_right = [c, r]
				elif r - r_q < m - r_q and c - c_q < z - c_q:
					bottom_right = [c, r]
			if r - r_q < 0 and c - c_q > 0 and abs(r - r_q) == abs(c - c_q):
				z, m = top_right
				if z == None and m == None:
					top_right = [c, r]
				elif r - r_q > m - r_q and c - c_q < z - c_q:
					top_right = [c, r]

		if W == True:
			if top in bobstacles:
				top[1] -= 1
			if bottom in bobstacles:
				bottom[1] += 1
			if right in bobstacles:
				right[0] += 1
			if left in bobstacles:
				left[0] -= 1
			if top_left in bobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in bobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in bobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in bobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1

		if B == True:
			if top in wobstacles:
				top[1] -= 1
			if bottom in wobstacles:
				bottom[1] += 1
			if right in wobstacles:
				right[0] += 1
			if left in wobstacles:
				left[0] -= 1
			if top_left in wobstacles:
				top_left[1] -= 1
				top_left[0] -= 1
			if top_right in wobstacles:
				top_right[1] -= 1
				top_right[0] += 1
			if bottom_left in wobstacles:
				bottom_left[1] += 1
				bottom_left[0] -= 1
			if bottom_right in wobstacles:
				bottom_right[1] += 1
				bottom_right[0] += 1

	    #GETTING ALL THE POSITIONS
		
		for i in range(1, 8):
			if c_q + i <= n:
				if right[0] == None:
					horizontal_positions.append([c_q + i, r_q])
				elif c_q + i < right[0]:
					horizontal_positions.append([c_q + i, r_q])
			if c_q - i >= 0:
				if left[0] == None:
					horizontal_positions.append([c_q - i, r_q])
				elif c_q - i > left[0]:
					horizontal_positions.append([c_q - i, r_q])
			if r_q - i >= 0:
				if top[1] == None:
					vertical_positions.append([c_q, r_q - i])
				elif r_q - i > top[1]:
					vertical_positions.append([c_q, r_q - i])
			if r_q + i <= n:
				if bottom[1] == None:
					vertical_positions.append([c_q, r_q + i])
				elif r_q + i < bottom[1]:
					vertical_positions.append([c_q, r_q + i])
			if r_q - i >= 0 and c_q + i <= n:
				if top_right[0] == None:
					diagonal_positions.append([c_q + i, r_q - i])
				elif r_q - i > top_right[1] and c_q + i < top_right[0]:
					diagonal_positions.append([c_q + i, r_q - i])
			if r_q + i <= n and c_q + i <= n:
				if bottom_right[1] == None:
					diagonal_positions.append([c_q + i, r_q + i])
				elif r_q + i < bottom_right[1] and c_q + i < bottom_right[0]:
					diagonal_positions.append([c_q + i, r_q + i])
			if r_q - i >= 0 and c_q - i >= 0:
				if top_left[1] == None:
					diagonal_positions.append([c_q - i, r_q - i])
				elif r_q - i > top_left[1] and c_q - i > top_left[0]:
					diagonal_positions.append([c_q - i, r_q - i])
			if r_q + i <= n and c_q - i >= 0:
				if bottom_left[1] == None:

					diagonal_positions.append([c_q - i, r_q + i])
				elif r_q + i < bottom_left[1] and c_q - i > bottom_left[0]:
					diagonal_positions.append([c_q - i, r_q + i])
		return vertical_positions + horizontal_positions + diagonal_positions
#PAWN CONVERSION
	def pop_up(self, current):
		self.can_Click = False
		pawn_color = current[0]
		self.Choose_Conversion = Toplevel()
		if pawn_color == "W":
			Rook_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.WRook, command = lambda : self.convert_rook(current = current, side = pawn_color))
			Bishop_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.WBishop, command = lambda : self.convert_bishop(current = current, side = pawn_color))
			Queen_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.WQueen, command = lambda : self.convert_queen(current = current, side = pawn_color))
			Knight_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.WKnight, command = lambda : self.convert_knight(current = current, side = pawn_color))
			Rook_Button.grid(row = 0, column = 0)
			Bishop_Button.grid(row = 0, column = 1)
			Queen_Button.grid(row = 0, column = 2)
			Knight_Button.grid(row = 0, column = 3)
		if pawn_color == "B":
			Rook_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.BRook, command = lambda : self.convert_rook(current = current, side = pawn_color))
			Bishop_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.BBishop, command = lambda : self.convert_bishop(current = current, side = pawn_color))
			Queen_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.BQueen, command = lambda : self.convert_queen(current = current, side = pawn_color))
			Knight_Button = Button(self.Choose_Conversion, padx = 50, pady = 50, highlightthickness = 0, borderwidth = 0, image = self.BKnight, command = lambda : self.convert_knight(current = current, side = pawn_color))
			Rook_Button.grid(row = 0, column = 0)
			Bishop_Button.grid(row = 0, column = 1)
			Queen_Button.grid(row = 0, column = 2)
			Knight_Button.grid(row = 0, column = 3)

	def convert_queen(self, current, side):
		if side == "W":
			x = len(self.canvas.find_withtag("WQueen")) + 1
			self.pieces_positions["WQueen" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.WQueen, anchor = CENTER, tag = ("ChessPiece", "WQueen" + str(x), "WQueen", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["WQueen" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]			
			self.moved = True
		if side == "B":
			x = len(self.canvas.find_withtag("BQueen")) + 1
			self.pieces_positions["BQueen" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.BQueen, anchor = CENTER, tag = ("ChessPiece", "BQueen" + str(x), "BQueen", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["BQueen" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		self.YUM = True
		self.can_Click = True
		self.Choose_Conversion.destroy()
		self.check_attack_positions(thepositions = self.pieces_positions)
		self.reset_chessboard_colors()
		self.actually_check_for_check()
		self.check_for_checkmate()
	def convert_rook(self, current, side):
		if side == "W":
			x = len(self.canvas.find_withtag("WRook")) + 1
			self.pieces_positions["WRook" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.WRook, anchor = CENTER, tag = ("ChessPiece", "WRook" + str(x), "WRook", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["WRook" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		if side == "B":
			x = len(self.canvas.find_withtag("BRook")) + 1
			self.pieces_positions["BRook" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.BRook, anchor = CENTER, tag = ("ChessPiece", "BRook" + str(x), "BRook", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["BRook" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True		
		self.YUM = True
		self.can_Click = True
		self.Choose_Conversion.destroy()
		self.check_attack_positions(thepositions = self.pieces_positions)
		self.reset_chessboard_colors()
		self.actually_check_for_check()
		self.check_for_checkmate()
	def convert_bishop(self, current, side):
		if side == "W":
			x = len(self.canvas.find_withtag("WBishop")) + 1
			self.pieces_positions["WBishop" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.WBishop, anchor = CENTER, tag = ("ChessPiece", "WBishop" + str(x), "WBishop", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["WBishop" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		if side == "B":
			x = len(self.canvas.find_withtag("BBishop")) + 1
			self.pieces_positions["BBishop" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.BBishop, anchor = CENTER, tag = ("ChessPiece", "BBishop" + str(x), "BBishop", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["BBishop" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		self.YUM = True
		self.can_Click = True
		self.Choose_Conversion.destroy()
		self.check_attack_positions(thepositions = self.pieces_positions)
		self.reset_chessboard_colors()
		self.actually_check_for_check()
		self.check_for_checkmate()
	def convert_knight(self, current, side):
		if side == "W":
			x = len(self.canvas.find_withtag("WKnight")) + 1
			self.pieces_positions["WKnight" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.WKnight, anchor = CENTER, tag = ("ChessPiece", "WKnight" + str(x), "WKnight", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["WKnight" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		if side == "B":
			x = len(self.canvas.find_withtag("BKnight")) + 1
			self.pieces_positions["BKnight" + str(x)] = [self.pieces_positions[current][0], self.pieces_positions[current][1]]
			self.canvas.create_image(self.pieces_positions[current][0] * 80 + 40, self.pieces_positions[current][1] * 80 + 40, image = self.BKnight, anchor = CENTER, tag = ("ChessPiece", "BKnight" + str(x), "BKnight", "fake")) 
			self.canvas.move(current, 10000, 10000)
			self.moves[-1].append([self.canvas.gettags(current)[1], 10000/80, 10000/80])
			self.moves[-1].append(["BKnight" + str(x), self.pieces_positions[current][0], self.pieces_positions[current][1]])
			self.pieces_positions[self.canvas.gettags(current)[1]] = [int(self.canvas.coords(self.canvas.gettags(current)[1])[0]/80), int(self.canvas.coords(self.canvas.gettags(current)[1])[1]/80)]
			self.moved = True
		self.YUM = True
		self.can_Click = True
		self.Choose_Conversion.destroy()
		self.check_attack_positions(thepositions = self.pieces_positions)
		self.reset_chessboard_colors()
		self.actually_check_for_check()
		self.check_for_checkmate()
	
	def create_piece(self, side, piece, move):
		if side == "W":
			if piece == "Queen":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.WQueen, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "WQueen", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Rook":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.WRook, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "WRook", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Bishop":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.WBishop, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "WBishop", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Knight":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.WKnight, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "WKnight", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
		if side == "B":
			if piece == "Queen":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.BQueen, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "BQueen", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Rook":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.BRook, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "BRook", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Bishop":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.BBishop, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "BBishop", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]
			if piece == "Knight":
				self.canvas.create_image(move[1] * 80 + 40, move[2] * 80 + 40, image = self.BKnight, anchor = CENTER, tag = ("ChessPiece", str(move[0]), "BKnight", "fake")) 
				self.pieces_positions[move[0]] = [move[1], move[2]]

#DEFINITION
	def join_server(self):
		self.t1.start()


	def server_update(self):
		run = True
		n = Network()
		n.connect()
		buffering = [["WPawn1", 0, 0]]
		server_message = (n.recv(4096)).decode()
		print(server_message)
		if server_message == "W":
			self.player = "W"
			self.reset()
		if server_message == "B":
			self.player = "B"
			self.reset()
		while run:
			try:
				if self.moved == True:
					n.sendall(self.history[-1])
					self.moved = False
				else:
					n.sendall(buffering)
				server = pickle.loads(n.recv(150))
				if not server:
					pass
				else:
					if server[0][0] == "RESET":
						if server[0][1] == self.player:
							pass
						elif server[0][1] != self.player:
							self.server_reset()
					elif server[0][0] == "UNDO":
						if server[0][1] == self.player:
							pass
						elif server[0][1] != self.player:
							self.server_undo()
					elif server != buffering:
						if server != self.history[-1]:
							self.update_board(server)
			except:
				pass
	def update_board(self, move):
		replaced = False
		for movement in move:
			if movement[0] not in self.pieces_positions:
				piece = movement[0][1:-1]
				side = movement[0][0]
				self.create_piece(side, piece, movement)
				replaced = True
			else:
				self.canvas.move(self.canvas.find_withtag(movement[0])[0], movement[1] * 80, movement[2] * 80)
				self.pieces_positions[movement[0]] = [int(self.canvas.coords(self.canvas.find_withtag(movement[0])[0])[0] / 80), int(self.canvas.coords(self.canvas.find_withtag(movement[0])[0])[1] / 80)]	
		if self.turn == "W":
			self.turn = "B"
		elif self.turn == "B":
			self.turn = "W"
		self.history.append(move)
		self.moves.append(move)
		self.check_attack_positions(thepositions = self.pieces_positions)
		self.reset_chessboard_colors()
		self.movement_marker(move)
		self.actually_check_for_check()
		self.check_for_checkmate()
		self.check_stalemate()

	def __init__(self, parent):
		Frame.__init__(self, parent, borderwidth = 10,relief = RIDGE, height = 640, width = 640)
		images.__init__(self)
		self.grid(column = 0, row = 0)
		self.turn = "W"
		self.canvas = Canvas(self, height = 640, width = 640, borderwidth = 0, highlightthickness = 0)
		self.canvas.pack()
		self.base_pieces_positions = {"WPawn1": [0, 6], "WPawn2" : [1, 6],  "WPawn3" : [2, 6], "WPawn4" : [3, 6], "WPawn5" : [4, 6], "WPawn6" : [5, 6], "WPawn7" : [6, 6], "WPawn8" : [7, 6], "WRook1" : [0, 7], "WRook2" : [7, 7], "WKnight1" : [1, 7], "WKnight2" : [6, 7], "WBishop1" : [2, 7], "WBishop2" : [5, 7], "WQueen1" : [3, 7], "WKing1" : [4, 7], "BPawn1": [0, 1], "BPawn2" : [1, 1],  "BPawn3" : [2, 1], "BPawn4" : [3, 1], "BPawn5" : [4, 1], "BPawn6" : [5, 1], "BPawn7" : [6, 1], "BPawn8" : [7, 1], "BRook1" : [0, 0], "BRook2" : [7, 0], "BKnight1" : [1, 0], "BKnight2" : [6, 0], "BBishop1" : [2, 0], "BBishop2" : [5, 0], "BQueen1" : [3, 0], "BKing1" : [4, 0]}
		self.pieces_positions = self.base_pieces_positions.copy()
		self.moves = [[["WPawn1", 0, 0]]]
		self.history = [[["WPawn1", 0, 0]]]
		self.wking_check = False
		self.bking_check = False
		self.can_Click = True
		self.player = "S"
		self.can_Click2 = True
		self.moved = False
		self.YUM = True
		self.stalemate = 0
		for x in range(8):
			for y in range(8):
				if (x + y) % 2 == 1:
					self.canvas.lower(self.canvas.create_rectangle(80 * x, 80 * y, 80 * x + 80, 80 * y + 80, fill = "#b58863", tag = ("immovable", "" + str(x) + ", " + str(y))))
				else:
					self.canvas.lower(self.canvas.create_rectangle(80 * x, 80 * y, 80 * x + 80, 80 * y + 80, fill = "#f0d9b5", tag = ("immovable", "" + str(x) + ", " + str(y))))
		self.place()
		Widget.bind(self.canvas, "<1>", self.mouse_down)
		Widget.bind(self.canvas, "<B1-Motion>", self.mouse_Move)
		Widget.bind(self.canvas, "<ButtonRelease-1>", self.mouse_Up)
		self.t1 = threading.Thread(target=self.server_update)

class Chess_Buttons(Frame):
	def __init__(self, parent):
		Frame.__init__(self, borderwidth = 10, bg = "black", pady = 10)
		self.grid(column = 0, row = 1, sticky = W+E)
		self.undo = Button(self, text = "undo", command = Piece.undo, activebackground = "yellow")
		self.reset = Button(self, text = "reset", command = Piece.reset, activebackground = "yellow" )
		self.connect = Button(self, text = "Connect to Multiplayer", command = Piece.join_server, activebackground = "yellow")
		self.undo.grid(column = 0, row = 0, sticky = N+S)
		self.reset.grid(column = 1, row = 0, sticky = N+S)
		self.connect.grid(column = 2, row = 0, sticky = N+S)

#GUI		
root = Tk()
root.iconbitmap(r"C:\Users\RetailAdmin\Documents\Python\Queen\gay.ico")
root.title("Chess")
root.configure(background = "#5577aa")
Piece = Pieces(root)
Some_Buttons = Chess_Buttons(root)
root.mainloop()
