import pygame, time

# local import
from base.base import GUIBase
from solver.parallel import Threads
from generator.generator import Generator


class LeftPanel(GUIBase):

    """Left control panel

    :param solver: solver object
    :type solver: Solver
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0] - size[1], size[1]), screen)
        self.gamesystem = GameSystem(self.size, self.screen)
        self.time = Time(self.size, self.screen)
        self.hints = Hints(self.size, self.screen)
        self.auto_solver = AutoSolver(solver, self.size, self.screen)
        self.options = Options(solver, self.size, self.screen)

    def draw(self):
        """Draw the left panel on the screen"""
        # Draw main frame
        # set frame lines width
        w = 3
        # draw rectangle (frame)
        pygame.draw.rect(
            self.screen, (72, 234, 54), ((0, 0), (self.size[0], self.size[1])), w
        )
        # print(Sudoku at the top)
        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, 0), (self.size[0], self.size[1] // 9)),
            w // 3,
        )
        self._type("Sudoku", (72, 234, 54), (self.size[0] // 4, 14), 42)
        # draw hint panel
        self.hints.draw()
        # draw auto solver control panel
        self.auto_solver.draw()
        # draw time panel at the bottom (above wrongs panel)
        self.time.draw()
        # draw gamesystem panel at the bottom
        self.gamesystem.draw()
        # draw option panel (solve, select, reset, generate)
        self.options.draw()


class GameSystem(GUIBase):

    """GameSystem system class

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__wrongs_counter = 0
        self.__lost = False
        self.__won = False

    def reset(self):
        """reset won/lost and wrongs counter"""
        self.__lost = False
        self.__won = False
        self.__wrongs_counter = 0

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
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 8), (self.size[0], self.size[1])),
            w,
        )
        # draw wrongs
        # check if the player lost or won
        if self.__won:
            self._type(
                "You Won",
                (72, 234, 54),
                (self.size[0] // 4 - 10, self.size[1] * 8 + 15),
                38,
            )
        elif not self.__lost:
            self._type(
                "X  " * self.__wrongs_counter,
                (234, 72, 54),
                (40, self.size[1] * 8 + 15),
                38,
            )
        else:
            self._type(
                "You Lost",
                (234, 72, 54),
                (self.size[0] // 4 - 15, self.size[1] * 8 + 15),
                38,
            )


class Time(GUIBase):

    """Time managment class

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__init_time = time.time()

    @property
    def init_time(self):
        """init time property (getter)"""
        return self.__init_time

    @init_time.setter
    def init_time(self, value: time.time):
        """init time property (setter)

        :param value: init time value
        :type value: time.time
        """
        self.__init_time = value

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
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 7), (self.size[0], self.size[1])),
            w,
        )
        # draw time delata
        ftime = self.__time_formatter(time.time() - self.__init_time)
        self._type(
            f"Time: {ftime}",
            (72, 234, 54),
            (self.size[0] // 9 - 3, self.size[1] * 7 + 21),
            32,
        )


class Hints(GUIBase):

    """Hints system class

    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
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
            self.screen,
            (72, 234, 54),
            ((0, self.size[1]), (self.size[0], self.size[1])),
            w,
        )
        # draw hint
        self._type(
            f"Hint: {self.__hint}",
            (72, 234, 54),
            (self.size[0] // 9 - 18, self.size[1] + 25),
            24,
        )


class AutoSolver(GUIBase):

    """Auto solver control panel class

    :param solver: solver object
    :type solver: Solver
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__threads = Threads()
        self.__solver = solver
        # create control buttons
        controlsize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 2)
        self.__buttons = [
            Button(*i, controlsize, self.screen)
            for i in (
                (self.pause, (), (-2, -2), "pause", 24, (20, 220)),
                (self.resume, (), (-10, -2), "resume", 24, (145, 220)),
                (self.start, (), (2, 0.8), "start", 24, (20, 270)),
                (self.kill, (), (2.3, 0.9), "stop", 24, (145, 270)),
            )
        ]
        # create delay buttons
        delaysize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 4)
        self.__buttons.extend(
            [
                Button(*i, delaysize, self.screen)
                for i in (
                    (self.delay, (1000), (15, -1), "1.0", 16, (20, 345)),
                    (self.delay, (500), (15, -1), "0.5", 16, (20, 373)),
                    (self.delay, (750), (10, -1), "0.75", 16, (145, 345)),
                    (self.delay, (250), (10, -1), "0.25", 16, (145, 373)),
                )
            ]
        )
        self.__run = False

    @property
    def delay(self) -> float:
        """delay property (getter)"""
        return self.__solver.delay

    def delay(self, value: float):
        """delay property (setter)

        :param value: delay value
        :type value: float
        """
        self.__solver.delay = value

    @property
    def buttons(self):
        """buttons property (getter)"""
        return self.__buttons

    def start(self):
        """Start auto solver"""
        if not self.__run:
            self.__solver.kill = False
            self.__solver.e = True
            self.__threads.start(self.__solver.auto_solver)
            self.__run = True

    def kill(self):
        """Kill/Stop auto solver"""
        self.__solver.kill = True
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
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 2), (self.size[0], self.size[1] * 3)),
            w,
        )
        # set panel title
        self._type(
            "Sudoku solver",
            (72, 234, 54),
            (self.size[0] // 9 + 10, self.size[1] * 2.15),
            30,
        )
        # set delay part title
        self._type(
            "Delay (secs)", (72, 234, 54), (self.size[0] // 3, self.size[1] * 4), 18
        )
        # draw buttons
        for b in self.__buttons:
            b.draw()


class Options(GUIBase):

    """Options class

    :param solver: solver object
    :type solver: Solver
    :param size: screen size (width height)
    :type size: tuple
    :param screen: pygame screen
    :type screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__solver = solver
        self.__generator = Generator()
        # create control buttons
        controlsize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 2)
        self.__buttons = [
            Button(*i, controlsize, self.screen)
            for i in (
                (self.solve_all, (), (14.25, -1.8), "all", 24, (20, 450)),
                (self.solve_selected, (), (-16, -1.8), "selected", 24, (145, 450)),
                (self.reset, (), (1.8, 0.7), "reset", 24, (20, 500)),
                (self.generate, (), (-18.3, 0.7), "generate", 24, (145, 500)),
            )
        ]

    @property
    def buttons(self):
        """buttons property (getter)"""
        return self.__buttons

    def solve_all(self) -> bool:
        """Solve entire board

        :returns: solvability
        :rtype: bool
        """
        # solve all
        s = self.__solver.solve(self.__solver.board.board)
        self.__solver.board.update_squares()
        return s

    def solve_selected(self, board: list, pos: tuple):
        """Solve selected square

        :param board: sudoku board to solve
        :type board: list
        :param pos: square position
        :type pos: tuple
        """
        # solve the board
        solution = self.__solver.solve(board)
        # if it's solvable set selected square value
        if solution and pos:
            self.__solver.board.board[pos[0]][pos[1]] = board[pos[0]][pos[1]]
            self.__solver.board.update_squares()
        return solution

    def generate(self, board: list) -> bool:
        """Generate new board

        :param board: sudoku board
        :type board: list
        """
        # set new random generated Sudoku board
        board.board = self.__generator.generate()
        return True

    def reset(self) -> bool:
        """Reset board"""
        # iterate over all squares
        for r in range(9):
            for c in range(9):
                # check for changeable squares
                if self.__solver.board.squares[r][c].changeable:
                    # reset it to 0
                    self.__solver.board.board[r][c] = 0
        # clear wrong square
        if self.__solver.board.wrong:
            self.__solver.board.clear
        # update squares
        self.__solver.board.update_squares()
        return True

    def draw(self):
        """Draw auto solver rect"""
        # sovle txt
        self._type("solve", (72, 234, 54), (110, 420), 22)
        # draw buttons
        for b in self.__buttons:
            b.draw()


class Button(GUIBase):

    """Button class

    :param target: target funtion to start onclicked
    :type target: function
    :param _args: target funtion args
    :type _args: tuple
    :param s: left, top space
    :type s: tuple
    :param innertxt: inner text
    :type innertxt: str
    :param fontsize: innertxt size
    :type fontsize: int
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
        _args: tuple,
        s: tuple,
        innertxt: str,
        fontsize: int,
        pos: tuple,
        size: tuple,
        screen: pygame.Surface,
    ):
        super().__init__(size, screen)
        self.__pos = pos
        self.__innertxt = innertxt
        self.__fontsize = fontsize
        self.__target = target
        self.__args = _args
        self.__fill = (0, 0, 0)
        self.__w = 1
        self.__s = s
        self.__click_range = (
            range(self.__pos[0], self.__pos[0] + self.size[0] + 1),
            range(self.__pos[1], self.__pos[1] + self.size[1] + 1),
        )

    @property
    def innertxt(self):
        """innertxt property (getter)"""
        return self.__innertxt

    @property
    def click_range(self):
        """click range property"""
        return self.__click_range

    @property
    def reset(self):
        """Reset button style"""
        self.__fill = (0, 0, 0)
        self.__w = 1

    def click(self, args: tuple = ()):
        """Handle click event

        :param args: target function args if the args isn't constant
        :type args: tuple
        """
        # change button style
        self.__fill = (30, 50, 20)
        self.__w = 2
        # call the traget
        if self.__args:
            return self.__target(self.__args)
        elif args:
            return self.__target(*args)
        else:
            return self.__target()

    def draw(self):
        """Draw button rect"""
        # Draw main frame
        # draw rectangle (frame)
        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            (self.__pos, self.size),
            self.__w,
        )
        # set inner text
        self._type(
            self.__innertxt,
            (72, 234, 54),
            (
                self.__pos[0] + self.size[0] // 4 + self.__s[0],
                self.__pos[1] + self.size[1] // 8 + self.__s[1],
            ),
            self.__fontsize,
        )
