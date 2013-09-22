from __future__ import division, print_function, absolute_import

from world import TurtleWorld, PowerTurtleMixin
from ninjaturtle.ninja import NinjaTurtle
from ninjaturtle.engine import ENGINE
from turgles.renderer import Renderer


class NinjaPowerTurtle(PowerTurtleMixin, NinjaTurtle):
    pass


class NinjaWorld(TurtleWorld):

    def init_screen(self):
        ENGINE.renderer = Renderer(800, 800, 16)
        self.render = ENGINE.renderer.render

    def print_fps(self):
        if not self.done:
            print(self.fps)
            #self.screen.ontimer(self.print_fps, 1000)
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
