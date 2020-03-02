import pygame, time

# local import
from solver.parallel import Threads


class LeftPanel:

    """Left control panel 

    :param solver: solver object
    :type solver: Solver
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        self.__size = (size[0] - size[1], size[1])
        self.__screen = screen
        self.wrongs = Wrongs(self.__size, self.__screen)
        self.time = Time(self.__size, self.__screen)
        self.hints = Hints(self.__size, self.__screen)
        self.auto_solver = AutoSolver(solver, self.__size, self.__screen)

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
        # draw hint panel
        self.hints.draw()
        # draw auto solver control panel
        self.auto_solver.draw()
        # draw time panel at the bottom (above wrongs panel)
        self.time.draw()
        # draw wrongs panel at the bottom
        self.wrongs.draw()


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
    def lost(self) -> bool:
        """lost property (getter)"""
        return self.__lost

    @lost.setter
    def lost(self, value: bool):
        """lost property (setter) 

        :param value: lost value
        :type value: bool
        """
        self.__lost = value

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
        """Draw Wrongs rect"""
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


class Time:

    """Time managment class
    
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = (size[0], size[1] // 9)
        self.__screen = screen
        self.__init_time = time.time()

    def __time_formatter(self, delta: float) -> str:
        """convert float secounds to HH:MM:SS str format

        :param delta: deffirent between init time and current time 
        :type delta: float
        :returns: HH:MM:SS time format
        "rtype: str
        """
        # calculate HHMMSS from franctional secs
        hms = [delta // 60 // 60, delta // 60, delta % 60]
        # convert in to str with required left zero if the number < 10
        for i in range(len(hms)):
            hms[i] = f"0{int(hms[i])}" if hms[i] < 10 else f"{int(hms[i])}"
        return f"{hms[0]}:{hms[1]}:{hms[2]}"

    def draw(self):
        """Draw Time rect"""
        # Draw main frame
        # set frame lines width
        w = 1
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen,
            (72, 234, 54),
            ((0, self.__size[1] * 7), (self.__size[0], self.__size[1])),
            w,
        )
        # create font object
        font = pygame.font.SysFont("rubik", 32)
        # render font object with formatted time
        ftime = self.__time_formatter(time.time() - self.__init_time)
        v = font.render(f"Time: {ftime}", 1, (72, 234, 54))
        # draw font obj on the surface
        self.__screen.blit(v, (self.__size[0] // 9 - 3, self.__size[1] * 7 + 21))


class Hints:

    """Hints system class

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = (size[0], size[1] // 9)
        self.__screen = screen
        self.__hint = "everything is well"

    @property
    def hint(self) -> str:
        """hint property (getter)"""
        return self.__hint

    @hint.setter
    def hint(self, value: str):
        """hint property (setter)

        :param value: hint value
        :type value: str
        """
        self.__hint = value

    def draw(self):
        """Draw Hint rect"""
        # Draw main frame
        # set frame lines width
        w = 1
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen,
            (72, 234, 54),
            ((0, self.__size[1]), (self.__size[0], self.__size[1])),
            w,
        )
        # create font object
        font = pygame.font.SysFont("rubik", 24)
        # render font object with hint
        v = font.render(f"Hint: {self.__hint}", 1, (72, 234, 54))
        # draw font obj on the surface
        self.__screen.blit(v, (self.__size[0] // 9 - 18, self.__size[1] + 25))


class AutoSolver:

    """Auto solver control panel class

    :param solver: solver object
    :type solver: Solver
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        self.__size = (size[0], size[1] // 9)
        self.__screen = screen
        self.__threads = Threads()
        self.__solver = solver
        self.__delay = 500
        s = (self.__size[0] - self.__size[0] // 2 - 25, self.__size[1] // 2)
        self.__buttons = [
            Button(*i, s, self.__screen)
            for i in (
                (self.pause, (-2, -2), "pause", (20, 220)),
                (self.resume, (-10, -2), "resume", (145, 220)),
                (self.start, (2, 0.8), "start", (20, 270)),
                (self.kill, (2.3, 0.9), "stop", (145, 270)),
            )
        ]
        self.__run = False

    @property
    def delay(self) -> float:
        """delay property (getter)"""
        return self.__delay_time

    @delay.setter
    def delay(self, value: float):
        """delay property (setter)

        :param value: delay value
        :type value: float
        """
        self.__delay = value

    @property
    def buttons(self):
        """buttons property (getter)"""
        return self.__buttons

    def start(self):
        """Start auto solver"""
        if not self.__run:
            self.__solver.kill
            self.__solver.e = True
            self.__threads.start(self.__solver.solve)
            self.__run = True

    def kill(self):
        """Kill/Stop auto solver"""
        self.__solver.kill
        self.__threads.stop()
        self.__run = False

    def pause(self):
        """pause auto solver by clear e flag"""
        if self.__run and self.__solver.e:
            self.__solver.e = False
            self.__run = False

    def resume(self):
        """resume auto solver by set e flag"""
        if not self.__run and not self.__solver.e:
            self.__solver.e = True
            self.__run = True

    def draw(self):
        """Draw auto solver rect"""
        # Draw main frame
        # set frame lines width
        w = 1
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen,
            (72, 234, 54),
            ((0, self.__size[1] * 2), (self.__size[0], self.__size[1] * 3)),
            w,
        )
        # set panel title
        self.__type(
            "Sudoku solver",
            (72, 234, 54),
            (self.__size[0] // 9 + 10, self.__size[1] * 2.15),
            30,
        )
        # three buttons (start/stop/pause/resume)
        for b in self.__buttons:
            b.draw()

    def __type(self, txt: str, rgb: tuple, pos: tuple, font_size: int):
        """Draw string on the surface screen

        :param txt: text to draw
        :type txt: str
        :param rgb: text color
        :type rgb: tuple
        :param pos: postition to draw
        :type pos: tuple
        :param font_size: font size plx
        :type font_size: int
        """
        # create font object
        font = pygame.font.SysFont("rubik", font_size)
        # render font object with text
        v = font.render(txt, 1, rgb)
        # draw font obj on the surface
        self.__screen.blit(v, pos)


class Button:

    """Button class 

    :param target: target funtion to start onclicked
    :type target: function
    :param s: left, top space
    :type s: tuple
    :param innertxt: inner text
    :type innertxt: str
    :param pos: square position (row, column)
    :type pos: tuple
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface 
    """

    def __init__(
        self,
        target,
        s: tuple,
        innertxt: str,
        pos: tuple,
        size: tuple,
        screen: pygame.Surface,
    ):
        self.__size = size
        self.__screen = screen
        self.__pos = pos
        self.__innertxt = innertxt
        self.__target = target
        self.__fill = (0, 0, 0)
        self.__w = 1
        self.__s = s
        self.__click_range = (
            range(self.__pos[0], self.__pos[0] + self.__size[0] + 1),
            range(self.__pos[1], self.__pos[1] + self.__size[1] + 1),
        )

    @property
    def click_range(self):
        """click range property"""
        return self.__click_range

    def click(self):
        """Handle click event"""
        print(f"clicked: {self.__innertxt}.")
        # change button style
        self.__fill = (10, 30, 0)
        self.__w = 2
        # call the traget
        self.__target()
        """# reset button style
        self.__fill = (0, 0, 0)
        self.__w = 1"""

    def draw(self):
        """Draw buttom rect"""
        # Draw main frame
        # draw rectangle (frame)
        pygame.draw.rect(
            self.__screen, (72, 234, 54), (self.__pos, self.__size), self.__w,
        )
        # set inner text
        # create font object
        font = pygame.font.SysFont("rubik", 24)
        # render font object with text
        v = font.render(self.__innertxt, 1, (72, 234, 54))
        # draw font obj on the surface
        self.__screen.blit(
            v,
            (
                self.__pos[0] + self.__size[0] // 4 + self.__s[0],
                self.__pos[1] + self.__size[1] // 8 + self.__s[1],
            ),
        )
