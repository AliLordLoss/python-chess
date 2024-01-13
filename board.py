import copy
from datetime import datetime


class Board:
    def __init__(self):
        self.board = [
            [
                "RookB",
                "KnightB",
                "BishopB",
                "QueenB",
                "KingB",
                "BishopB",
                "KnightB",
                "RookB",
            ],
            ["PawnB", "PawnB", "PawnB", "PawnB", "PawnB", "PawnB", "PawnB", "PawnB"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["PawnW", "PawnW", "PawnW", "PawnW", "PawnW", "PawnW", "PawnW", "PawnW"],
            [
                "RookW",
                "KnightW",
                "BishopW",
                "QueenW",
                "KingW",
                "BishopW",
                "KnightW",
                "RookW",
            ],
        ]
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.turn = True
        self.black_dead = []
        self.white_dead = []
        self.choices = []
        self.chosen = None
        self.pawn_at_end = None
        self.beginning = datetime.now()

    def get_elapsed_time(self):
        return str(datetime.now() - self.beginning)[2:7]

    def is_checkmated(self):
        if self.is_checked():
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != "" and self.get_possible_moves(i, j):
                        if self.turn and self.board[i][j][-1] == "W":
                            return False
                        if (not self.turn) and self.board[i][j][-1] == "B":
                            return False
            return True

    def is_checked(self):
        if self.turn:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != "" and self.board[i][j][-1] == "B":
                        if self.white_king in self.get_moves(i, j):
                            return True
            return False
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != "" and self.board[i][j][-1] == "W":
                        if self.black_king in self.get_moves(i, j):
                            return True
            return False

    def move(self, src, dst):
        self.board[dst[0]][dst[1]] = self.board[src[0]][src[1]]
        self.board[src[0]][src[1]] = ""
        if self.board[dst[0]][dst[1]] == "KingW":
            self.white_king = dst
        if self.board[dst[0]][dst[1]] == "KingB":
            self.black_king = dst

    def make_move(self, src, dst):
        if self.turn:
            if self.board[src[0]][src[1]] == "PawnW" and dst[0] == 0:
                self.pawn_at_end = dst
            if self.board[dst[0]][dst[1]] != "":
                self.black_dead.append(self.board[dst[0]][dst[1]])
        else:
            if self.board[src[0]][src[1]] == "PawnB" and dst[0] == 7:
                self.pawn_at_end = dst
            if self.board[dst[0]][dst[1]] != "":
                self.white_dead.append(self.board[dst[0]][dst[1]])
        self.move(src, dst)

    def get_rook_moves(self, i, j):
        moves = []
        counter = 1
        while i + counter < 8:
            if self.board[i + counter][j] != "":
                if self.board[i + counter][j][-1] != self.board[i][j][-1]:
                    moves.append((i + counter, j))
                break
            moves.append((i + counter, j))
            counter += 1
        counter = 1
        while i - counter >= 0:
            if self.board[i - counter][j] != "":
                if self.board[i - counter][j][-1] != self.board[i][j][-1]:
                    moves.append((i - counter, j))
                break
            moves.append((i - counter, j))
            counter += 1
        counter = 1
        while j + counter < 8:
            if self.board[i][j + counter] != "":
                if self.board[i][j + counter][-1] != self.board[i][j][-1]:
                    moves.append((i, j + counter))
                break
            moves.append((i, j + counter))
            counter += 1
        counter = 1
        while j - counter >= 0:
            if self.board[i][j - counter] != "":
                if self.board[i][j - counter][-1] != self.board[i][j][-1]:
                    moves.append((i, j - counter))
                break
            moves.append((i, j - counter))
            counter += 1
        return moves

    def get_bishop_moves(self, i, j):
        moves = []
        counter = 1
        while i + counter < 8 and j + counter < 8:
            if self.board[i + counter][j + counter] != "":
                if self.board[i + counter][j + counter][-1] != self.board[i][j][-1]:
                    moves.append((i + counter, j + counter))
                break
            moves.append((i + counter, j + counter))
            counter += 1
        counter = 1
        while i - counter >= 0 and j - counter >= 0:
            if self.board[i - counter][j - counter] != "":
                if self.board[i - counter][j - counter][-1] != self.board[i][j][-1]:
                    moves.append((i - counter, j - counter))
                break
            moves.append((i - counter, j - counter))
            counter += 1
        counter = 1
        while i - counter >= 0 and j + counter < 8:
            if self.board[i - counter][j + counter] != "":
                if self.board[i - counter][j + counter][-1] != self.board[i][j][-1]:
                    moves.append((i - counter, j + counter))
                break
            moves.append((i - counter, j + counter))
            counter += 1
        counter = 1
        while i + counter < 8 and j - counter >= 0:
            if self.board[i + counter][j - counter] != "":
                if self.board[i + counter][j - counter][-1] != self.board[i][j][-1]:
                    moves.append((i + counter, j - counter))
                break
            moves.append((i + counter, j - counter))
            counter += 1
        return moves

    def get_moves(self, i, j):
        moves = []
        if self.board[i][j] == "PawnB":
            try:
                if self.board[i + 1][j] == "":
                    moves.append((i + 1, j))
                    if i == 1 and self.board[i + 2][j] == "":
                        moves.append((i + 2, j))
            except IndexError:
                pass
            try:
                if self.board[i + 1][j + 1][-1] == "W":
                    moves.append((i + 1, j + 1))
            except IndexError:
                pass
            try:
                if j - 1 < 0:
                    raise IndexError
                if self.board[i + 1][j - 1][-1] == "W":
                    moves.append((i + 1, j - 1))
            except IndexError:
                pass
            return moves
        elif self.board[i][j] == "PawnW":
            try:
                if self.board[i - 1][j] == "":
                    moves.append((i - 1, j))
                    if i == 6 and self.board[i - 2][j] == "":
                        moves.append((i - 2, j))
            except IndexError:
                pass
            try:
                if self.board[i - 1][j + 1][-1] == "B":
                    moves.append((i - 1, j + 1))
            except IndexError:
                pass
            try:
                if j - 1 < 0:
                    raise IndexError
                if self.board[i - 1][j - 1][-1] == "B":
                    moves.append((i - 1, j - 1))
            except IndexError:
                pass
            return moves
        elif "Rook" in self.board[i][j]:
            return self.get_rook_moves(i, j)
        elif "Bishop" in self.board[i][j]:
            return self.get_bishop_moves(i, j)
        elif "Knight" in self.board[i][j]:
            if (
                i + 2 < 8
                and j - 1 >= 0
                and (
                    self.board[i + 2][j - 1] == ""
                    or self.board[i + 2][j - 1][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i + 2, j - 1))
            if (
                i + 2 < 8
                and j + 1 < 8
                and (
                    self.board[i + 2][j + 1] == ""
                    or self.board[i + 2][j + 1][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i + 2, j + 1))
            if (
                i - 2 >= 0
                and j - 1 >= 0
                and (
                    self.board[i - 2][j - 1] == ""
                    or self.board[i - 2][j - 1][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i - 2, j - 1))
            if (
                i - 2 >= 0
                and j + 1 < 8
                and (
                    self.board[i - 2][j + 1] == ""
                    or self.board[i - 2][j + 1][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i - 2, j + 1))
            if (
                i + 1 < 8
                and j - 2 >= 0
                and (
                    self.board[i + 1][j - 2] == ""
                    or self.board[i + 1][j - 2][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i + 1, j - 2))
            if (
                i - 1 >= 0
                and j - 2 >= 0
                and (
                    self.board[i - 1][j - 2] == ""
                    or self.board[i - 1][j - 2][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i - 1, j - 2))
            if (
                i + 1 < 8
                and j + 2 < 8
                and (
                    self.board[i + 1][j + 2] == ""
                    or self.board[i + 1][j + 2][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i + 1, j + 2))
            if (
                i - 1 >= 0
                and j + 2 < 8
                and (
                    self.board[i - 1][j + 2] == ""
                    or self.board[i - 1][j + 2][-1] != self.board[i][j][-1]
                )
            ):
                moves.append((i - 1, j + 2))
            return moves
        elif "Queen" in self.board[i][j]:
            moves = self.get_rook_moves(i, j)
            moves.extend(self.get_bishop_moves(i, j))
            return moves
        elif "King" in self.board[i][j]:
            if i + 1 < 8:
                if (
                    self.board[i + 1][j] == ""
                    or self.board[i + 1][j][-1] != self.board[i][j][-1]
                ):
                    moves.append((i + 1, j))
                if j + 1 < 8 and (
                    self.board[i + 1][j + 1] == ""
                    or self.board[i + 1][j + 1][-1] != self.board[i][j][-1]
                ):
                    moves.append((i + 1, j + 1))
                if j - 1 >= 0 and (
                    self.board[i + 1][j - 1] == ""
                    or self.board[i + 1][j - 1][-1] != self.board[i][j][-1]
                ):
                    moves.append((i + 1, j - 1))
            if i - 1 >= 0:
                if (
                    self.board[i - 1][j] == ""
                    or self.board[i - 1][j][-1] != self.board[i][j][-1]
                ):
                    moves.append((i - 1, j))
                if j + 1 < 8 and (
                    self.board[i - 1][j + 1] == ""
                    or self.board[i - 1][j + 1][-1] != self.board[i][j][-1]
                ):
                    moves.append((i - 1, j + 1))
                if j - 1 >= 0 and (
                    self.board[i - 1][j - 1] == ""
                    or self.board[i - 1][j - 1][-1] != self.board[i][j][-1]
                ):
                    moves.append((i - 1, j - 1))
            if j + 1 < 8 and (
                self.board[i][j + 1] == ""
                or self.board[i][j + 1][-1] != self.board[i][j][-1]
            ):
                moves.append((i, j + 1))
            if j - 1 >= 0 and (
                self.board[i][j - 1] == ""
                or self.board[i][j - 1][-1] != self.board[i][j][-1]
            ):
                moves.append((i, j - 1))
            return moves
        return moves

    def get_possible_moves(self, i, j):
        main_board = copy.deepcopy(self.board)
        king_position = (self.white_king, self.black_king)
        moves = self.get_moves(i, j)
        possible_moves = []
        for move in moves:
            self.board = copy.deepcopy(main_board)
            self.move((i, j), move)
            if not self.is_checked():
                possible_moves.append(move)
            self.white_king, self.black_king = king_position
        self.board = copy.deepcopy(main_board)
        return possible_moves

    def game_manager(self, clicked):
        j, i = clicked
        if (self.is_checkmated() and 300 < i < 380 and 300 < j < 380) or (
            (not self.is_checkmated()) and 680 < j < 840 and 60 < i < 220
        ):
            self.__init__()
            return
        if self.pawn_at_end is not None:
            m, n = self.pawn_at_end
            if 260 < i < 420:
                if 20 < j < 180:
                    self.board[m][n] = "Queen" + self.board[m][n][-1]
                elif 180 < j < 340:
                    self.board[m][n] = "Rook" + self.board[m][n][-1]
                elif 340 < j < 500:
                    self.board[m][n] = "Bishop" + self.board[m][n][-1]
                elif 500 < j < 660:
                    self.board[m][n] = "Knight" + self.board[m][n][-1]
                self.pawn_at_end = None
            return
        i -= 20
        j -= 20
        i //= 80
        j //= 80
        if 0 <= i < 8 and 0 <= j < 8:
            if (i, j) in self.choices:
                self.make_move(self.chosen, (i, j))
                self.turn = not self.turn
                self.chosen = None
                self.choices = []
            elif self.board[i][j] != "":
                if (self.turn and self.board[i][j][-1] == "W") or (
                    (not self.turn) and self.board[i][j][-1] == "B"
                ):
                    self.chosen = (i, j)
                    self.choices = self.get_possible_moves(i, j)
            else:
                self.chosen = None
                self.choices = []
        else:
            self.chosen = None
            self.choices = []
