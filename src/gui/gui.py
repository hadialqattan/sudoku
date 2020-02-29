import pygame, time

# local import
try:
    from models.board import Board
    from models.left_panel import LeftPanel
    from solver.solver import Solver
    from solver.parallel import Threads
except ImportError:
    from src.models.board import Board
    from src.models.left_panel import LeftPanel
    from src.solver.solver import Solver
    from src.solver.parallel import Threads


class GUI:

    """GUI interface for Sudoku solver

    :param board: Board class instance represent our Sudoku board
    :type board: Board
    :param screen_size: display width
    :type screen_size: tuple
    """

    def __init__(self, board: list, screen_size: tuple):
        # set main pygame screen size
        self.__screen_size = (screen_size[0], screen_size[1])
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        self.__board = board
        # create gui objects from board.py
        self.__board_model = Board(self.__screen_size, self.__board, self.__screen)
        self.__left_panel = LeftPanel(self.__screen_size, self.__screen)
        # create threads managment object
        self.__threads = Threads()
        # create solver object
        self.__solver = Solver(self.__board_model, 50)
        # set screen title
        pygame.display.set_caption("Sudoku")

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
        jump_mode = False
        # run Pygame main loop
        while True:
            # listen to events
            for e in pygame.event.get():
                # close window button event
                if e.type == pygame.QUIT:
                    return
                # select square by mouse event
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.select_by_mouse()
                # set value and delete events
                elif e.type == pygame.KEYDOWN:
                    # block all playing event when player lost/won
                    if (
                        not self.__left_panel.wrongs.lost
                        and not self.__left_panel.wrongs.won
                    ):
                        # set and delete square value by keys
                        self.set_del_value_by_key(e)
                        # change selected square by arrows
                        self.select_by_arrows(e, self.__board_model.selected, jump_mode)

                    if e.key == pygame.K_q:
                        return
                    elif e.key == pygame.K_j:
                        jump_mode = not jump_mode
                    elif e.key == pygame.K_s:
                        self.__solver.kill
                        self.__threads.start(self.__solver.solve)
                    elif e.key == pygame.K_e:
                        self.__solver.kill
                        self.__threads.stop()
                    elif e.key == pygame.K_r:
                        self.__solver.e

            # update the screen
            self.refresh()

    def select_by_mouse(self):
        """Select board square by MOUSEBUTTONDOWN event"""
        # get mouse click position
        p = pygame.mouse.get_pos()
        # calculate square (row, column) from mouse position
        left_space = self.__screen_size[0] - self.__screen_size[1]
        if p[0] > left_space:
            self.__board_model.selected = (
                p[1] // (self.__screen_size[1] // 9),
                (p[0] - left_space) // (self.__screen_size[1] // 9),
            )
        else:
            # select none if mouse out of board
            self.__board_model.selected = None

    def set_del_value_by_key(self, e: pygame.event.Event):
        """Set and delete square value by pygame.KEYDOWN event

        :param e: pygame event
        :type e: pygame.event.Event
        """
        v = 0
        # delete / backspace key
        if e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
            self.__board_model.clear
        # return / enter key
        elif e.key == pygame.K_RETURN:
            issuccess = self.__board_model.set_value()
            if issuccess:
                # check if player solve the board
                if self.__board_model.isfinished:
                    self.__left_panel.wrongs.won = True
            elif type(issuccess) == bool:
                # increase wrongs counter
                self.__left_panel.wrongs.wrongs_counter
        # pencil 1-9
        elif e.key == pygame.K_1:
            v = 1
        elif e.key == pygame.K_2:
            v = 2
        elif e.key == pygame.K_3:
            v = 3
        elif e.key == pygame.K_4:
            v = 4
        elif e.key == pygame.K_5:
            v = 5
        elif e.key == pygame.K_6:
            v = 6
        elif e.key == pygame.K_7:
            v = 7
        elif e.key == pygame.K_8:
            v = 8
        elif e.key == pygame.K_9:
            v = 9
        if 0 < v < 10:
            self.__board_model.set_pencil(v)

    def select_by_arrows(self, e: pygame.event.Event, pos: tuple, jump_mode: bool):
        """changed selected square by arrows

        :param e: pygame event
        :type e: pygame.event.Event
        :param pos: current position
        :type pos: tuple
        :param jump_mode: if true the selection will move to the next empty position
        :type jump_mode: bool
        """
        # set row, column change value
        r, c = 0, 0
        if e.key == pygame.K_UP or e.key == pygame.K_w:
            r = -1
        elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
            r = 1
        elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
            c = 1
        elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
            c = -1
        # check if there's selected square
        if pos:
            if jump_mode:
                # find next empty position in the same direction
                while -1 < pos[0] + r < 9 and -1 < pos[1] + c < 9 and r + c != 0:
                    pos = (pos[0] + r, pos[1] + c)
                    if self.__board_model.board[pos[0]][pos[1]] == 0:
                        break
                # move only if the next position is empty -(handle pre edge case)
                if self.__board_model.board[pos[0]][pos[1]] == 0:
                    self.__board_model.selected = pos
            else:
                # move to the next position
                pos = (pos[0] + r, pos[1] + c)
                if -1 < pos[0] < 9 and -1 < pos[1] < 9:
                    self.__board_model.selected = pos
