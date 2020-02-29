import threading
import time


class Solver:

    """Sudoku game solver using backtracking algorithm

    :param board: Sudoku Board class instance
    :type board: Board
    :param sleep: delay time 1/1000 secs
    :type sleep: float
    """

    def __init__(self, board, sleep: float):
        self.__board = board
        self.__sleep = sleep / 1000
        self.__e = threading.Event()
        self.__kill = True
        self.__e.set()

    @property
    def board(self):
        """board property (getter)"""
        return self.__board

    @property
    def sleep(self) -> float:
        """sleep property (getter)"""
        return self.__sleep

    @sleep.setter
    def sleep(self, sleep: float):
        """sleep property (setter)
        
        :param sleep: delay time 1/1000 secs
        :type sleep: float
        """
        sleep = 1000 if sleep > 1000 else sleep
        sleep = 0 if sleep < 0 else sleep
        self.__sleep = sleep / 1000

    @property
    def e(self):
        """change threading.event state"""
        if not self.__e.is_set():
            self.__e.set()
        else:
            self.__e.clear()

    @property
    def kill(self):
        """stop solve function to join the thread"""
        self.__kill = not self.__kill
        if not self.__e.is_set():
            self.__e.set()

    def solve(self, change_state: bool = True) -> bool:
        """Solve Sudoku game board using backtracking algorithm

        :param board: Sudoku game board representation (two dimensional array)
        :type board: list
        :param change_state: change board state (default = True)
        :type change_state: bool
        :returns: True if the board solved else False for backtracking
        :rtype: bool
        """
        if not self.__kill:
            # get the next unused position from (LTR, TTB)
            pos = self.nextpos(self.__board.board)
            # solved -edge
            if not pos:
                return True
            # itertate over all possible numbers(0-9)
            for n in range(1, 10):
                # check if the number valid in sudoku rules
                if not self.exists(self.__board.board, n, pos):
                    # set the number as solution
                    if change_state:
                        # pause/resumption
                        self.__e.wait()
                        # change board state
                        self.__board.set_sq_value(n, (pos[0], pos[1]))
                    self.__board.board[pos[0]][pos[1]] = n
                    # sleep (solution case)
                    time.sleep(self.__sleep)
                    # continue in the solution -edge
                    if self.solve():
                        return True
                    if not self.__kill:
                        # backtracking
                        if change_state:
                            # pause/resumption
                            self.__e.wait()
                            # change board state
                            self.__board.set_sq_value(0, (pos[0], pos[1]))
                        self.__board.board[pos[0]][pos[1]] = 0
            # sleep (backtracking case)
            time.sleep(self.__sleep)
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
