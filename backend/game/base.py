from abc import ABC
from dataclasses import dataclass, field
import uuid

@dataclass
class OnlineGame(ABC):
    name: str = field(default_factory=lambda: uuid.uuid4().hex)
    users: list = field(default_factory=list)
    
    
    
@dataclass
class TicTacToe(OnlineGame):
    board: list = field(default_factory=lambda: [["" for _ in range(3)] for _ in range(3)])
    current_player: int = 0
    winner: str = None
    game_over: bool = False
    
    def make_move(self, row: int, col: int) -> bool:
        if self.game_over:
            raise Exception("Game is already over")
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise Exception(f"Invalid move. {row=}, {col=}")
        if self.board[row][col] != "":
            raise Exception(f"Cell already occupied. {row=}, {col=}")
        if self.board[row][col] == "" and not self.game_over:
            self.board[row][col] = "X" if self.current_player == 0 else "O"
            self.check_winner()
            self.current_player = 1 - self.current_player
            return True
        return False
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                self.winner = row[0]
                self.game_over = True
                return
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.winner = self.board[0][col]
                self.game_over = True
                return
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != "" or
            self.board[0][2] == self.board[1][1] == self.board[2][0] != ""):
            self.winner = self.board[1][1]
            self.game_over = True
            return
    