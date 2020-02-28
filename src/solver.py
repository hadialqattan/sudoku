import time

# local import
try: 
    from .models import Board
except ImportError: 
    from models import Board


class Solver: 

    """Sudoku game solver using backtracking algorithm

    :param board: Sudoku Board class instance
    :type board: Board
    :param speed: 1 / 1000 for 1 sec
    :type speed: int
    """

    def __init__ (self, board: Board, speed: int): 
        self.board = board
        self.sleep = speed / 1000
        self.run = True

    def solve(self) -> bool:
        """Solve Sudoku game board using backtracking algorithm

        :param board: Sudoku game board representation (two dimensional array)
        :type board: list
        :returns: True if the board solved else False for backtracking
        :rtype: bool
        """
        if self.run: 
            # get the next unused position from (LTR, TTB) 
            pos = self.nextpos(self.board.board)
            # solved -edge
            if not pos: 
                return True
            # itertate over all possible numbers(0-9)
            for n in range(1, 10): 
                # check if the number valid in sudoku rules
                if self.isvalid(self.board.board, n, pos):
                    # set the number as solution
                    self.board.set_value(n, (pos[0], pos[1]))
                    self.board.board[pos[0]][pos[1]] = n
                    time.sleep(self.sleep)
                    # continue in the solution -edge
                    if self.solve():
                        return True
                    # backtracking
                    if self.run:
                        self.board.set_value(0, (pos[0], pos[1]))
                        self.board.board[pos[0]][pos[1]] = 0
            time.sleep(self.sleep)
            # invalid solution
            return False


    def nextpos(self, board: list) -> tuple:
        """Get the next unused position from Left2Right & Top2Bottom

        :param board: Sudoku game board representation (two dimensional array)
        :type board: list
        :returns: next unused position or empty if there's no next
        :rtype: tuple 
        """
        # iterate over each row
        for r in range(9):
            # iterate over each column
            for c in range(9):
                # check for unused position
                if board[r][c] == 0:
                    return(r, c)
        # end of Sudoku board after (9, 9) position (solved) -edge
        return ()


    def isvalid(self, board: list, n: int, rc: tuple) -> bool:
        """Sudoku game rules checker 

        :param board: Sudoku game board representation (two dimensional array)
        :type board: list
        :param n: integer number as solution
        :type n: int 
        :param rc: board position represented as (row, column)
        :type rc: tuple
        :returns: True if the number represent a valid solution else False
        :rtype: bool
        """
        # check row rule
        # iterate over all columns
        for c in range(len(board)): 
            # check if the number exists in the same row
            if board[rc[0]][c] == n: 
                return False
        # check column rule
        # iterate over all rows
        for r in range(len(board)): 
            # check if the number exists in the same column
            if board[r][rc[1]] == n:
                return False
        # check 3*3 area rule
        #       row start pos | column start pos
        spos = ((rc[0] // 3)*3, (rc[1] // 3)*3)
        # (row) iterate over 3*3 area from spos[0] to spos[0] + 3
        for r in range(spos[0], spos[0] + 3): 
            # (column) iterate over 3*3 area from spos[1] to spos[1] + 3
            for c in range(spos[1], spos[1] + 3):
                # check if the number exists in the same 3*3 area
                if board[r][c] == n:
                    return False
        # valid position
        return True
