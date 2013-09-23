from __future__ import division, print_function, absolute_import

from random import randint, random, shuffle
from turtle import TurtleScreen, RawTurtle, TK
from tkinter import Tk

def noisy(value, variance=0.01):
    size = value * variance
    return value + (random() * size * 2) - size


def wrap(t, W, H):
    """wrap a turtle coords around"""
    x, y = t.pos()
    nx = ny = None
    if x > W / 2:
        nx = x - W
    elif x < -W / 2:
        nx = x + W

    if y > H / 2:
        ny = y - H
    elif y < -H / 2:
        ny = y + H

    down = t.isdown()
    if nx is not None:
        t.penup()
        t.setx(nx)
    if ny is not None:
        t.penup()
        t.sety(ny)
    if down:
        t.pendown()


def clamp(t, W, H):
    """Clamp turtle to window"""
    x, y = t.pos()
    nx = ny = None
    if x > W / 2:
        nx = W / 2
    elif x < -W / 2:
        nx = -W / 2

    if y > H / 2:
        ny = H / 2
    elif y < -H / 2:
        ny = -H / 2

    if nx is not None:
        t.setx(nx)
    if ny is not None:
        t.sety(ny)


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

    def position_turtle(self, t, pos, angle):
        # move to location
        t.hideturtle()
        t.penup()
        if pos is None:
            x = randint(-self.half_width, self.half_width)
            y = randint(-self.half_height, self.half_height)
        else:
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
        return self.position_turtle(turtle, None, None)

    def print_fps(self):
        if not self.done:
            print(self.fps)
            self.screen.ontimer(self.print_fps, 1000)
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
        #self.screen.ontimer(self.print_fps, 1000)
        self.ticks = ticks
        self.screen.ontimer(self.tick, 33)
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
    type = "turtle"

    def __init__(self, world):
        self.world = world
        super(PowerTurtleMixin, self).__init__(world.screen)
        self.setup()

    def setup(self):
        super(PowerTurtleMixin, self).setup()

    def set_callback(self, callback):
        self.callback = lambda world: callback(self, world)

    def turn_towards(self, desired, amount):
        heading = self.heading()
        angle = desired - heading
        angle = (angle + 180) % 360 - 180
        if angle >= 0:
            amount = min(amount, angle)
        else:
            amount = max(-amount, angle)
        self.left(amount)
        return amount

    def get_neighbours(self, distance, angle):
        neighbours = []
        for t in self.world.turtles:
            if t is not self:
                a = abs(self.heading() - self.towards(t))
                if a < angle and self.distance(t) < distance:
                    neighbours.append(t)
        return neighbours


class PowerTurtle(PowerTurtleMixin, RawTurtle):

    def setup(self):
        pass
