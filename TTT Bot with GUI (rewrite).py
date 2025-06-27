import random
from tkinter import Tk, N, E, S, W, StringVar, IntVar
from tkinter.ttk import Button, Label, Frame, Radiobutton
from functools import partial
from time import sleep

#----------------------------- Global vars -----------------------------#
turn = True     # Keeps track of if it's P1's turn (if not, it can be assumed that it's P2's turn)
game_on = False # Keeps track of if a game is currently running

#----------------------------- Functions -----------------------------#
def start_game():
    """Begins a game of TTT
    """
    # Resets the labels and buttons
    for r in buttons:
        for button in r:
            button[0]['state'] = 'normal'
            button[1].set('')
    # Switches to the game screen
    show_screen(1)
    
    # If both players are AIs, disable the buttons
    if (p1_type.get() > 0) and (p2_type.get() > 0):
        for row in buttons:
            for b in row:
                b[0]['state'] = 'disabled'
    
    # Resets the game variables
    global game_on
    game_on = True
    global turn
    turn = True
    #print("Game on!")

    # Plays the first move if player 1 is an AI
    if p1_type.get() == 1:
        play_move(random_ai_move())
    elif p1_type.get() == 2:
        play_move(better_ai_move())

def exit_game():
    """Exits the game window
    """
    root.destroy()

def get_winner():
    for player in ['X', 'O']:
        # Check for 3-in-a-row in the rows
        for row in buttons:
            if row[0][1].get() == player and row[1][1].get() == player and row[2][1].get() == player:
                return player
        # Check for 3-in-a-row in the columns
        for i in range(3):
            if (buttons[0][i][1].get() == player and buttons[1][i][1].get() == player and buttons[2][i][1].get() == player):
                return player
        # Check for 3-in-a-row in the diagonals
        if (buttons[0][0][1].get() == player and buttons[1][1][1].get() == player and buttons[2][2][1].get() == player):
            return player
        if (buttons[0][2][1].get() == player and buttons[1][1][1].get() == player and buttons[2][0][1].get() == player):
            return player

def is_board_full():
    """Checks if the bingo board is completely full

    Returns:
        full (bool): Whether or not the board is full
    """
    full = True
    for row in buttons:
        for b in row:
            if b[1].get() == '':
                full = False
    
    return full

def play_move(coords: tuple):
    """Handles the logic of "playing" a move

    Args:
        coords (tuple): A tuple containing the X and Y coordinates (in that order) of the space to be played
    """
    global turn
    global game_on
    
    mark = 'X' if turn else 'O'

    if game_on:
        #print(f'{mark} has made a move at {coords[0]}, {abs(coords[1] - 2)}')  # Human-readable (bottom left is (0, 0)
        button_in_play = buttons[coords[1]][coords[0]][0]
        text_in_play = buttons[coords[1]][coords[0]][1]

        text_in_play.set(mark)
        button_in_play['state'] = 'disabled'

        root.update()

        if get_winner() != None:
            game_on =  False
            winner.set(get_winner())
            if p1_type.get() in [1, 2] or p2_type.get() in [1, 2]:
                sleep(1.5)
            show_screen(2)
            return
        elif is_board_full():
            game_on = False
            if p1_type.get() == 2 and p2_type.get() == 2:
                winner.set('A strange game. The only winning move is not to play.') # Wargames reference
            else:
                winner.set('Tie!')
            if p1_type.get() in [1, 2] or p2_type.get() in [1, 2]:
                sleep(1.5)
            show_screen(2)
            return

        if turn:                        # Player 1's turn (currently)
            turn = False
            if p2_type.get() == 1:      # If p2 is random AI
                play_move(random_ai_move())
            elif p2_type.get() == 2:    # If p2 is better AI
                play_move(better_ai_move())
        else:                           # Player 2's turn (currently)
            turn = True
            if p1_type.get() == 1:      # If p1 is random AI
                play_move(random_ai_move())
            elif p1_type.get() == 2:    # If p1 is better AI
                play_move(better_ai_move())
    else:
        show_screen(2)                  # If something goes wrong, show the end screen

