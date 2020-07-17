from tkinter import *
from PIL import ImageTk, Image

class images():
    def __init__(self):
        self.BPawn = ImageTk.PhotoImage(Image.open(".\\Images\\BPawn.png").resize((80, 80)))
        self.BRook = ImageTk.PhotoImage(Image.open(".\\Images\\BRook.png").resize((80, 80)))
        self.BBishop = ImageTk.PhotoImage(Image.open(".\\Images\\BBishop.png").resize((80, 80)))
        self.BQueen = ImageTk.PhotoImage(Image.open(".\\Images\\BQueen.png").resize((80, 80)))
        self.BKing = ImageTk.PhotoImage(Image.open(".\\Images\\BKing.png").resize((80, 80)))   
        self.BKnight = ImageTk.PhotoImage(Image.open(".\\Images\\BKnight.png").resize((80, 80)))
        self.WPawn = ImageTk.PhotoImage(Image.open(".\\Images\\WPawn.png").resize((80, 80)))
        self.WRook = ImageTk.PhotoImage(Image.open(".\\Images\\WRook.png").resize((80, 80)))
        self.WBishop = ImageTk.PhotoImage(Image.open(".\\Images\\WBishop.png").resize((80, 80)))
        self.WQueen = ImageTk.PhotoImage(Image.open(".\\Images\\WQueen.png").resize((80, 80)))
        self.WKing = ImageTk.PhotoImage(Image.open(".\\Images\\WKing.png").resize((80, 80)))   
        self.WKnight = ImageTk.PhotoImage(Image.open(".\\Images\\WKnight.png").resize((80, 80)))
        self.chessboard = ImageTk.PhotoImage(Image.open(".\\Images\\Chessboard.png"))
        self.checkmate = ImageTk.PhotoImage(Image.open(".\\Images\\Checkmate.png").resize((400, 200)))
        self.stalemate_image = ImageTk.PhotoImage(Image.open(".\\Images\\Stalemate.png").resize((484, 121)))