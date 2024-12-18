from tkinter import Tk
from game_logic import CubicGame
from ai_player import AIPlayer
from ui import CubicUI

if __name__ == "__main__":
    root = Tk()
    root.title(" Tic-Tac-Toe")
    game = CubicGame()
    ai = AIPlayer("O")
    app = CubicUI(root, game, ai)
    root.mainloop() 