def random_ai_move():
    """Figures out what move the random AI "player" wants to make

    Returns:
        tuple: The coordinates of the space to be played
    """
    
    # Gets an array of all valid moves
    valid_moves = []
    for y in range(3):
        for x in range(3):
            if buttons[y][x][1].get() == '':
                valid_moves.append((x, y))
    
    # Waits for a bit so the move isn't instant
    sleep(1.5)
    
    return random.choice(valid_moves)

def better_ai_move():
    """Figures out what move the better AI "player" wants to make

    Returns:
        tuple: The coordinates of the space to be played
    """
    mark = 'X' if turn else 'O'
    other_mark = 'O' if turn else 'X'
        
    # Waits for a bit so the move isn't instant
    sleep(1.5)
    
    # Gets an array of all valid moves (to be used at the end)
    valid_moves = []
    for get_y in range(3):
        for get_x in range(3):
            if buttons[get_y][get_x][1].get() == '':
                valid_moves.append((get_x, get_y))

    # Figure out if you're about to win, and play the winning move
    if (buttons[0][1][1].get() == mark and buttons[0][2][1].get() == mark) or (buttons[1][0][1].get() == mark and buttons[2][0][1].get() == mark) or (buttons[1][1][1].get() == mark and buttons[2][2][1].get() == mark):
        if buttons[0][0][1].get() == '':
            return (0, 0)
    elif (buttons[0][0][1].get() == mark and buttons[0][2][1].get() == mark) or (buttons[1][1][1].get() == mark and buttons[2][1][1].get() == mark):
        if buttons[0][1][1].get() == '':
            return (1, 0)
    elif (buttons[0][0][1].get() == mark and buttons[0][1][1].get() == mark) or (buttons[1][2][1].get() == mark and buttons[2][2][1].get() == mark) or (buttons[2][0][1].get() == mark and buttons[1][1][1].get() == mark):
        if buttons[0][2][1].get() == '':
            return (2, 0)
    elif (buttons[0][0][1].get() == mark and buttons[2][0][1].get() == mark) or (buttons[1][1][1].get() == mark and buttons[1][2][1].get() == mark):
        if buttons[1][0][1].get() == '':
            return (0, 1)
    elif (buttons[0][0][1].get() == mark and buttons[2][2][1].get() == mark) or (buttons[0][2][1].get() == mark and buttons[2][0][1].get() == mark) or (buttons[1][0][1].get() == mark and buttons[1][2][1].get() == mark) or (buttons[0][1][1].get() == mark and buttons[2][1][1].get() == mark):
        if buttons[1][1][1].get() == '':
            return (1, 1)
    elif (buttons[1][0][1].get() == mark and buttons[1][1][1].get() == mark) or (buttons[0][2][1].get() == mark and buttons[2][2][1].get() == mark):
        if buttons[1][2][1].get() == '':
            return (2, 1)
    elif (buttons[0][0][1].get() == mark and buttons[1][0][1].get() == mark) or (buttons[2][1][1].get() == mark and buttons[2][2][1].get() == mark) or (buttons[1][1][1].get() == mark and buttons[0][2][1].get() == mark):
        if buttons[2][0][1].get() == '':
            return (0, 2)
    elif (buttons[2][0][1].get() == mark and buttons[2][2][1].get() == mark) or (buttons[0][1][1].get() == mark and buttons[1][1][1].get() == mark):
        if buttons[2][1][1].get() == '':
            return (1, 2)
    elif (buttons[2][0][1].get() == mark and buttons[2][1][1].get() == mark) or (buttons[0][2][1].get() == mark and buttons[1][2][1].get() == mark) or (buttons[0][0][1].get() == mark and buttons[1][1][1].get() == mark):
        if buttons[2][2][1].get() == '':
            return (2, 2)

    # If the other player is about to get three in a row, block them
    if (buttons[0][1][1].get() == other_mark and buttons[0][2][1].get() == other_mark) or (buttons[1][0][1].get() == other_mark and buttons[2][0][1].get() == other_mark) or (buttons[1][1][1].get() == other_mark and buttons[2][2][1].get() == other_mark):
        if buttons[0][0][1].get() == '':
            return (0, 0)
    elif (buttons[0][0][1].get() == other_mark and buttons[0][2][1].get() == other_mark) or (buttons[1][1][1].get() == other_mark and buttons[2][1][1].get() == other_mark):
        if buttons[0][1][1].get() == '':
            return (1, 0)
    elif (buttons[0][0][1].get() == other_mark and buttons[0][1][1].get() == other_mark) or (buttons[1][2][1].get() == other_mark and buttons[2][2][1].get() == other_mark) or (buttons[2][0][1].get() == other_mark and buttons[1][1][1].get() == other_mark):
        if buttons[0][2][1].get() == '':
            return (2, 0)
    elif (buttons[0][0][1].get() == other_mark and buttons[2][0][1].get() == other_mark) or (buttons[1][1][1].get() == other_mark and buttons[1][2][1].get() == other_mark):
        if buttons[1][0][1].get() == '':
            return (0, 1)
    elif (buttons[0][0][1].get() == other_mark and buttons[2][2][1].get() == other_mark) or (buttons[0][2][1].get() == other_mark and buttons[2][0][1].get() == other_mark) or (buttons[1][0][1].get() == other_mark and buttons[1][2][1].get() == other_mark) or (buttons[0][1][1].get() == other_mark and buttons[2][1][1].get() == other_mark):
        if buttons[1][1][1].get() == '':
            return (1, 1)
    elif (buttons[1][0][1].get() == other_mark and buttons[1][1][1].get() == other_mark) or (buttons[0][2][1].get() == other_mark and buttons[2][2][1].get() == other_mark):
        if buttons[1][2][1].get() == '':
            return (2, 1)
    elif (buttons[0][0][1].get() == other_mark and buttons[1][0][1].get() == other_mark) or (buttons[2][1][1].get() == other_mark and buttons[2][2][1].get() == other_mark) or (buttons[1][1][1].get() == other_mark and buttons[0][2][1].get() == other_mark):
        if buttons[2][0][1].get() == '':
            return (0, 2)
    elif (buttons[2][0][1].get() == other_mark and buttons[2][2][1].get() == other_mark) or (buttons[0][1][1].get() == other_mark and buttons[1][1][1].get() == other_mark):
        if buttons[2][1][1].get() == '':
            return (1, 2)
    elif (buttons[2][0][1].get() == other_mark and buttons[2][1][1].get() == other_mark) or (buttons[0][2][1].get() == other_mark and buttons[1][2][1].get() == other_mark) or (buttons[0][0][1].get() == other_mark and buttons[1][1][1].get() == other_mark):
        if buttons[2][2][1].get() == '':
            return (2, 2)
    
    # The order in this list is significant!  Adding 2 to the index and modding by 4 gets the opposite corner!
    corners = [
        (0, 0),     # Top-left
        (0, 2),     # Top-right
        (2, 2),     # Bottom-right
        (2, 0)      # Bottom-left
    ]
    # If the other player went in the middle, play one of the corners randomly
    if buttons[1][1][1].get() == other_mark:
        new_move = random.choice(corners)
        if buttons[new_move[0]][new_move[1]][1].get() == '':
            return random.choice(corners)
    
    # If the other player goes in a corner and the board is otherwise empty, play the opposite corner
    i = 0
    for temp_y, temp_x in corners:
        other_board = [['', '', ''], ['', '', ''], ['', '', '']]
        temp_board = []
        for row in buttons:
            temp_row = []
            for b in row:
                temp_row.append(b[1].get())
            temp_board.append(temp_row)
        
        other_board[temp_y][temp_x] = other_mark

        if temp_board == other_board:
            if temp_board[corners[(i + 2) % 4][0]][corners[(i + 2) % 4][1]] == '':
                return corners[(i + 2) % 4]
    
    # As a fallback, make a random move
    return random.choice(valid_moves)

