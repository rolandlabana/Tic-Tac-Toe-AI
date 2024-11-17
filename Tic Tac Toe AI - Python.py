
# (c) 2024 Roland Labana

import random

PRINT_ON = True
DEBUG_PRINT_ON = False

def print_on(s):
    if PRINT_ON == True:
        print (s)

def debug_print_on(s):
    if DEBUG_PRINT_ON == True:
        print (s)


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

class HumanPlayer(Player):
     def __init__(self, symbol):
         super().__init__(symbol)
         self.strategy = "Human Player"

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
        debug_print_on(f"{self.symbol}'s AI is thinking...")
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
                    print_on(f"                    {player.symbol} wins!")
                    if player.symbol == "X": input("press any key to cont..")
                    return (player.symbol)  #return who wins
                if self.is_board_full():
                    self.display_board()
                    print_on("                    It's a draw!")
                    return ('tie')  #tie

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

        debug_print_on(f"Current board state: {theBoard} (length: {len(theBoard)})")

        # Ensure the board is exactly 9 elements long
        if len(theBoard) != 9:
            raise ValueError("Board should have exactly 9 positions.")
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)
    
    def check_win2(self, theBoard):
        win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        print(f"Current board state: {theBoard} (length: {len(theBoard)})")

        # Ensure the board is exactly 9 elements long
        if len(theBoard) != 9:
            raise ValueError("Board should have exactly 9 positions.")
    
        # Check for a win in any of the winning combinations
        for combo in win_conditions:
            if theBoard[combo[0]] == theBoard[combo[1]] == theBoard[combo[2]] != ' ':
                return True  # Return True if any winning condition is met
    
        return False  # No win detected


    def is_board_full(self):
        return ' ' not in self.board

    def display_board(self):
        #print("\nCurrent Board State:")
        for i in range(0, 9, 3):
            print_on(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print_on("-----------")
        print_on ("")
        print_on("")

     #Helper function for JudahsCoolAI
    def make_temporary_move(self, move, symbol):
        original_symbol = self.board[move] #Have a place to keep what the original board looks like withouto making a move
        self.board[move] = symbol #This is having the player "move" to a pos on the board. The player doesn't actually move
        is_winning = self.check_win(self.board) #Check if that player move is a winning one
        self.board[move] = original_symbol  # reset it back to its original state
        return is_winning

        

# Example of a simple AI strategy - pick FIRST available space 0 - 8
class SimpleAI:
    def determine_move(self, game):
        # Simple strategy: check for winning move, then blocking opponent's win, then take first open space
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Assuming this AI plays 'X'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    debug_print_on ("     GOING FOR WIN")
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Check if opponent ('O') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    debug_print_on ("     BLOCKING OPPONENT")
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
    
class AaronMikeAI:
    def determine_move(self, game):
        possibleMoves = []
        #add all open spaces into a list to then randomly choose one
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)
        
        #check if we have winning move
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Assuming this AI plays 'O'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check

        #check if enemy has winning move
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Check if opponent ('X') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check

        if 4 in possibleMoves:
            return 4
        
        for corneroption in [0, 2, 6, 8]:
            if corneroption in possibleMoves:
                return corneroption
            
        return random.choice(possibleMoves)
    
    #########################
   #Priotitizes center then corners then random spots if corners and center is taken. Follows this strat unless there is a winning move.
class JudahsCoolAI:
    def determine_move(self, game):
        # Lambda to check if a move is winning
        is_winning_move = lambda symbol, move: (game.is_valid_move(move) and game.make_temporary_move(move, symbol)) #It doesn't know move and symbol yet until we call it with the values
        
        # pick middle if u can
        if game.is_valid_move(4):
            return 4

        #This'll check for a winning move for both the AI and the opponent and also where you call the lambda
        for symbol in ('O', 'X'):  
            for move in range(9):
                if is_winning_move(symbol, move):
                    return move

        # pick corners if u can
        corners = [i for i in [0, 2, 6, 8] if game.is_valid_move(i)]
        if corners:
            return random.choice(corners)

        # Pick a random available spot if there's no moves
        possible_moves = [i for i in range(9) if game.is_valid_move(i)]
        return random.choice(possible_moves)

