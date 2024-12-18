import tkinter as tk
from tkinter import messagebox
import time

class CubicUI:
    def __init__(self, root, game, ai):
        self.game = game
        self.ai = ai
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.menu_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)

        self.create_menu()  
        self.create_game_ui()

        self.show_menu()

        self.start_time = None
        self.timer_running = False

    def create_menu(self):
        self.menu_frame.pack(fill="both", expand=True)

        title = tk.Label(self.menu_frame, text="Tic-Tac-Toe", font=("Arial", 24))
        title.pack(pady=20)

        start_button = tk.Button(self.menu_frame, text="Start Game", font=("Arial", 16),
                                 command=self.start_game, width=15, height=2)
        start_button.pack(pady=10)

        close_button = tk.Button(self.menu_frame, text="Close", font=("Arial", 16),
                                 command=self.on_close, width=15, height=2)
        close_button.pack(pady=10)

    def create_game_ui(self):
        self.game_frame.pack_forget()

        top_frame = tk.Frame(self.game_frame)
        top_frame.pack(pady=10)

        self.status_label = tk.Label(top_frame, text="Player X's Turn", font=("Arial", 16))
        self.status_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(top_frame, text="Time: 00:00", font=("Arial", 16))
        self.timer_label.pack(side="right", padx=20)

        grid_frame = tk.Frame(self.game_frame)
        grid_frame.pack()

        self.frames = []
        self.buttons = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.create_grid(grid_frame)

        bottom_frame = tk.Frame(self.game_frame)
        bottom_frame.pack(pady=10)

        reset_button = tk.Button(bottom_frame, text="Reset", font=("Arial", 14),
                                 command=self.reset_game, width=10)
        reset_button.pack(side="left", padx=10)

        back_button = tk.Button(bottom_frame, text="Back to Menu", font=("Arial", 14),
                                command=self.back_to_menu, width=15)
        back_button.pack(side="right", padx=10)

    def create_grid(self, parent):
        for z in range(4):
            frame = tk.Frame(parent, borderwidth=2, relief="solid")
            frame.grid(row=0, column=z, padx=5, pady=5)
            self.frames.append(frame)
            tk.Label(frame, text=f"Layer {z+1}", font=("Arial", 12)).grid(row=0, column=0, columnspan=4)
            for x in range(4):
                for y in range(4):
                    button = tk.Button(
                        frame, text="", width=4, height=2, font=("Arial", 16),
                        command=lambda x=x, y=y, z=z: self.make_move(x, y, z)
                    )
                    button.grid(row=x+1, column=y, padx=2, pady=2)
                    self.buttons[z][x][y] = button

    def show_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.reset_game()
        self.start_timer()

    def reset_game(self):
        self.game.reset_game()
        self.update_grid()
        self.status_label.config(text=f"Player {self.game.current_player}'s Turn")
        self.start_time = time.time()
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

        for z in range(4):
            for x in range(4):
                for y in range(4):
                    self.buttons[z][x][y].config(state="normal", text="", fg="black", bg="white")  

    def back_to_menu(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to return to the main menu?"):
            self.timer_running = False
            self.show_menu()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def make_move(self, x, y, z):
        if self.game.board[x][y][z] is None and self.timer_running:
            self.game.board[x][y][z] = self.game.current_player
            self.update_grid()
            if self.game.is_winner(self.game.current_player):
                self.status_label.config(text=f"Player {self.game.current_player} Wins")
                self.highlight_winner(self.game.winning_positions)
                self.disable_buttons()
                self.timer_running = False
                return
            elif self.game.is_full():
                self.status_label.config(text="It's a Draw")
                self.disable_buttons()
                self.timer_running = False
                return
            self.game.current_player = "O"
            self.status_label.config(text="Player O's Turn (AI)")
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if not self.timer_running:
            return
        start_time = time.time()
        move = self.ai.find_best_move(self.game)
        end_time = time.time()

        print(f"Time taken: {end_time - start_time:.2f} seconds")
        if move:
            x, y, z = move
            self.game.board[x][y][z] = self.game.current_player
            self.update_grid()
            if self.game.is_winner(self.game.current_player):
                self.status_label.config(text=f"Player {self.game.current_player} Wins")
                self.highlight_winner(self.game.winning_positions)
                self.disable_buttons()
                self.timer_running = False
                return
            elif self.game.is_full():
                self.status_label.config(text="It's a Draw")
                self.disable_buttons()
                self.timer_running = False
                return
        self.game.current_player = "X"
        self.status_label.config(text="Player X's Turn")

    def update_grid(self):
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    symbol = self.game.board[x][y][z]
                    if symbol == "X":
                        self.buttons[z][x][y].config(text=symbol, fg="red")
                    elif symbol == "O":
                        self.buttons[z][x][y].config(text=symbol, fg="blue")
                    else:
                        self.buttons[z][x][y].config(text="", fg="black")

    def highlight_winner(self, winning_positions):
        for (x, y, z) in winning_positions:
            self.buttons[z][x][y].config(bg="green")

    def disable_buttons(self):
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    self.buttons[z][x][y].config(state="disabled")

    def start_timer(self):
        self.start_time = time.time()
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
