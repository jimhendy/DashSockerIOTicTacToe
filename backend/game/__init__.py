from dataclasses import dataclass, field

@dataclass
class TicTacToe:
    board: list = field(default_factory=lambda: [[' ']*3 for _ in range(3)])
    player: str = 'X'
    winner: str = ''
    moves: int = 0

    def make_move(self, x, y):
        if self.winner:
            return 'Game is over'
        if self.board[x][y] == ' ':
            self.board[x][y] = self.player
            self.moves += 1
            if self.check_winner():
                self.winner = self.player
            elif self.moves == 9:
                self.winner = 'Draw'
            self.player = 'X' if self.player == 'O' else 'O'
            return 'Move made'
        return 'Invalid move'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def reset(self):
        self.board = [[' ']*3 for _ in range(3)]
        self.player = 'X'
        self.winner = ''
        self.moves = 0

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.board])