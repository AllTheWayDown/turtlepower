from __future__ import division, print_function, absolute_import
from random import randint, random

from world import TurtleWorld, PowerTurtle, wrap


class Boid(PowerTurtle):

    def setup(self):
        self.world.random_position(self)
        self.penup()

    def callback(self, world):
        neighbours = [t for t in world.turtles if t.distance(self) < 60]
        headings = []
        speeds = []
        for t in neighbours:
            headings.append(t.heading())
            speeds.append(t.speed())
        self.speed(sum(speeds) / len(speeds))
        self.setheading(sum(headings) / len(headings))
        self.forward(3)


w = TurtleWorld(600, 600, wrap)
for i in range(10):
    w.add_turtle(Boid(w))
w.run(-1)
