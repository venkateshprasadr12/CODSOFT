import tkinter as tk
from tkinter import messagebox
import math

# Set up the main application window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Initialize the game board and variables
board = [' ' for _ in range(9)]
human = 'O'
ai = 'X'

# Function to reset the game board
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    for button in buttons:
        button.config(text=" ", state=tk.NORMAL)

# Function to print the board to the console (for debugging)
def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print(row)
    print()

# Function to check if the board is full
def is_full(board):
    return ' ' not in board

# Function to check for a win
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

# Minimax function with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == ai:
        return 10 - depth
    elif winner == human:
        return depth - 10
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = ai
                eval = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = human
                eval = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

# Function for the AI's move
def ai_move():
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = ai
        buttons[best_move].config(text=ai)
        if check_winner(board) == ai:
            messagebox.showinfo("Game Over", "AI wins!")
            disable_buttons()
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()

# Function to handle human move
def handle_click(i):
    if board[i] == ' ':
        board[i] = human
        buttons[i].config(text=human)
        if check_winner(board) == human:
            messagebox.showinfo("Game Over", "You win!")
            disable_buttons()
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            ai_move()

# Function to disable all buttons after game ends
def disable_buttons():
    for button in buttons:
        button.config(state=tk.DISABLED)

# Create a 3x3 grid of buttons for the board
buttons = []
for i in range(9):
    button = tk.Button(window, text=" ", font=("Arial", 24), width=5, height=2,
                       command=lambda i=i: handle_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Reset button
reset_button = tk.Button(window, text="Reset", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

# Start the GUI event loop
window.mainloop()
