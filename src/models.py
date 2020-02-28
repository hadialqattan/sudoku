import pygame


class Board:

    """Screen Board

    :param size: sreen dimensions (pixels) (width, height, left gap)
    :type size: tuple
    :param board: Sudoku board represent as two dimensional array
    :type board: list
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, board: list, screen: pygame.Surface):
        self.board = board
        self.size = size
        self.screen = screen
        # create squares list
        self.squares = [
            [Square(self.board[c][r], (r, c), (self.size[0], self.size[2]), self.screen) for r in range(9)]
            for c in range(9)
        ]

    def set_value(self, value: int, pos: tuple):
        """change square value by position"""
        self.squares[pos[0]][pos[1]].value = value

    def draw(self):
        """Draw the board on the screen"""
        # Draw grid
        # set space between squares
        space = self.size[0] // 9
        # drow 10 lines HvV
        for r in range(10):
            # set line weight (bold at the end of 3*3 area)
            w = 3 if r % 3 == 0 and r != 0 else 1
            # draw horizontal line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen, (32, 194, 14), (self.size[2], r * space), (self.size[0] + self.size[2], r * space), w
            )
            # draw vertical line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen, (32, 194, 14), (r * space + self.size[2], 0), (r * space + self.size[2], self.size[1]), w
            )
        # Draw squares
        # iterate over all rows
        for r in range(9):
            # iterate over all columns
            for c in range(9):
                # draw square value
                self.squares[c][r].draw()


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
        self.value = value
        self.pos = pos
        self.widthpos = widthpos
        self.screen = screen

    def draw(self):
        """Draw square value"""
        # set space between squares
        space = self.widthpos[0] // 9
        # set actuall square position on the screen
        r, c = self.pos[0] * space + self.widthpos[1], self.pos[1] * space
        # choose the font and the size
        font = pygame.font.SysFont("rubik", 38)
        # check for none 0's squares
        if self.value != 0:
            # draw the value
            v = font.render(str(self.value), 1, (32, 194, 14))
            # set it on the screen
            self.screen.blit(
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
        self.size = size
        self.screen = screen

    def draw(self): 
        """Draw the left panel on the screen"""
        # Draw main frame
        # set frame lines width
        w = 3
        # draw rectangle
        pygame.draw.rect(self.screen, (32, 194, 14), ((0, 0), (self.size[0], self.size[1])), w)

