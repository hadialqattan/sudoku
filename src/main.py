import pygame

# local import
from gui.gui import GUI


if __name__ == "__main__":
    # initialize all imported pygame modules
    pygame.init()
    # start pygame main loop
    gui = GUI()
    gui.loop()
    # uninitialize all pygame modules
    pygame.quit()
