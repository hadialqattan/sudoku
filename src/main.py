import pygame

# local import
try: 
    from gui.gui import GUI
except ImportError:
    from src.gui.gui import GUI


if __name__ == "__main__":
    # initialize all imported pygame modules
    pygame.init()
    # start pygame main loop
    gui = GUI(
        [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7],
        ], 
        (1000, 720)
    )
    """gui = GUI(
        [
            [9, 5, 6, 7, 2, 4, 1, 8, 3],
            [3, 7, 1, 8, 9, 6, 4, 2, 5],
            [2, 8, 4, 5, 1, 3, 7, 9, 6],
            [4, 2, 8, 3, 6, 9, 5, 1, 7],
            [5, 1, 3, 2, 8, 7, 9, 6, 4],
            [7, 6, 9, 4, 5, 1, 8, 3, 2],
            [1, 9, 7, 6, 4, 2, 3, 5, 8],
            [6, 3, 5, 1, 7, 8, 2, 4, 9],
            [8, 4, 2, 9, 3, 5, 6, 7, 0],
        ], 
        (1000, 720)
    )"""
    gui.loop()
    # uninitialize all pygame modules
    pygame.quit()
