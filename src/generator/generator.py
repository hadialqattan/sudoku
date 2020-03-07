from random import randint

# local import
try:
    from solver.solver import Solver
except ImportError:
    # for tests purposes
    from src.solver.solver import Solver


class Generator:

    """Random valid Sudoku board generator"""

    def __init__(self):
        self.__solver = Solver()

    def generate(self) -> list:
        """Generate valid random Sudoku board

        :returns: valid Sudoku board
        :rtype: list
        """
        # fill random position with random value
        b = [[0 for r in range(9)] for c in range(9)]
        b[randint(0, 8)][randint(0, 8)] = randint(1, 9)
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
        self.__solver.solve(b)
        # apply solution in random positions
        b2 = [[] for i in range(9)]
        # iterate overall rows
        for r in range(9):
            # iterate overall columns
            for c in range(9):
                # check if (r, c) position in random positions list
                if (r, c) in ranpos:
                    b2[r].append(b[r][c])
                else:
                    b2[r].append(0)
        return b2
