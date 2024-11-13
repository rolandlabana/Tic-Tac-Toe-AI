
# (c) 2024 Roland Labana

import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            try:
                move = int(input(f"Enter your move for '{self.symbol}' (0-8): "))
                if game.is_valid_move(move):
                    game.make_move(move, self.symbol)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")

# Template for AI Player
class AIPlayer(Player):
    def __init__(self, symbol, strategy):
        super().__init__(symbol)
        self.strategy = strategy

    def make_move(self, game):
        # Here's where students would implement their AI logic
        print(f"{self.symbol}'s AI is thinking...")
        move = self.strategy.determine_move(game)
        if game.is_valid_move(move):
            game.make_move(move, self.symbol)
        else:
            print(f"Error: Invalid move suggested by {self.symbol}'s AI. Defaulting to random move.")
            # Default to random move if AI suggests an invalid move
            for i in range(9):
                if game.is_valid_move(i):
                    game.make_move(i, self.symbol)
                    break

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]
        self.players = [player1, player2]
        #self.display_board()  # Display the board initially


    def play(self):
         while True:
            for player in self.players:
                self.display_board()
                player.make_move(self)
                if self.check_win(game.board):
                    self.display_board()
                    print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    self.display_board()
                    print("It's a draw!")
                    return

    def is_valid_move(self, move):
        return self.board[move] == ' ' and 0 <= move <= 8

    def make_move(self, move, symbol):
        self.board[move] = symbol

    def check_win(self, theBoard):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def is_board_full(self):
        return ' ' not in self.board

    def display_board(self):
        #print("\nCurrent Board State:")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print ()

        

# Example of a simple AI strategy - pick FIRST available space 0 - 8
class SimpleAI:
    def determine_move(self, game):
        # Simple strategy: check for winning move, then blocking opponent's win, then take first open space
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Assuming this AI plays 'X'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Check if opponent ('O') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        # If no immediate winning or blocking move, take first available space
        for i in range(9):
            if game.is_valid_move(i):
                return i
            
# Example of a simple AI strategy - pick a RANDOM available space 0 - 8
class RandomAI:
    def determine_move(self, game):
        possibleMoves = []
        #add all open spaces into a list to then randomly choose one
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)
        return (random.choice(possibleMoves))
# this AI makes a list of possible moves, then preferred moves, then picks a random preferred
# move. It has no block function because there were too many bugs.
class Felix_Jessie_AI:
   def determine_player(self, game):
       p1 = True
       o = game.board.count("O")
       x = game.board.count("X")
       if x>o:
           p1 = False
       return p1
   def determine_move(self, game):  
        rows = 3 #this will change depending on the amount of rows in a board
        possibleMoves = []
        moves = []
        #look for a possible win (works by subbing in "O" and using the check_win)
        for spot in range (0,9):
            if game.is_valid_move(spot):
                game.board[spot] = "O"
                win = game.check_win(game.board) #check win returns true or false using any(), which checks for true items in a list
                if win:
                    print("Good Game!")
                    win_spot = spot
                    game.board[spot] = ' '
                    return win_spot
                game.board[spot] = ' '
        #look for a possible spot (works the same as the previous check but for the opposite purpose)
        for spot in range(0,9):
            if game.is_valid_move(spot):
                game.board[spot] = "X"
                lose = game.check_win(game.board)
                if lose:
                    print ("BLOCK")
                    block_spot = spot
                    game.board[spot] = ' '
                    return block_spot
                game.board[spot] = ' '
                possibleMoves.append(spot)
        # check for friendly neighbors on top, to the sides, and diagonally,
        # if the list goes out of range it just passes
        # this appends to a list of good moves called moves
        for m in possibleMoves:
            idx = m
            try:
                if game.board[idx-1]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[idx+1]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[idx-(len(game.board)//rows)]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[idx+(len(game.board)//rows)]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[(idx-(len(game.board)//rows)+1)]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[(idx+(len(game.board)//rows))+1]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[(idx-(len(game.board)//rows)-1)]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            try:
                if game.board[(idx+(len(game.board)//rows))-1]== 'O':
                    moves.append(m)
            except IndexError:
                pass
            # this is to set up a potential trap
            if m == 0 or m == 2 or m ==6 or m == 8:
                    moves.append(m)
            # we want this to only happen when the AI is p2 so that it can block possible traps
            if m == 4 and not self.determine_player(game):
                return m
        # if there are no good moves, it picks the first one
        if len(moves)==0:
            return possibleMoves[0]
        # picks a random good move
        return moves[random.randint(0, len(moves)-1)]
   
class MinimaxAI:
    def FJ_minimax(self, game, depth, is_maximizing):
        #BASE CASE(s) check for win or tie

        if game.check_win(game.board):
            if not is_maximizing:
                return 1
            else:
                return -1
        elif game.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float('inf') #best score starts low at negative infinity
            for move in range(9): #each space in 3x3 grid
                if game.is_valid_move(move):
                    game.make_move(move, 'O') #test move O
                    score = self.FJ_minimax(game, depth+1, False) #recursion! (calls as minimizer)
                    game.board[move] = ' ' #undo move
                    best_score = max(score, best_score) #update score
            return best_score
        else: #is minimizer
            best_score = float('inf') #set best at infinity (so we can only go down)
            for move in range(9): #pretty much the same
                if game.is_valid_move(move):
                    game.make_move(move, 'X') #moves X bc this is minimizer
                    score = self.FJ_minimax(game, depth+1, True) #recurs as max
                    game.board[move] = ' '
                    best_score = min(score, best_score)
            return best_score
         
    def determine_move(self, game):
        best_move = None
        best_score = -float('inf') #set best score to negative infinity

        for move in range(9): #loop through all possible moves on the 3x3 board
            if game.is_valid_move(move):
                game.make_move(move, 'O') #ai test plays O 
                score = self.FJ_minimax(game, 0, False)  #call minimax using min for the next player.
                game.board[move] = ' '  #undo move
                #update the best score if one is found
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move
            
            
if __name__ == "__main__":
    # Here you can decide how to initialize players
    # For example, to test with one human and one AI:
    # player1 = HumanPlayer('X')
    # player2 = AIPlayer('O', SimpleAI())
    # game = TicTacToe(player1, player2)X
    # game.play()

    # For students' AI competition:
    #player1 = HumanPlayer('X')
    player1 = HumanPlayer('X')
    #player1 = AIPlayer('X', SimpleAI())  # Replace with student AI implementation - name function with your name ie: "Jim-AI"
    #player2 = AIPlayer('X', RandomAI())  # Replace with another student AI implementation or the same for testing ie: "Mary-AI"
    player2 = AIPlayer('O', MinimaxAI())
    game = TicTacToe(player1, player2)
    game.play()