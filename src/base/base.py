import pygame


class GUIBase:

    """Base GUI class

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = size
        self.__screen = screen

    @property
    def size(self):
        """size property (getter)"""
        return self.__size

    @property
    def screen(self):
        """screen property (getter)"""
        return self.__screen

    def draw(self):
        """Draw function"""
        pass

    def _type(self, txt: str, rgb: tuple, pos: tuple, fsize: int):
        """Draw string on the surface screen

        :param txt: text to draw
        :type txt: str
        :param rgb: text color
        :type rgb: tuple
        :param pos: postition to draw
        :type pos: tuple
        :param fsize: font size
        :type fsize: int
        """
        # create font object
        font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", fsize)
        # render font object with text
        v = font.render(txt, 1, rgb)
        # draw font obj on the surface
        self.__screen.blit(v, pos)
