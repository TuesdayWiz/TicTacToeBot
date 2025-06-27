import random
from tkinter import Tk, N, E, S, W, StringVar, IntVar
from tkinter.ttk import Button, Label, Frame, Radiobutton
from functools import partial
from time import sleep

#-----------------------------TODO------------------------------#
# Button coords are broken, design a function that takes coords #
#    and returns which button should be pressed                 #
#---------------------------------------------------------------#

#----------------------------- Global Vars -----------------------------#

turn = 1    # Keeps track of which player's turn it is
#p1_human = True
#p2_human = True

#----------------------------- Player Types -----------------------------#
class HumanPlayer:
    def __init__(self, mark):
        self.mark = mark
        self.human = True

class RandomAiPlayer:
    def __init__(self, mark):
        self.mark = mark
        self.human = False
    
    def take_turn(self):
        #print('Turn being taken!')
        # Select a random location on the board that is not filled.
        
        # Find the list of all empty locations
        empty_locs = []
        for y in range(3):
            for x in range(3):
                if labels[y][x].get() == '':
                    empty_locs.append((x, y))
                    
        # Pick 1 at random
        sleep(3)
        move = random.choice(empty_locs)
        play_move(move[0], move[1])

class BetterAiPlayer:
    def __init__(self, mark):
        self.mark = mark
        self.human = False
    
    def take_turn(self):
        # If the other player is about to get 3 in a row, block them
        #print('Turn being taken!')
        other_player = 'X' if self.mark == 'O' else 'O'
        for player in [self.mark, other_player]:
            for y in range(3):
                if labels[y][0].get() == player and labels[y][1].get() == player:
                    if labels[y][2].get() == '':
                        sleep(3)
                        play_move(2, y)
                if labels[y][0].get() == player and labels[y][2].get() == player:
                    if labels[y][1].get() == '':
                        sleep(3)
                        play_move(1, y)
                if labels[y][1].get() == player and labels[y][2].get() == player:
                    if labels[y][0].get() == '':
                        sleep(3)
                        play_move(0, y)
            for x in range(3):
                if labels[0][x].get() == player and labels[1][x].get() == player:
                    if labels[2][x].get() == '':
                        sleep(3)
                        play_move(x, 2)
                if labels[0][x].get() == player and labels[2][x].get() == player:
                    if labels[1][x].get() == '':
                        sleep(3)
                        play_move(x, 1)
                if labels[1][x].get() == player and labels[2][x].get() == player:
                    if labels[0][x].get() == '':
                        sleep(3)
                        play_move(x, 0)
            if labels[0][0].get() == player and labels[1][1].get() == player:
                if labels[2][2].get() == '':
                    sleep(3)
                    play_move(2, 2)
            if labels[0][0].get() == player and labels[2][2].get() == player:
                if labels[1][1].get() == '':
                    sleep(3)
                    play_move(1, 1)
            if labels[1][1].get() == player and labels[2][2].get() == player:
                if labels[0][0].get() == '':
                    sleep(3)
                    play_move(0, 0)
            
            if labels[2][0].get() == player and labels[1][1].get() == player:
                if labels[0][2].get() == '':
                    sleep(3)
                    play_move(2, 0)
            if labels[2][0].get() == player and labels[0][2].get() == player:
                if labels[1][1].get() == '':
                    sleep(3)
                    play_move(1, 1)
            if labels[1][1].get() == player and labels[0][2].get() == player:
                if labels[2][0].get() == '':
                    sleep(3)
                    play_move(0, 2)
                
        # The ordering in this list is significant!
        # Adding 2 to the index (mod 4) gives us the opposite corner.
        corners = [(0, 0), (2, 0), (2, 2), (0, 2)]
        if b2.get() == other_player:
            # Randomly pick a corner if the other player moved first and took the middle
            sleep(3)
            move = random.choice(corners)
            play_move(move[0], move[1])
        i = 0
        for corner_x, corner_y in corners:
            other_board = [['', '', ''], ['', '', ''], ['', '', '']]
            other_board[corner_y][corner_x] = other_player
            if labels == other_board:
                sleep(3)
                move = corners[(i + 2) % 4]
                play_move(move[0], move[1])
            i += 1
        
        # As a fall back, do things randomly
        
        # Find the list of all empty locations
        empty_locs = []
        for y in range(3):
            for x in range(3):
                if labels[y][x].get() == '':
                    empty_locs.append((x, y))
                    
        # Pick 1 at random
        sleep(3)
        move = random.choice(empty_locs)
        play_move(move[0], move[1])