# Plays based off of the order of the numbers in pi
class DavidAI:     
    def determine_move(self, game):
        #print(game.players[1].symbol) - exmample to access symbols from here
        empty = []
        for z in range(9):
            if game.is_valid_move(z):
                empty.append(z+1)
                
        # pi 3.1415926535897
        for z in range(len(empty)):
            if empty[z] == 3:
                return 2
        for z in range(len(empty)):
            if empty[z] == 1:
                return 0
        for z in range(len(empty)):
            if empty[z] == 4:
                return 3
        #Skip repeated - 1
        for z in range(len(empty)):
            if empty[z] == 5:
                return 4
        for z in range(len(empty)):
            if empty[z] == 9:
                return 8
        for z in range(len(empty)):
            if empty[z] == 2:
                return 1
        for z in range(len(empty)):
            if empty[z] == 6:
                return 5
        #Skip repeated - 5
        #Skip repeated - 3
        #Skip repeated - 5
        for z in range(len(empty)):
            if empty[z] == 8:
                return 7
        #Skip repeated - 9
        for z in range(len(empty)):
            if empty[z] == 7:
                return 6
            
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
                    print_on ("Good Game!")
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



#-------------------------------- MiniMax ----------------------
class MinimaxAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.nodes_evaluated = 0  # Count of nodes checked
        self.max_depth_reached = 0  # Track max depth reached

    def determine_move(self, game):
        # Reset tracking variables for each new move
        self.nodes_evaluated = 0
        self.max_depth_reached = 0

        best_score = -float('inf')
        best_move = None

        for move in range(9):
            if game.is_valid_move(move):
                #debug_print_on("move: " , move)
                game.board[move] = self.symbol  # Make a temporary move
                score = self.minimax(game, 0, False)
                game.board[move] = ' '  # Undo move

                if score > best_score:
                    best_score = score
                    best_move = move

        debug_print_on(f"Nodes evaluated: {self.nodes_evaluated}")
        debug_print_on(f"Max depth reached: {self.max_depth_reached}")
        return best_move

    def minimax(self, game, depth, is_maximizing):
        self.nodes_evaluated += 1
        self.max_depth_reached = max(self.max_depth_reached, depth)

        if game.check_win(game.board):
            return -1 if is_maximizing else 1  # Lose if maximizing, win if minimizing
        elif game.is_board_full():
            return 0  # Draw

        if is_maximizing:
            max_eval = -float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.symbol
                    eval = self.minimax(game, depth + 1, False)
                    game.board[move] = ' '
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.opponent_symbol
                    eval = self.minimax(game, depth + 1, True)
                    game.board[move] = ' '
                    min_eval = min(min_eval, eval)
            return min_eval

#_________________ MiniMax - enhanced stats ___________________
class MinimaxAI_stats:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.nodes_evaluated = 0  # Total nodes evaluated
        self.max_depth_reached = 0  # Maximum depth reached in a single call
        self.config_nodes = []  # Track nodes visited for each configuration

    def determine_move(self, game):
        # Reset tracking variables for each move
        self.nodes_evaluated = 0
        self.max_depth_reached = 0
        self.config_nodes = []

        best_score = -float('inf')
        best_move = None

        for move in range(9):
            if game.is_valid_move(move):
                game.board[move] = self.symbol  # Make a temporary move
                score = self.minimax(game, 0, False)
                game.board[move] = ' '  # Undo move

                if score > best_score:
                    best_score = score
                    best_move = move

        debug_print_on(f"Nodes evaluated: {self.nodes_evaluated}")
        debug_print_on(f"Max depth reached: {self.max_depth_reached}")
        debug_print_on("Node visitations per configuration:")
        for config in self.config_nodes:
            debug_print_on(config)
        
        return best_move

    def minimax(self, game, depth, is_maximizing):
        # Track the current board state and number of nodes evaluated at this depth
        board_state = "".join(game.board)
        current_nodes = {'board_state': board_state, 'depth': depth, 'nodes_visited': 0}
        self.config_nodes.append(current_nodes)

        self.nodes_evaluated += 1
        current_nodes['nodes_visited'] += 1  # Increment nodes for this configuration
        self.max_depth_reached = max(self.max_depth_reached, depth)

        # Terminal condition checks
        if game.check_win(game.board):
            return -1 if is_maximizing else 1  # Lose if maximizing, win if minimizing
        elif game.is_board_full():
            return 0  # Draw

        # Recursive minimax search
        if is_maximizing:
            max_eval = -float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.symbol
                    eval = self.minimax(game, depth + 1, False)
                    game.board[move] = ' '
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.opponent_symbol
                    eval = self.minimax(game, depth + 1, True)
                    game.board[move] = ' '
                    min_eval = min(min_eval, eval)
            return min_eval


