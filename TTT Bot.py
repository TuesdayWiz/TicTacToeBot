import random

def print_board(board):
    for y in range(3):
        for x in range(3):
            cell = board[y][x]
            if cell == '':
                print(' ', end='')
            else:
                print(cell, end='')
            if x != 2:
                print('|', end='')
        print()
        if y != 2:
            print('-+-+-')


def get_winner(board):
    """
    Determine if there is winner yet. Returns 'X' or 'O' if that player has won
    or None if no player has won yet.
    """
    for player in ['X', 'O']:
        # Check for 3-in-a-row in the rows
        for row in board:
            if row[0] == player and row[1] == player and row[2] == player:
                return player
        # Check for 3-in-a-row in the columns
        for i in range(3):
            if (board[0][i] == player and board[1][i] == player
                    and board[2][i] == player):
                return player
        # Check for 3-in-a-row in the diagonals
        if (board[0][0] == player and board[1][1] == player
                and board[2][2] == player):
            return player
        if (board[0][2] == player and board[1][1] == player
                and board[2][0] == player):
            return player
    
    # No one has won yet
    return None
    
def is_board_full(board):
    "Returns True if the game is tied and no moves remain."
    for row in board:
        for cell in row:
            if cell == '':
                # If we find an empty cell, the board cannot be full yet
                return False
    return True


def get_player_move(player, board):
    x = int(input(f"Player {player}, where would you place your mark (x): "))
    y = int(input(f"Player {player}, where would you place your mark (y): "))
    
    while board[y][x] != '':
        print("That space is already filled.")
        x = int(input(f"Player {player}, where would you place your mark (x): "))
        y = int(input(f"Player {player}, where would you place your mark (y): "))
    return (x, y)

class HumanPlayer:
    def __init__(self, mark):
        self.mark = mark
    
    def take_turn(self, board):
        print_board(board)
        x, y = get_player_move(self.mark, board)
        return (x, y)

class RandomAiPlayer:
    def __init__(self, mark):
        self.mark = mark
    
    def take_turn(self, board):
        # Select a random location on the board that is not filled.
        
        # Find the list of all empty locations
        empty_locs = []
        for y in range(3):
            for x in range(3):
                if board[y][x] == '':
                    empty_locs.append((x, y))
                    
        # Pick 1 at random
        return random.choice(empty_locs)

class BetterAiPlayer:
    def __init__(self, mark):
        self.mark = mark
    
    def take_turn(self, board):
        # Look for places the other player is about to get 3-in-a-row and block
        # them
        other_player = 'X' if self.mark == 'O' else 'O'
        for player in [self.mark, other_player]:
            for y in range(3):
                if board[y][0] == player and board[y][1] == player:
                    if board[y][2] == '':
                        return (2, y)
                if board[y][0] == player and board[y][2] == player:
                    if board[y][1] == '':
                        return (1, y)
                if board[y][1] == player and board[y][2] == player:
                    if board[y][0] == '':
                        return (0, y)
            for x in range(3):
                if board[0][x] == player and board[1][x] == player:
                    if board[2][x] == '':
                        return (x, 2)
                if board[0][x] == player and board[2][x] == player:
                    if board[1][x] == '':
                        return (x, 1)
                if board[1][x] == player and board[2][x] == player:
                    if board[0][x] == '':
                        return (x, 0)
            if board[0][0] == player and board[1][1] == player:
                if board[2][2] == '':
                    return (2, 2)
            if board[0][0] == player and board[2][2] == player:
                if board[1][1] == '':
                    return (1, 1)
            if board[1][1] == player and board[2][2] == player:
                if board[0][0] == '':
                    return (0, 0)
            
            if board[2][0] == player and board[1][1] == player:
                if board[0][2] == '':
                    return (2, 0)
            if board[2][0] == player and board[0][2] == player:
                if board[1][1] == '':
                    return (1, 1)
            if board[1][1] == player and board[0][2] == player:
                if board[2][0] == '':
                    return (0, 2)
                
        # The ordering in this list is significant!
        # Adding 2 to the index (mod 4) gives us the opposite corner.
        corners = [(0, 0), (2, 0), (2, 2), (0, 2)]
        if board == [['', '', ''], ['', other_player, ''], ['', '', '']]:
            # Randomly pick a corner if the other player moved first and took the middle
            return random.choice(corners)
        i = 0
        for corner_x, corner_y in corners:
            other_board = [['', '', ''], ['', '', ''], ['', '', '']]
            other_board[corner_y][corner_x] = other_player
            if board == other_board:
                return corners[(i + 2) % 4]
            i += 1
        
        # As a fall back, do things randomly
        
        # Find the list of all empty locations
        empty_locs = []
        for y in range(3):
            for x in range(3):
                if board[y][x] == '':
                    empty_locs.append((x, y))
                    
        # Pick 1 at random
        return random.choice(empty_locs)
        
        
if __name__ == "__main__":
    board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', ''],
    ]
    player1_mode = input("Player 1, AI or Human? ")
    player2_mode = input("Player 2, AI or Human? ")
    
    if player1_mode.lower() == "human":
        player1 = HumanPlayer('X')
    elif player1_mode.lower() == "ai":
        player1 = RandomAiPlayer('X')
        p1_ai = True
    elif player1_mode.lower() == "better ai" or player1_mode.lower() == 'wopr':
        player1 = BetterAiPlayer('X')
        p1_ai = True
        
    if player2_mode.lower() == "human":
        player2 = HumanPlayer('O')
    elif player2_mode.lower() == "ai":
        player2 = RandomAiPlayer('O')
        p2_ai = True
    elif player2_mode.lower() == "better ai" or player2_mode.lower() == 'wopr':
        player2 = BetterAiPlayer('O')
        p2_ai = True
    
    player = 'X'
    while get_winner(board) is None and not is_board_full(board):
        # print_board(board)
        # Get the player's move
        if player == 'X':
            x, y = player1.take_turn(board)
        else:
            x, y = player2.take_turn(board)
        # Update the board
        board[y][x] = player
        
        # Change player
        if player == 'X':
            player = 'O'
        else:
            player = 'X'
    
    print_board(board)    
    winner = get_winner(board)
    if winner is not None:
        print(f"Congrats {winner}, you won.")
    else:
        if p1_ai and p2_ai:
            print("A strange game. The only winning move is not to play.")
        else:
            print("Tie :(")