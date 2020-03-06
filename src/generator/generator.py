from random import randint

# local import
from solver.solver import Solver


class Generator: 

    """Random valid Sudoku board generator"""

    def __init__(self):
        self.__board = [[0 for r in range(9)] for c in range(9)]
        self.__solver = Solver(self.__board, 0)

    def generate(self) -> list: 
        """Generate valid random Sudoku board

        :returns: valid Sudoku board
        :rtype: list
        """
        # fill random position with random value
        board = [[0 for r in range(9)] for c in range(9)]
        board[randint(0, 8)][randint(0, 8)] = randint(1, 9)
        # 40%(32) to 60%(48) unempty squares (random value)
        unempty = randint(32, 48)
        # random postions list
        ranpos = []
        # get random positions
        counter = 0
        while counter <= unempty:
            # get random row and random column
            r, c = randint(0, 8), randint(0, 8)
            # check for repeated values
            if (r, c) not in ranpos:
                ranpos.append((r, c))
                counter += 1
        # sovle the board 
        self.__solver.solve(board)
        # apply solution in ranpos squares
        for r in range(9): 
            for c in range(9): 
                if (r, c) in ranpos: 
                    self.__board[r][c] = board[r][c]
                else: 
                    self.__board[r][c] = 0
        return self.__board
