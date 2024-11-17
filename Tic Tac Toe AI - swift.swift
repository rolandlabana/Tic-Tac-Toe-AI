
// c 2024 Roland Labana
// This swift version converted from my python version by GROK
//

import Foundation

import SwiftUI

struct TicTacToeBoardView: View {
    let board: [String]
    
    var body: some View {
        VStack(spacing: 5) {
            ForEach(0..<3, id: \.self) { row in
                HStack(spacing: 5) {
                    ForEach(0..<3, id: \.self) { col in
                        let index = row * 3 + col
                        Text(board[index])
                            .font(.system(size: 40))
                            .frame(width: 60, height: 60)
                            .background(Color.white)
                            .border(Color.black, width: 1)
                    }
                }
            }
        }
        .padding()
    }
}

struct TicTacToeBoardView_Previews: PreviewProvider {
    static var previews: some View {
        TicTacToeBoardView(board: Array(repeating: " ", count: 9))
    }
}

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

    func undoMove(at move: Int) {
        _board[move] = " "
    }

    init(player1: Player, player2: Player) {
        self.players = [player1, player2]
    }

    func play() {
        while true {
            for player in players {
                displayBoard()
                displayGraphicalBoard()  // only works in app environment
                player.makeMove(in: self)
                if checkWin() {
                    displayBoard()
                    displayGraphicalBoard()  // only works in app environment
                    print_on("\(player.symbol) wins!")
                    return
                }
                if isBoardFull() {
                    displayBoard()
                    displayGraphicalBoard()  // only works in app environment
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

extension TicTacToe {
    func displayGraphicalBoard() {
        let view = TicTacToeBoardView(board: board)
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 300, height: 300),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false)
        
        window.center()
        window.title = "Tic-Tac-Toe"
        window.contentView = NSHostingView(rootView: view)
        window.makeKeyAndOrderFront(nil)
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

// Minimax AI Implementation
class MinimaxAI: AI {
    let symbol: Character
    let opponentSymbol: Character
    
    init(symbol: Character) {
        self.symbol = symbol
        self.opponentSymbol = symbol == "X" ? "O" : "X"
    }
    
    func determineMove(in game: TicTacToe) -> Int {
        let (_, move) = minimax(game: game, isMaximizing: true)
        return move
    }
    
    private func minimax(game: TicTacToe, isMaximizing: Bool) -> (score: Int, move: Int) {
        if game.checkWin() {
            return (isMaximizing ? -1 : 1, -1)  // -1 for loss, 1 for win
        }
        if game.isBoardFull() {
            return (0, -1)  // 0 for draw
        }
        
        var bestMove = -1
        
        if isMaximizing {
            var bestScore = Int.min
            for move in 0..<9 where game.isValidMove(move) {
                game.makeMove(move, symbol: symbol)
                let (score, _) = minimax(game: game, isMaximizing: false)
                game.undoMove(at: move)  // Use the new undoMove method instead of directly setting _board
                if score > bestScore {
                    bestScore = score
                    bestMove = move
                }
            }
            return (bestScore, bestMove)
        } else {
            var bestScore = Int.max
            for move in 0..<9 where game.isValidMove(move) {
                game.makeMove(move, symbol: opponentSymbol)
                let (score, _) = minimax(game: game, isMaximizing: true)
                game.undoMove(at: move)  // Use the new undoMove method
                if score < bestScore {
                    bestScore = score
                    bestMove = move
                }
            }
            return (bestScore, bestMove)
        }
    }
}

// Main function to run the game
if #available(macOS 10.15, *) {
    let player1 = HumanPlayer(symbol: "X")
    let player2 = AIPlayer(symbol: "O", strategy: MinimaxAI(symbol: "O"))

    //let player2 = AIPlayer(symbol: "O", strategy: RandomAI())
    let game = TicTacToe(player1: player1, player2: player2)
    game.play()
}