#     --- SCREEN FUNCTIONS ---     #
def show_screen(screen_num: int):
    """Replaces the widgets of one "screen" with those of another

    Args:
        screen_num (int): The ID of the screen (0-2) that needs to be shown
    """
    # Clears currently-active widgets (except the title, which is always visible)
    for name in mainframe.children:
        if name != 'title':
            mainframe.children[name].grid_forget()

    if screen_num == 0:     # Start screen
        start_button.grid(row=4, column=1)
        p1_menu1.grid(row=1, column=0)
        p1_menu2.grid(row=2, column=0)
        p1_menu3.grid(row=3, column=0)
        p2_menu1.grid(row=1, column=2)
        p2_menu2.grid(row=2, column=2)
        p2_menu3.grid(row=3, column=2)
    elif screen_num == 1:   # Game screen
        a1_button.grid(row=1, column=0)
        a2_button.grid(row=1, column=1)
        a3_button.grid(row=1, column=2)
        b1_button.grid(row=2, column=0)
        b2_button.grid(row=2, column=1)
        b3_button.grid(row=2, column=2)
        c1_button.grid(row=3, column=0)
        c2_button.grid(row=3, column=1)
        c3_button.grid(row=3, column=2)

        # Sets all of the buttons back to normal
        for row in buttons:
            for b in row:
                b[0]['state'] = 'normal'
    elif screen_num == 2:   # End screen
        winner_label.grid(row=1, column=0, columnspan=3)
        play_again_button.grid(row=2, column=0)
        main_menu_button.grid(row=2, column=2)
        exit_button.grid(row=3, column=1)
    
    # Makes sure the window shows the updates
    root.update()

