import pygame


class Board:

    """Screen Board

    :param board: Sudoku board represent as two dimensional array
    :type board: list
    :param size: sreen dimensions (pixels) (width, height, left gap)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, board: list, screen: pygame.Surface):
        self.__board = board
        self.__size = size
        self.__screen = screen
        # create squares list
        self.__squares = self.squares

    @property
    def board(self) -> list:
        """board property (getter)"""
        return self.__board

    @board.setter 
    def board(self, board: list): 
        """board property (setter)

        :param board: Sudoku board represent as two dimensional array
        :type board: list
        """
        if len(board) < 9 or len(board[0]) < 9: 
            raise ("only 9*9 board accepted.")
        self.__board = board
        self.__squares = self.squares

    @property
    def squares(self): 
        """squares property (getter)"""
        return [
            [
                Square(
                    self.__board[c][r], (r, c), (self.__size[0], self.__size[2]), self.__screen
                )
                for r in range(9)
            ]
            for c in range(9)
        ]

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
        # Draw grid
        # set space between squares
        space = self.__size[0] // 9
        # drow 10 lines HvV
        for r in range(10):
            # set line weight (bold at the end of 3*3 area)
            w = 3 if r % 3 == 0 and r != 0 else 1
            # draw horizontal line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.__screen,
                (32, 194, 14),
                (self.__size[2], r * space),
                (self.__size[0] + self.__size[2], r * space),
                w,
            )
            # draw vertical line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.__screen,
                (32, 194, 14),
                (r * space + self.__size[2], 0),
                (r * space + self.__size[2], self.__size[1]),
                w,
            )
        # Draw squares
        # iterate over all rows
        for r in range(9):
            # iterate over all columns
            for c in range(9):
                # draw square value
                self.__squares[c][r].draw()


class Square:

    """Board squeares

    :param value: square display number
    :type value: int
    :param pos: square position (row, column)
    :type pos: tuple
    :param width: screen width and left gap (width, gap)
    :type width: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, value: int, pos: tuple, widthpos: tuple, screen: pygame.Surface):
        self.__value = value
        self.__pos = pos
        self.__widthpos = widthpos
        self.__screen = screen
        self.__pencil = None

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
        self.__pencil = value

    def draw(self):
        """Draw square value"""
        # set space between squares
        space = self.__widthpos[0] // 9
        # set actuall square position on the screen
        r, c = self.__pos[0] * space + self.__widthpos[1], self.__pos[1] * space
        # choose the font and the size
        font = pygame.font.SysFont("rubik", 38)
        # check for none 0's squares
        if self.__value != 0:
            # create suface object
            v = font.render(str(self.__value), 1, (32, 194, 14))
            # draw in on the screen
            self.__screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2))),
                    int(c + ((space / 2) - (v.get_height() / 2))),
                ),
            )


class LeftPanel:

    """Left control panel 

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = size
        self.__screen = screen

    def draw(self):
        """Draw the left panel on the screen"""
        # Draw main frame
        # set frame lines width
        w = 3
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen, (32, 194, 14), ((0, 0), (self.__size[0], self.__size[1])), w
        )
        # print(Sudoku at the top)
        # choose the font and the size
        font = pygame.font.SysFont("rubik", 38)
        # create suface object
        v = font.render("Sudoku", 1, (32, 194, 14))
        # draw it on the screen
        self.__screen.blit(v, (self.__size[0]//4, 10))
