import pygame, time

# local import
try:
    from .models import Board, LeftPanel
    from .solver import Solver
    from .parallel import Threads
except ImportError:
    from models import Board, LeftPanel
    from solver import Solver
    from parallel import Threads


class GUI:

    """GUI interface for Sudoku solver

    :param board: Board class instance represent our Sudoku board
    :type board: Board
    """

    def __init__(self, board: list):
        # set main pygame screen size
        self.__screen = pygame.display.set_mode((1000, 720))
        self.__board = board
        # create gui objects from models.py
        self.__board_model = Board((720, 720, 280), self.__board, self.__screen)
        self.__left_panel = LeftPanel((280, 720), self.__screen)
        # create threads managment object
        self.__threads = Threads()
        # create solver object
        self.__solver = Solver(self.__board_model, 500)
        # set screen title
        pygame.display.set_caption("Sudoku solver")

    def refresh(self):
        """Redraw the screen and update it"""
        # set background color to black
        self.__screen.fill((0, 0, 0))
        # redraw the board
        self.__board_model.draw()
        # redraw the left panel
        self.__left_panel.draw()
        # update the screen
        pygame.display.update()

    def loop(self):
        """Pygame main loop"""
        # run Pygame main loop
        while True:
            # listen to events
            for e in pygame.event.get():
                # close window button event
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        return
                    if e.key == pygame.K_s:
                        self.__solver.kill
                        self.__threads.start(self.__solver.solve)
                    if e.key == pygame.K_e:
                        self.__solver.kill
                        self.__threads.stop()
                    if e.key == pygame.K_r:
                        self.__solver.e
            # update the screen
            self.refresh()
