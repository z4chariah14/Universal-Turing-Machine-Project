class TuringMachine3Tape:
    def __init__(self):
        # Initialize tapes
        self.tape1 = ["_" for _ in range(9)]  # Game board (3x3)
        self.tape2 = []  # Temporary computation space
        self.tape3 = []  # Rulebook
        self.head1 = 0  # Head position for Tape 1
        self.current_player = "O"  # Start with AI (O)

    def display_board(self):
        """Display the Tic-Tac-Toe board."""
        print("\nCurrent Board:")
        for i in range(0, 9, 3):
            print(" ".join(self.tape1[i:i + 3]))
        print()

    def check_winner(self):
        """Check if there's a winner or a draw."""
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for pos in winning_positions:
            line = [self.tape1[i] for i in pos]
            if line == ["X", "X", "X"]:
                return "X"
            if line == ["O", "O", "O"]:
                return "O"
        if "_" not in self.tape1:
            return "Draw"
        return None

    def evaluate_board(self):
        """Heuristic evaluation for AI (O)."""
        winner = self.check_winner()
        if winner == "O":
            return 10
        elif winner == "X":
            return -10
        return 0

    def minimax(self, is_maximizing):
        """Minimax algorithm to determine the best move."""
        score = self.evaluate_board()
        if score != 0 or "_" not in self.tape1:
            return score

        if is_maximizing:
            best_score = float("-inf")
            for i in range(9):
                if self.tape1[i] == "_":
                    self.tape1[i] = "O"
                    score = self.minimax(False)
                    self.tape1[i] = "_"
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if self.tape1[i] == "_":
                    self.tape1[i] = "X"
                    score = self.minimax(True)
                    self.tape1[i] = "_"
                    best_score = min(best_score, score)
            return best_score

    def ai_move(self):
        """AI (O) makes the best move."""
        best_score = float("-inf")
        best_move = None
        for i in range(9):
            if self.tape1[i] == "_":
                self.tape1[i] = "O"
                score = self.minimax(False)
                self.tape1[i] = "_"
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            self.tape1[best_move] = "O"

    def player_move(self):
        """Get the player's (X) move."""
        while True:
            try:
                move = int(input("Enter your move (0-8): "))
                if 0 <= move < 9 and self.tape1[move] == "_":
                    self.tape1[move] = "X"
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Enter a number between 0 and 8.")

    def play_game(self):
        """Main loop to play the game."""
        self.display_board()
        while True:
            if self.current_player == "X":
                self.player_move()
            else:
                print("AI is thinking...")
                self.ai_move()
            self.display_board()

            result = self.check_winner()
            if result:
                if result == "Draw":
                    print("It's a draw!")
                else:
                    print(f"{result} wins!")
                break
            self.current_player = "X" if self.current_player == "O" else "O"


# Run the simulation
if __name__ == "__main__":
    tm_game = TuringMachine3Tape()
    tm_game.play_game()