#----------------------------- Functions -----------------------------#
def start_game():
    """Sets up the variables to play a game of TTT
    Also used to "play again" after a game
    """
    global turn
    turn = 1
    
    for row in board:
        for button in row:
            button['state'] = 'normal'
    
    a1.set('')
    a2.set('')
    a3.set('')
    
    b1.set('')
    b2.set('')
    b3.set('')

    c1.set('')
    c2.set('')
    c3.set('')

    global player_1
    global player_2
    if p1_type.get() == 0:
        player_1 = HumanPlayer("X")
    elif p1_type.get() == 1:
        player_1 = RandomAiPlayer("X")
    elif p2_type.get() == 2:
        player_1 = BetterAiPlayer("X")

    if p2_type.get() == 0:
        player_2 = HumanPlayer("O")
    elif p2_type.get() == 1:
        player_2 = RandomAiPlayer("O")
    elif p2_type.get() == 2:
        player_2 = BetterAiPlayer("O")
    
    if p1_type.get() in [1, 2] and p2_type.get() in [1, 2]:
        for row in board:
            for button in row:
                button['state'] = 'disabled'
    
    #print(f'New game starting with types {p1_type.get()} and {p2_type.get()}')
    game_screen()
    game_logic()

def exit_game():
    """Closes the game window
    """
    root.destroy()

def play_move(x, y):
    """Handles a move being made (either by a human or by the computer)

    Args:
        x (int): The x-coordinate of the space that was played (0-2 inclusive)
        y (int): The y-coordinate of the space that was played (0-2 inclusive)

    """
    global turn
    button_in_play = get_button(x, y)
    label_in_play = labels[y][x]

    # Figures out what to put in the button, changes whose turn it is (once this play ends)
    if turn == 1:
        mark = "X"
        turn = 2
    else:
        mark = "O"
        turn = 1

    label_in_play.set(mark)
    button_in_play['state'] = "disabled"
    
    root.update()

def clear_screen():
    """Removes all currently-active widgets (except the title widget) to prepare for a new "screen" being shown
    """
    for name in mainframe.children:
        if name != 'title':
            mainframe.children[name].grid_forget()

def start_screen():
    """Places the widgets for the start screen
    """
    clear_screen()
    
    start_button.grid(row=4, column=1)
    
    p1_menu1.grid(row=1, column=0)
    p1_menu2.grid(row=2, column=0)
    p1_menu3.grid(row=3, column=0)
    
    p2_menu1.grid(row=1, column=2)
    p2_menu2.grid(row=2, column=2)
    p2_menu3.grid(row=3, column=2)

def game_screen():
    """Places all the widgets for the game screen
    """
    clear_screen()

    a1_button.grid(row=1, column=0)
    a2_button.grid(row=1, column=1)
    a3_button.grid(row=1, column=2)

    b1_button.grid(row=2, column=0)
    b2_button.grid(row=2, column=1)
    b3_button.grid(row=2, column=2)

    c1_button.grid(row=3, column=0)
    c2_button.grid(row=3, column=1)
    c3_button.grid(row=3, column=2)

