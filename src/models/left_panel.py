import pygame


class LeftPanel:

    """Left control panel 

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = (size[0] - size[1], size[1])
        self.__screen = screen
        self.wrongs = Wrongs(self.__size, self.__screen)

    def draw(self):
        """Draw the left panel on the screen"""
        # Draw main frame
        # set frame lines width
        w = 3
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen, (72, 234, 54), ((0, 0), (self.__size[0], self.__size[1])), w
        )
        # print(Sudoku at the top)
        pygame.draw.rect(
            self.__screen,
            (72, 234, 54),
            ((0, 0), (self.__size[0], self.__size[1] // 9)),
            w // 3,
        )
        # create font object
        font = pygame.font.SysFont("rubik", 42)
        # create surface object
        v = font.render("Sudoku", 1, (72, 234, 54))
        # draw it on the screen
        self.__screen.blit(v, (self.__size[0] // 4, 14))
        # draw wrongs panel at the bottom
        self.__wrongs.draw()


class Wrongs:

    """Lose system class
    
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = (size[0], size[1] // 9)
        self.__screen = screen
        self.__wrongs_counter = 0
        self.__lost = False
        self.__won = False

    @property
    def wrongs_counter(self):
        """increase wrongs counter"""
        # increase wrongs counter (max=5)
        if self.__wrongs_counter < 5:
            self.__wrongs_counter += 1
        else:
            # set lost flag
            self.__lost = True

    @property
    def lost(self):
        """lost property (getter)"""
        return self.__lost

    @property
    def won(self) -> bool:
        """won property (getter)"""
        return self.__won

    @won.setter
    def won(self, value: bool):
        """won property (setter)

        :param value: won value
        :type value: bool
        """
        self.__won = value

    def draw(self):
        """Draw Wrongs square"""
        # Draw main frame
        # set frame lines width
        w = 1
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen,
            (72, 234, 54),
            ((0, self.__size[1] * 8), (self.__size[0], self.__size[1])),
            w,
        )
        # draw wrongs
        # check if the player lost or won
        if self.__won:
            self.__type(
                "You Won",
                (72, 234, 54),
                (self.__size[0] // 4 - 10, self.__size[1] * 8 + 15),
            )
        elif not self.__lost:
            self.__type(
                "X  " * self.__wrongs_counter,
                (234, 72, 54),
                (40, self.__size[1] * 8 + 15),
            )
        else:
            self.__type(
                "You Lost",
                (234, 72, 54),
                (self.__size[0] // 4 - 15, self.__size[1] * 8 + 15),
            )

    def __type(self, txt: str, rgb: tuple, pos: tuple):
        """Draw string on the surface screen

        :param txt: text to draw
        :type txt: str
        :param rgb: text color
        :type rgb: tuple
        :param pos: postition to draw
        :type pos: tuple
        """
        # create font object
        font = pygame.font.SysFont("rubik", 38)
        # render font object with text
        v = font.render(txt, 1, rgb)
        # draw font obj on the surface
        self.__screen.blit(v, pos)
