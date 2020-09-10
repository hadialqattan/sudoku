import threading
import time


class Solver:

    """Sudoku game solver using backtracking algorithm

    :param board: Sudoku Board class instance (default None)
    :type board: Board
    :param delay: delay time 1/1000 secs (default 0.0)
    :type delay: float
    """

    def __init__(self, board=None, delay: float = 0.0):
        self.board = board
        self.__delay = delay / 1000
        self.__e = threading.Event()
        self.__kill = False
        self.__e.set()

    @property
    def delay(self) -> float:
        """delay property (getter)"""
        return self.__delay

    @delay.setter
    def delay(self, delay: float):
        """delay property (setter)

        :param delay: delay time 1/1000 secs
        :type delay: float
        """
        self.__delay = delay / 1000

    @property
    def e(self):
        """e property (getter)"""
        return self.__e.is_set()

    @e.setter
    def e(self, set: bool):
        """e property (setter)

        :param set: set of not
        :type set: bool
        """
        if set:
            self.__e.set()
        else:
            self.__e.clear()

    @property
    def kill(self):
        """stop solve function to join the thread"""
        return self.__kill

    @kill.setter
    def kill(self, kill: bool):
        """kill property (setter)

        :param kill: value
        :type kill: bool
        """
        self.__kill = kill

    def auto_solver(self) -> bool:
        """Solve Sudoku game board using backtracking algorithm (AutoSolver (board state change))

        :returns: True if the board solved else False for backtracking
        :rtype: bool
        """
        if not self.__kill:
            # get the next unused position from (LTR, TTB)
            pos = self.nextpos(self.board.board)
            # solved -edge
            if not pos:
                return True
            # itertate over all possible numbers(0-9)
            for n in range(1, 10):
                # check if the number valid in sudoku rules
                if not self.exists(self.board.board, n, pos):
                    # pause/resumption
                    self.__e.wait()
                    # change board state
                    self.board.set_sq_value(n, (pos[0], pos[1]))
                    self.board.board[pos[0]][pos[1]] = n
                    # sleep (solution case)
                    time.sleep(self.__delay)
                    # continue in the solution -edge
                    if self.auto_solver():
                        return True
                    if not self.__kill:
                        # pause/resumption
                        self.__e.wait()
                        # backtracking
                        # change board state
                        self.board.set_sq_value(0, (pos[0], pos[1]))
                        self.board.board[pos[0]][pos[1]] = 0
            # sleep (backtracking case)
            time.sleep(self.__delay)
            # invalid solution
            return False

    def solve(self, board: list) -> bool:
        """Solve Sudoku game board using backtracking algorithm

        :param board: Sudoku game board representation (two dimensional array)
        :type board: list
        :returns: True if the board solved else False for backtracking
        :rtype: bool
        """
        # get the next unused position from (LTR, TTB)
        pos = self.nextpos(board)
        # solved -edge
        if not pos:
            return True
        # itertate over all possible numbers(0-9)
        for n in range(1, 10):
            # check if the number valid in sudoku rules
            if not self.exists(board, n, pos):
                # set value as solution
                board[pos[0]][pos[1]] = n
                # continue in the solution -edge
                if self.solve(board):
                    return True
                # backtracking
                board[pos[0]][pos[1]] = 0
        # invalid solution
        return False

    def nextpos(self, board: list) -> tuple:
        """Get the next unused position from Left2Right & Top2Bottom

        :param board: Sudoku board represent as two dimensional array
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
                    return (r, c)
        # end of Sudoku board after (9, 9) position (solved) -edge
        return ()

    def exists(self, board: list, n: int, rc: tuple) -> tuple:
        """Sudoku game rules checker

        :param board: Sudoku board represent as two dimensional array
        :type board: list
        :param n: integer number as solution
        :type n: int
        :param rc: board position represented as (row, column)
        :type rc: tuple
        :returns: tuple of exists number position OR empty tuple if the number doesn't exists
        :rtype: tuple
        """
        # check row rule
        # iterate over all columns
        for c in range(len(board)):
            # check if the number exists in the same row
            if board[rc[0]][c] == n:
                return (rc[0], c)
        # check column rule
        # iterate over all rows
        for r in range(len(board)):
            # check if the number exists in the same column
            if board[r][rc[1]] == n:
                return (r, rc[1])
        # check 3*3 area rule
        #       row start pos | column start pos
        spos = ((rc[0] // 3) * 3, (rc[1] // 3) * 3)
        # (row) iterate over 3*3 area from spos[0] to spos[0] + 3
        for r in range(spos[0], spos[0] + 3):
            # (column) iterate over 3*3 area from spos[1] to spos[1] + 3
            for c in range(spos[1], spos[1] + 3):
                # check if the number exists in the same 3*3 area
                if board[r][c] == n:
                    return (r, c)
        # valid position
        return ()