#Sets up the tkinter window
root = Tk()
root.title('Tic-Tac-Toe')

# Sets up the grid for use in positioning
mainframe = Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

title = Label(mainframe, text='Tic-Tac-Toe', name='title')
title.grid(row=0, column=0, columnspan=3)

#----------------------------- tkinter Variables -----------------------------#
p1_type = IntVar()
p2_type = IntVar()
winner = StringVar()
a1_label = StringVar()
a2_label = StringVar()
a3_label = StringVar()

b1_label = StringVar()
b2_label = StringVar()
b3_label = StringVar()

c1_label = StringVar()
c2_label = StringVar()
c3_label = StringVar()

#---------- START SCREEN WIDGETS ----------#
start_button = Button(mainframe, text='Start!', command=start_game)

# Radio buttons for player 1's type
p1_menu1 = Radiobutton(mainframe, text="Human", variable=p1_type, value=0)
p1_menu2 = Radiobutton(mainframe, text="AI", variable=p1_type, value=1)
p1_menu3 = Radiobutton(mainframe, text="AI+", variable=p1_type, value=2)

# Radio buttons for player 2's type
p2_menu1 = Radiobutton(mainframe, text="Human", variable=p2_type, value=0)
p2_menu2 = Radiobutton(mainframe, text="AI", variable=p2_type, value=1)
p2_menu3 = Radiobutton(mainframe, text="AI+", variable=p2_type, value=2)

#---------- GAME SCREEN WIDGETS ----------#
# Top row
a1_button = Button(mainframe, textvariable=a1_label, command=partial(play_move, (0, 0)))
a2_button = Button(mainframe, textvariable=a2_label, command=partial(play_move, (1, 0)))
a3_button = Button(mainframe, textvariable=a3_label, command=partial(play_move, (2, 0)))

# Middle row
b1_button = Button(mainframe, textvariable=b1_label, command=partial(play_move, (0, 1)))
b2_button = Button(mainframe, textvariable=b2_label, command=partial(play_move, (1, 1)))
b3_button = Button(mainframe, textvariable=b3_label, command=partial(play_move, (2, 1)))

# Bottom row
c1_button = Button(mainframe, textvariable=c1_label, command=partial(play_move, (0, 2)))
c2_button = Button(mainframe, textvariable=c2_label, command=partial(play_move, (1, 2)))
c3_button = Button(mainframe, textvariable=c3_label, command=partial(play_move, (2, 2)))

# Creates an array in which a given entry is a tuple containing a button object and
#    its corresponding label (in that order)
buttons = [
    [(a1_button, a1_label), (a2_button, a2_label), (a3_button, a3_label)],
    [(b1_button, b1_label), (b2_button, b2_label), (b3_button, b3_label)],
    [(c1_button, c1_label), (c2_button, c2_label), (c3_button, c3_label)]
]

#---------- END SCREEN WIDGETS ----------#
winner_label = Label(mainframe, textvariable=winner)
play_again_button = Button(mainframe, text='Play again' ,command=start_game)
main_menu_button = Button(mainframe, text='Main menu', command=partial(show_screen, 0))
exit_button = Button(mainframe, text='Exit', command=exit_game)

# Begins the window loop
show_screen(0)
root.mainloop()