def game_logic():
    # Handles the game logic
    game_over = False
    while game_over == False:
        if turn == 1:   # Player 1 logic
            if player_1.human == False:
                player_1.take_turn()
        elif turn == 2: # Player 2 logic
            if player_2.human == False:
                player_2.take_turn()
        
        root.update()

        if get_winner() != None:
            winner.set(f'{get_winner()} is the winner!')
            game_over = True
        elif is_board_full():
            if p1_type == 2 and p2_type == 2:
                winner.set('A strange game. The only winning move is not to play.')
            else:
                winner.set("Tie!")
            game_over = True
    end_screen()

def end_screen():
    """Places all the widgets for the end screen
    """
    clear_screen()
    
    winner_label.grid(row=1, column=0, columnspan=3)
    play_again_button.grid(row=2, column=0)
    main_menu_button.grid(row=2, column=2)
    exit_button.grid(row=3, column=1)

def get_winner():
    """Determine if there is winner yet. Returns 'X' or 'O' if that player has won
    or None if no player has won yet.
    """
    for player in ['X', 'O']:
        # Check for 3-in-a-row in the rows
        for row in labels:
            if row[0].get() == player and row[1].get() == player and row[2].get() == player:
                return player
        # Check for 3-in-a-row in the columns
        for i in range(3):
            if (labels[0][i].get() == player and labels[1][i].get() == player and labels[2][i].get() == player):
                return player
        # Check for 3-in-a-row in the diagonals
        if (labels[0][0].get() == player and labels[1][1].get() == player and labels[2][2].get() == player):
            return player
        if (labels[0][2].get() == player and labels[1][1].get() == player and labels[2][0].get() == player):
            return player
    
    # No one has won yet
    return None
    
def is_board_full():
    """Returns True if the game is tied and no moves remain.
    """
    for row in labels:
        for cell in row:
            if cell.get() == '':
                # If we find an empty cell, the board cannot be full yet
                return False
    return True

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
a1 = StringVar()
a2 = StringVar()
a3 = StringVar()

b1 = StringVar()
b2 = StringVar()
b3 = StringVar()

c1 = StringVar()
c2 = StringVar()
c3 = StringVar()

labels = [
    [a1, a2, a3],
    [b1, b2, b3],
    [c1, c2, c3],
    ]

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
# Row 1
a1_button = Button(mainframe, textvariable=a1, command=partial(play_move, 0, 0))
a2_button = Button(mainframe, textvariable=a2, command=partial(play_move, 1, 0))
a3_button = Button(mainframe, textvariable=a3, command=partial(play_move, 2, 0))

# Row 2
b1_button = Button(mainframe, textvariable=b1, command=partial(play_move, 0, 1))
b2_button = Button(mainframe, textvariable=b2, command=partial(play_move, 1, 1))
b3_button = Button(mainframe, textvariable=b3, command=partial(play_move, 2, 1))

# Row 3
c1_button = Button(mainframe, textvariable=c1, command=partial(play_move, 0, 2))
c2_button = Button(mainframe, textvariable=c2, command=partial(play_move, 1, 2))
c3_button = Button(mainframe, textvariable=c3, command=partial(play_move, 2, 2))

board = [
    [a1_button, a2_button, a3_button],
    [b1_button, b2_button, b3_button],
    [c1_button, c2_button, c3_button],
    ]

def get_button(x, y):
    """_summary_

    Args:
        x (int): X-coordinate of the button (0-2, inclusive)
        y (int): Y-coordinate of the button (0-2, inclusive)
    
    Returns:
        button (Button): The button that corresponds to the given coordinates
    """
    button = board[y][x]
    return button

#---------- END SCREEN WIDGETS ----------#
winner_label = Label(mainframe, textvariable=winner)
play_again_button = Button(mainframe, text='Play again' ,command=start_game)
main_menu_button = Button(mainframe, text='Main menu', command=start_screen)
exit_button = Button(mainframe, text='Exit', command=exit_game)

# Begins the window loop
start_screen()
root.mainloop()