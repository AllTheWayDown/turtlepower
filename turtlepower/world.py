from __future__ import division, print_function, absolute_import

import sys
from random import randint, random, shuffle
from turtle import TurtleScreen, RawTurtle, TK


if sys.version_info[0] < 3:
    from Tkinter import Tk, mainloop
else:
    from tkinter import Tk
    mainloop = False



DEBUG = False


def noisy(value, variance=0.01):
    size = value * variance
    return value + (random() * size * 2) - size


def wrap(turtle, screen_width, screen_height):
    """wrap a turtle coords around"""
    x, y = turtle.pos()
    new_x = new_y = None
    if x > screen_width / 2:
        new_x = x - screen_width
    elif x < -screen_width / 2:
        new_x = x + screen_width

    if y > screen_height / 2:
        new_y = y - screen_height
    elif y < -screen_height / 2:
        new_y = y + screen_height

    was_down = turtle.isdown()
    if new_x is not None:
        turtle.penup()
        turtle.setx(new_x)
    if new_y is not None:
        turtle.penup()
        turtle.sety(new_y)
    if was_down:
        turtle.pendown()


def clamp(turtle, screen_width, screen_height):
    """Clamp turtle to window"""
    x, y = turtle.pos()
    new_x = new_y = None
    if x > screen_width / 2:
        new_x = screen_width / 2
    elif x < -screen_width / 2:
        new_x = -screen_width / 2

    if y > screen_height / 2:
        new_y = screen_height / 2
    elif y < -screen_height / 2:
        new_y = -screen_height / 2

    if new_x is not None:
        turtle.setx(new_x)
    if new_y is not None:
        turtle.sety(new_y)


class TurtleWorld(object):

    def __init__(self, width, height, borders=wrap, title="TurtlePower"):
        self.width = width
        self.half_width = width // 2
        self.height = height
        self.half_height = height // 2
        self.borders = borders
        self.window_title = title

        self.init_screen()

        self.fps = 0
        self.done = True
        self.turtles = []

    def init_screen(self):
        # intialise screen and turn off auto-render
        root = Tk()
        root.wm_title(self.window_title)
        window = TK.Canvas(master=root, width=self.width, height=self.height)
        window.pack()
        self.screen = TurtleScreen(window)
        self.screen.tracer(0, 0)

    def position_turtle(self, t, pos=None, angle=None):
        # move to location
        t.hideturtle()
        t.penup()
        if pos is None:
            pos = (randint(-self.half_width, self.half_width),
                   randint(-self.half_height, self.half_height))
        x, y = pos
        t.goto(x, y)
        if angle is None:
            angle = random() * 360
        t.setheading(angle)
        # ready to go
        t.showturtle()
        t.pendown()
        return t

    def random_position(self, turtle):
        return self.position_turtle(turtle)

    def _print_fps(self):
        if not self.done:
            print(self.fps)
            self.screen.ontimer(self._print_fps, 1000)
        self.fps = 0

    def create_turtle(self, callback, pos=None, angle=None):
        t = PowerTurtle(self)
        t.set_callback(callback)
        self.position_turtle(t, pos, angle)
        self.turtles.append(t)
        return t

    def add_turtle(self, turtle):
        turtle.clear()
        self.turtles.append(turtle)

    def remove_turtle(self, turtle):
        turtle.hideturtle()
        turtle.clear()
        self.turtles.remove(turtle)

    def run(self, ticks=1000):
        # run for 1000 ticks
        self.done = False
        if DEBUG:
            self.screen.ontimer(self._print_fps, 1000)
        self.ticks = ticks
        self.screen.ontimer(self.tick, 33)
        if mainloop:
            mainloop()
        else:
            self.screen.mainloop()

    def tick(self):
        shuffle(self.turtles)
        for t in self.turtles:
            t.callback(self)
            self.borders(t, self.width, self.height)
        self.screen.update()
        self.fps += 1
        self.ticks -= 1
        if self.ticks == 0:
            self.done = True
        else:
            self.screen.ontimer(self.tick, 33)


class PowerTurtleMixin(object):
    """A set of useful extra methods for a turtle"""
    type = "turtle"

    def __init__(self, world):
        self.world = world
        super(PowerTurtleMixin, self).__init__(world.screen)
        self.setup()

    def setup(self):
        """Initialisation function, called once"""
        super(PowerTurtleMixin, self).setup()

    def set_callback(self, callback):
        """Set the callback to a function, for classes usage"""
        self.callback = lambda world: callback(self, world)

    def turn_towards(self, desired, amount):
        """Helper to to turn a small amount towards a heading"""
        heading = self.heading()
        angle = desired - heading
        angle = (angle + 180) % 360 - 180
        if angle >= 0:
            amount = min(amount, angle)
        else:
            amount = max(-amount, angle)
        self.left(amount)
        return amount

    def get_neighbours(self, distance=60, angle=120):
        """Other turtles you can see that are with distance and angle of your
        current heading"""
        neighbours = []
        for t in self.world.turtles:
            if t is not self:
                a = abs(self.heading() - self.towards(t))
                if a < angle and self.distance(t) < distance:
                    neighbours.append(t)
        return neighbours


class PowerTurtle(PowerTurtleMixin, RawTurtle):

    def setup(self):
        """PowerTurtle based on stdlib turtle module"""
        pass
