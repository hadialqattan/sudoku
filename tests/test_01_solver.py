import unittest

# local import
from .IO import INPUT_SOLVER, OUTPUT_SOLVER
from src.solver.solver import Solver


class Test_Solver(unittest.TestCase):

    """Solver class tests using unittest"""

    def __init__(self, *args, **kwargs):
        super(Test_Solver, self).__init__(*args, **kwargs)
        self.inputs = INPUT_SOLVER()
        self.outputs = OUTPUT_SOLVER()
        self.s = Solver()

    def test_01_nextpos(self):
        """Test Solver.nextpos function"""
        pos = self.s.nextpos(self.inputs["nextpos"]["board"])
        assert pos == self.outputs["nextpos"]

    def test_02_exists_success(self):
        """Test Solver.exists success case"""
        r = self.s.exists(
            self.inputs["exists"]["board"],
            self.inputs["exists"]["success"]["n"],
            self.inputs["exists"]["success"]["rc"],
        )
        assert r == self.outputs["exists"]["success"]

    def test_03_exists_false_row(self):
        """Test Solver.exists false row"""
        r = self.s.exists(
            self.inputs["exists"]["board"],
            self.inputs["exists"]["row0"]["n"],
            self.inputs["exists"]["row0"]["rc"],
        )
        assert r == self.outputs["exists"]["row0"]

    def test_04_exists_false_column(self):
        """Test Solver.exists false column"""
        r = self.s.exists(
            self.inputs["exists"]["board"],
            self.inputs["exists"]["column0"]["n"],
            self.inputs["exists"]["column0"]["rc"],
        )
        assert r == self.outputs["exists"]["column0"]

    def test_05_exists_false_33area(self):
        """Test Solver.exists false 3*3area"""
        r = self.s.exists(
            self.inputs["exists"]["board"],
            self.inputs["exists"]["3*3area0"]["n"],
            self.inputs["exists"]["3*3area0"]["rc"],
        )
        assert r == self.outputs["exists"]["3*3area0"]

    def test_06_solve(self):
        """Test Solver.solve function"""
        self.s.solve(self.inputs["solve"])
        assert self.inputs["solve"] == self.outputs["solve"]
