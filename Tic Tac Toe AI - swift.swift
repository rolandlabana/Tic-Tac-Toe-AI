
// c 2024 Roland Labana
// This swift version converted from my python version by GROK
//

import Foundation

// Global variables for print control
public var PRINT_ON = true
public var DEBUG_PRINT_ON = false

func print_on(_ s: String) {
    if PRINT_ON {
        print(s)
    }
}

func debug_print_on(_ s: String) {
    if DEBUG_PRINT_ON {
        print(s)
    }
}

// Player protocol and implementations
protocol Player {
    var symbol: Character { get }
    var strategy: String { get }
    func makeMove(in game: TicTacToe)
}

class HumanPlayer: Player {
    let symbol: Character
    let strategy = "Human Player"

    init(symbol: Character) {
        self.symbol = symbol
    }

    func makeMove(in game: TicTacToe) {
        while true {
            print("Enter your move for '\(symbol)' (0-8): ")
            if let moveStr = readLine(), let move = Int(moveStr), game.isValidMove(move) {
                game.makeMove(move, symbol: symbol)
                break
            } else {
                print("Invalid move. Try again.")
            }
        }
    }
}

class AIPlayer: Player {
    let symbol: Character
    let strategy: String
    private let aiStrategy: AI

    init(symbol: Character, strategy: AI) {
        self.symbol = symbol
        self.strategy = "AI Player"
        self.aiStrategy = strategy
    }

    func makeMove(in game: TicTacToe) {
        debug_print_on("\(symbol)'s AI is thinking...")
        let move = aiStrategy.determineMove(in: game)
        if game.isValidMove(move) {
            game.makeMove(move, symbol: symbol)
        } else {
            print("Error: Invalid move suggested by \(symbol)'s AI. Defaulting to random move.")
            game.makeRandomMove(for: symbol)
        }
    }
}

class TicTacToe {
    private var _board = Array(repeating: " ", count: 9)
    var board: [String] { return _board }  // Computed property for board access
    private var players: [Player]

    init(player1: Player, player2: Player) {
        self.players = [player1, player2]
    }

    func play() {
        while true {
            for player in players {
                displayBoard()
                player.makeMove(in: self)
                if checkWin() {
                    displayBoard()
                    print_on("\(player.symbol) wins!")
                    return
                }
                if isBoardFull() {
                    displayBoard()
                    print_on("It's a draw!")
                    return
                }
            }
        }
    }

    func isValidMove(_ move: Int) -> Bool {
        return _board[move] == " " && move >= 0 && move < 9
    }

    func makeMove(_ move: Int, symbol: Character) {
        _board[move] = String(symbol)
    }

    func checkWin() -> Bool {
        let winConditions: [[Int]] = [
            [0,1,2], [3,4,5], [6,7,8],  // Rows
            [0,3,6], [1,4,7], [2,5,8],  // Columns
            [0,4,8], [2,4,6]            // Diagonals
        ]
        
        for combo in winConditions {
            if Set(combo.map { _board[$0] }).count == 1 && _board[combo[0]] != " " {
                return true
            }
        }
        return false
    }

    func isBoardFull() -> Bool {
        return !_board.contains(" ")
    }

    func displayBoard() {
        for i in stride(from: 0, to: 9, by: 3) {
            print_on("\(_board[i]) | \(_board[i+1]) | \(_board[i+2])")
            if i < 6 {
                print_on("-----------")
            }
        }
        print_on("\n\n")
    }

    func makeRandomMove(for symbol: Character) {
        for i in 0..<9 {
            if isValidMove(i) {
                makeMove(i, symbol: symbol)
                break
            }
        }
    }
}

// AI Strategy Protocol
protocol AI {
    func determineMove(in game: TicTacToe) -> Int
}

// Example AI implementation (RandomAI)
class RandomAI: AI {
    func determineMove(in game: TicTacToe) -> Int {
        let possibleMoves = game.board.enumerated().filter { $1 == " " }.map { $0.0 }
        return possibleMoves.randomElement() ?? -1
    }
}

// Main function to run the game
if #available(macOS 10.15, *) {
    let player1 = HumanPlayer(symbol: "X")
    let player2 = AIPlayer(symbol: "O", strategy: RandomAI())
    let game = TicTacToe(player1: player1, player2: player2)
    game.play()
}