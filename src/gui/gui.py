import pygame, time

# local import
from models.board import Board
from models.left_panel import LeftPanel
from solver.solver import Solver
from generator.generator import Generator


class GUI:

    """GUI interface for Sudoku solver

    :param screen_size: display width
    :type screen_size: tuple
    """

    def __init__(self):
        # set main pygame screen size
        self.__screen_size = (1000, 720)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        # change display icon
        pygame.display.set_icon(pygame.image.load("../assets/icon.png"))
        self.__generator = Generator()
        self.__board = self.__generator.generate()
        # create board object
        self.__board_model = Board(self.__screen_size, self.__board, self.__screen)
        # create solver object
        self.__solver = Solver(self.__board_model, 500)
        # create left panel object
        self.__left_panel = LeftPanel(self.__solver, self.__screen_size, self.__screen)
        # set screen title
        pygame.display.set_caption("Sudoku")

    def __refresh(self):
        """Redraw the screen and update it"""
        # set background color to black
        self.__screen.fill((0, 0, 0))
        # redraw the board
        self.__board_model.draw()
        # redraw the left panel
        self.__left_panel.draw()
        # update the screen
        pygame.display.update()
        # reset buttons style
        # reset auto solver buttons
        for b in self.__left_panel.auto_solver.buttons:
            b.reset
        # reset options buttons
        for b in self.__left_panel.options.buttons:
            b.reset

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
                    self.__select_by_mouse()
                    self.__auto_solver_buttons_mouse()
                    self.__options_buttons_mouse()
                # set value and delete events
                elif e.type == pygame.KEYDOWN:
                    # block all playing event when player lost/won
                    if (
                        not self.__left_panel.gamesystem.lost
                        and not self.__left_panel.gamesystem.won
                    ):
                        # set and delete square value by keys
                        self.__set_del_value_by_key(e)
                        # change selected square by arrows
                        self.__select_by_arrows(
                            e, self.__board_model.selected, jump_mode
                        )
                    # quite shortcut
                    if e.key == pygame.K_q:
                        return
                    # jump mode shortcut
                    elif e.key == pygame.K_j:
                        jump_mode = not jump_mode
            # update the screen
            self.__refresh()

    def __select_by_mouse(self):
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

    def __auto_solver_buttons_mouse(self):
        """Button events"""
        # get mouse click position
        p = pygame.mouse.get_pos()
        # iterate over all auto solver buttons
        for b in self.__left_panel.auto_solver.buttons:
            # check if the position match b click range
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                # call click event
                b.click()

    def __options_buttons_mouse(self):
        """Button events"""
        # get mouse click position
        p = pygame.mouse.get_pos()
        s = True
        # iterate over all options buttons
        for b in self.__left_panel.options.buttons:
            # check if the position match b click range
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                # call click event
                if b.innertxt == "selected":
                    # copy board
                    # init copy as two dimensional array with 9 rows
                    copy = [[] for r in range(9)]
                    # iterate over all rows
                    for r in range(9):
                        # iterate over all columns
                        for c in range(9):
                            # append the num
                            copy[r].append(self.__board_model.board[r][c])
                    s = b.click((copy, self.__board_model.selected))
                elif b.innertxt == "generate":
                    # reset won/lost/wrongs_counter
                    self.__left_panel.gamesystem.reset()
                    # reset time
                    self.__left_panel.time.init_time = time.time()
                    # reset hint
                    self.__left_panel.hints.hint = "everything is well"
                    s = b.click((self.__board_model,))
                elif b.innertxt == "reset":
                    # reset won/lost/wrongs_counter
                    self.__left_panel.gamesystem.reset()
                    # reset time
                    self.__left_panel.time.init_time = time.time()
                    # reset hint
                    self.__left_panel.hints.hint = "everything is well"
                    s = b.click()
                else:
                    s = b.click()
        # check for unsolvable case
        if not s:
            self.__left_panel.hints.hint = "unsolvable board"

    def __set_del_value_by_key(self, e: pygame.event.Event):
        """Set and delete square value by pygame.KEYDOWN event

        :param e: pygame event
        :type e: pygame.event.Event
        """
        v = 0
        # delete / backspace key
        if e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
            # clear selected item
            self.__board_model.clear
            # reset hints
            self.__left_panel.hints.hint = "everything is well"
        # return / enter key
        elif e.key == pygame.K_RETURN:
            issuccess = self.__board_model.set_value()
            if issuccess == "s":
                # check if player solve the board
                if self.__board_model.isfinished:
                    self.__left_panel.gamesystem.won = True
            elif issuccess == "w":
                # increase wrongs counter
                self.__left_panel.gamesystem.wrongs_counter
                # set clear hint
                self.__left_panel.hints.hint = "press backspace"
            elif issuccess == "c":
                # set clear hint
                self.__left_panel.hints.hint = "unsolvable board"
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

    def __select_by_arrows(self, e: pygame.event.Event, pos: tuple, jump_mode: bool):
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
