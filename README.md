See the slides for background and how to use the framework as well as the below:

//You need to name your AI “class” as follows:
{yourname}-AI
i.e., “Mike-AI”, “Jim-AI1”, “Jim-AI2”, “Mary-Jake-AI” instead of “RandomAI” as below

Python:
class RandomAI:
   def determine_move(self, game):  
	{your code here}
	return {integer 0-8 representing square to move to}

Java:
class RandomAI implements AI {
   @Override
   public int determineMove(TicTacToe game) {
{your code here}
return {integer 0-8 representing square to move to}
   }

// #################################

Main Program - Python
player1 = HumanPlayer('O')
player2 = HumanPlayer('X')
#player1 = AIPlayer('X', SimpleAI())     #ie: Jim-AI, Jim-AI2
#player2 = AIPlayer('O', RandomAI())   
game = TicTacToe(player1, player2)
game.play()

Main Program - Java
public static void main(String[] args) {
     Player player1 = new HumanPlayer('O');
     Player player2 = new HumanPlayer('X');
     //Player player1 = new AIPlayer('O', new SimpleAI());   // ie: "Jim-AI"
     //Player player2 = new AIPlayer('X', new RandomAI());
     TicTacToe game = new TicTacToe(player1, player2);
     game.play();
   }
}

// ####################################

game.board : list 0..8 of “ “  | “X” | “O”
game.is_valid_move(i) : returns True or False
game.check_win(theBoard) : Returns True or False   #I made the change we talked about in class - it now takes a list representing the board instead of using the actual board. You can pass it the actual board or a copy you update.

These are the only functions you should need to call from the code I provide.
You can create additional functions as needed. 
I will supply the full code after you come up with some approaches for the AI move function.


NOTE: Should we make it so that check_win() doesn’t check the actual current state but can take in a board configuration and report back win or lose?   YES - I've made this change!









