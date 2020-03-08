import unittest

# local import
from src.generator.generator import Generator
from src.solver.solver import Solver


class Test_Generator(unittest.TestCase):

    """Generator class tests using unittest"""

    def __init__(self, *args, **kwargs):
        super(Test_Generator, self).__init__(*args, **kwargs)
        self.g = Generator()
        self.s = Solver()

    def test_01_generate(self):
        """Test Generator.generate function"""
        # generate new board
        b = self.g.generate()
        # check if unempty squares between 40%(32) and 60%(48) + random one
        counter = 0
        for r in b:
            for c in r:
                if c != 0:
                    counter += 1
        assert 32 <= counter <= 49
        # check if it solveable
        assert self.s.solve(b) == True