#________________________ MINIMAX Depth limit with Eval________________
class MinimaxAI_depth_Eval:
    def __init__(self, symbol, max_depth=None):
        self.symbol = symbol
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.max_depth = max_depth if max_depth is not None else float('inf')  # Full depth if not specified

    def determine_move(self, game):
        _, move, self.nodes_visited = self.minimax(game, self.symbol, depth=0)
        return move

    def minimax(self, game, current_symbol, depth):
        if game.check_win(game.board):
            return (1 if current_symbol == self.opponent_symbol else -1, None, 1)  # Win, no move, node count 1
        if game.is_board_full():
            return 0, None, 1  # Draw, no move, node count 1
        if depth >= self.max_depth:
            eval_score = self.evaluate(game)  # Use evaluation score if max depth reached
            #print (f"eval_score:  {eval_score} depth: {depth}")
            return eval_score, None, 1  # Node count 1 at this depth

        best_score = float('-inf') if current_symbol == self.symbol else float('inf')
        best_move = None
        nodes_visited = 0

        for move in range(9):
            if game.is_valid_move(move):
                game.board[move] = current_symbol
                score, _, node_count = self.minimax(
                    game, 
                    self.opponent_symbol if current_symbol == self.symbol else self.symbol, 
                    depth + 1
                )
                nodes_visited += node_count
                game.board[move] = ' '  # Undo move

                if current_symbol == self.symbol:
                    if score > best_score:
                        best_score, best_move = score, move
                else:
                    if score < best_score:
                        best_score, best_move = score, move

        debug_print_on (f"best_score:  {score} depth: {depth}")
        return best_score, best_move, nodes_visited + 1  # Total nodes visited for this call

    def evaluate(self, game):
        score = 0
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for condition in win_conditions:
            player_count = sum(1 for i in condition if game.board[i] == self.symbol)
            opponent_count = sum(1 for i in condition if game.board[i] == self.opponent_symbol)

            if player_count == 2 and opponent_count == 0:
                score += 10  # Favorable near-win
            elif player_count == 1 and opponent_count == 0:
                score += 1  # Slightly favorable

            if opponent_count == 2 and player_count == 0:
                score -= 10  # Opponent near-win
            elif opponent_count == 1 and player_count == 0:
                score -= 1  # Slightly unfavorable

        return score





###############################################################
# MAIN
################################################################
if __name__ == "__main__":
    # Here you can decide how to initialize players
    # For example, to test with one human and one AI:
    # player1 = HumanPlayer('X')
    # player2 = AIPlayer('O', SimpleAI())
    # game = TicTacToe(player1, player2)
    # game.play()

    # Examples of ways to set up the players:
    #player1 = HumanPlayer('X')
    #player2 = HumanPlayer('O')
    #player2 = AIPlayer('X', SimpleAI())  # Replace with another student AI implementation or the same for testing ie: "Mary-AI"
    #player1 = AIPlayer('X', RandomAI())  # Replace with another student AI implementation or the same for testing ie: "Mary-AI"
    #player1 = AIPlayer('O', MinimaxAI('O'))  
    #player2 = AIPlayer('O', MinimaxAI_depth('O', 1))  

    player1 = AIPlayer('X', RandomAI())
    player2 = AIPlayer('O', MinimaxAI_depth_Eval('O', 6))  # Replace with student AI implementation - name function with your name ie: "Jim-AI"

    wins = [0,0,0]

    numGames = int(input("How many games to play? "))
    for currGame in range (1,numGames+1):
        game = TicTacToe(player1, player2)
        print_on(f"Game starting... {currGame} \n")
        print_on ("#############")
        winner = game.play()

        #keep count of the number of wins
        if winner == "X" and player1.symbol == "X": wins[1]= wins[1] + 1
        if winner == "X" and player2.symbol == "X": wins[2]= wins[2] + 1

        if winner == "O" and player1.symbol == "O": wins[1]= wins[1] + 1
        if winner == "O" and player2.symbol == "O": wins[2]= wins[2] + 1

        if winner == "tie": wins[0]= wins[0] + 1

    #done playing all the games, print the results
    print ("\nRESULTS - ", numGames, "games played -")
    print ("Player 1: ", wins[1], round((wins[1]/numGames)*100), "%","   Sym = ", player1.symbol, "  Strat = ", player1.strategy)
    print ("Player 2: ", wins[2], round((wins[2]/numGames)*100), "%","   Sym = ", player2.symbol, "  Strat = ", player2.strategy)
    print ("Ties    : ", wins[0], round((wins[0]/numGames)*100), "%")
    print ()


