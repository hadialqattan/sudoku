import pygame

# local import
from base.base import GUIBase
from solver.solver import Solver


class Board(GUIBase):

    """Screen Board

    :param board: Sudoku board represent as two dimensional array
    :type board: list
    :param size: screen dimensions (pixels) (width, height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, board: list, screen: pygame.Surface):
        super().__init__((size[1], size[1], size[0] - size[1]), screen)
        self.__board = board
        self.__solver = Solver(self)
        # create squares list
        self.__squares = [
            [
                Square(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]
        self.__selected = None
        self.__wrong = None

    @property
    def wrong(self):
        """wrong property (getter)"""
        return self.__wrong

    @property
    def squares(self) -> list:
        """squares property (getter)"""
        return self.__squares

    def update_squares(self):
        """squares property (updatter)"""
        # iterate over all squares
        for r in range(9):
            for c in range(9):
                # update values
                self.__squares[r][c].value = self.__board[r][c]
                self.__squares[r][c].pencil = 0

    @property
    def board(self) -> list:
        """board property (getter)"""
        return self.__board

    @board.setter
    def board(self, board: list):
        """board property (setter) & update squares

        :param board: Sudoku board represent as two dimensional array
        :type board: list
        """
        # set new board
        self.__board = board
        # reinit squares
        self.__squares = [
            [
                Square(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]

    @property
    def selected(self) -> tuple:
        """selected property (getter)"""
        return self.__selected

    @selected.setter
    def selected(self, pos: tuple):
        """selected property (setter) & refresh squares

        :param pos: selected square position (row, column)
        :type pos: tuple
        """
        if not self.__wrong:
            # clear previous selection
            if self.__selected != None:
                self.__squares[self.__selected[0]][self.__selected[1]].selected = False
            if pos:
                # select new square
                self.__selected = pos
                self.__squares[self.__selected[0]][self.__selected[1]].selected = True
            else:
                # set selected to None if pos out of board
                self.__selected = None

    @property
    def get_pencil(self) -> int:
        """selected square pencil (getter)"""
        # get selected square
        r, c = self.__selected
        return self.__squares[r][c].pencil

    def set_pencil(self, value: int):
        """set pencil value

        :param value: pencil value
        :type value: int
        """
        # get selected square
        r, c = self.__selected
        if self.__squares[r][c].value == 0:
            self.__squares[r][c].pencil = value

    @property
    def get_value(self) -> int:
        """selected square value (getter)"""
        # get selected square
        r, c = self.__selected
        return self.__squares[r][c].value

    def set_value(self) -> str:
        """set square value

        :returns: board state ('s' -> success, 'w' -> wrong, 'c' -> unsolvable board)
        :rtype: str
        """
        # get selected square
        r, c = self.__selected
        if self.get_value == 0:
            # chock for non-0 pencil value
            pencil = self.get_pencil
            if pencil != 0:
                # check the number match Sudoku rules
                w = self.__solver.exists(self.__board, pencil, (r, c))
                if w:
                    # change squares state to wrong (red color)
                    self.__squares[r][c].wrong = True
                    self.__squares[w[0]][w[1]].wrong = True
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    self.__wrong = w
                    return "w"
                else:
                    # change set square value and return true
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    # copy board
                    # init copy as two dimensional array with 9 rows
                    copy = [[] for r in range(9)]
                    # iterate over all rows
                    for r in range(9):
                        # iterate over all columns
                        for c in range(9):
                            # append the num
                            copy[r].append(self.__board[r][c])
                    # check if the board unsolvable
                    if not self.__solver.solve(copy):
                        return "c"
                    return "s"

    @property
    def clear(self):
        """clear selected square value"""
        # get selected square
        r, c = self.__selected
        # clear square value and pencil
        self.__squares[r][c].value = 0
        self.__squares[r][c].pencil = 0
        self.__board[r][c] = 0
        # change wrong state
        if self.__wrong:
            self.__squares[r][c].wrong = False
            self.__squares[self.__wrong[0]][self.__wrong[1]].wrong = False
            self.__wrong = None

    @property
    def isfinished(self):
        """return true if there's no more empty squares else false

        :returns: true if there's no more empty squares else false
        :rtype: bool
        """
        return not self.__solver.nextpos(self.board)

    def set_sq_value(self, value: int, pos: tuple):
        """change square value by position

        :param value: new square value
        :type value: int
        :param pos: square position
        :type pos: tuple
        """
        self.__squares[pos[0]][pos[1]].value = value

    def draw(self):
        """Draw the board on the screen"""
        # Draw squares
        # iterate over all rows
        for r in range(9):
            # iterate over all columns
            for c in range(9):
                # draw square value
                self.__squares[c][r].draw()
        # Draw grid
        # set space between squares
        space = self.size[0] // 9
        # drow 10 lines HvV
        for r in range(10):
            # set line weight (bold at the end of 3*3 area)
            w = 4 if r % 3 == 0 and r != 0 else 1
            # draw horizontal line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (72, 234, 54),
                (self.size[2], r * space),
                (self.size[0] + self.size[2], r * space),
                w,
            )
            # draw vertical line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (72, 234, 54),
                (r * space + self.size[2], 0),
                (r * space + self.size[2], self.size[1]),
                w,
            )


class Square(GUIBase):

    """Board squeares

    :param value: square display number
    :type value: int
    :param pos: square position (row, column)
    :type pos: tuple
    :param width: screen width and left gap (width, gap)
    :type width: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    :param changeable: changeabllity
    :type changeable: bool
    """

    def __init__(
        self,
        value: int,
        pos: tuple,
        widthpos: tuple,
        screen: pygame.Surface,
        changeable: bool,
    ):
        super().__init__(0, screen)
        self.__value = value
        self.__pos = pos
        self.__widthpos = widthpos
        self.__pencil = 0
        self.__selected = False
        self.__changeable = changeable
        self.__wrong = False

    @property
    def changeable(self):
        """changeable property (getter)"""
        return self.__changeable

    @property
    def selected(self) -> tuple:
        """selected property (getter)"""
        return self.__selected

    @selected.setter
    def selected(self, v: bool):
        """selected property (setter)

        :param v: selected value
        :type v: bool
        """
        self.__selected = v

    @property
    def value(self) -> int:
        """value property (getter)"""
        return self.__value

    @value.setter
    def value(self, value: int):
        """value property (setter)

        :param value: square value
        :type value: int
        """
        if self.__changeable:
            self.__value = value

    @property
    def pencil(self) -> int:
        """pencil property (getter)"""
        return self.__pencil

    @pencil.setter
    def pencil(self, value: int):
        """pencil property (setter)

        :param value: pencil square value
        :type value: int
        """
        if self.__changeable:
            self.__pencil = value

    @property
    def wrong(self):
        """wrong property (getter)"""
        return self.__wrong

    @wrong.setter
    def wrong(self, w: bool):
        """wrong property (setter)

        :param w: wrong value
        :type w: bool
        """
        self.__wrong = w

    def draw(self):
        """Draw square value"""
        # set space between squares
        space = self.__widthpos[0] // 9
        # set actuall square position on the screen
        r, c = self.__pos[0] * space + self.__widthpos[1], self.__pos[1] * space
        # fill unchangeable square background
        if not self.__changeable:
            sqsize = self.__widthpos[0] // 9
            # draw rectangle (frame)
            pygame.draw.rect(self.screen, (10, 30, 0), ((r, c), (sqsize, sqsize)))
        # check for none 0's squares
        if self.__value != 0:
            font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", 38)
            # set color
            rgb = (72, 234, 54) if not self.__wrong else (234, 72, 54)
            # create suface object
            v = font.render(str(self.__value), 1, rgb)
            # draw in on the screen
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2))),
                    int(c + ((space / 2) - (v.get_height() / 2))),
                ),
            )
        elif self.__pencil != 0:
            font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", 30)
            # create suface object
            v = font.render(str(self.__pencil), 1, (2, 164, 0))
            # draw in on the screen
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2)) - 20),
                    int(c + ((space / 2) - (v.get_height() / 2)) - 15),
                ),
            )
        # draw bold outline around selected square
        if self.__selected:
            # draw rectangle (frame)
            pygame.draw.rect(self.screen, (52, 214, 34), ((r, c), (space, space)), 3)
