from __future__ import division, print_function, absolute_import
from random import random

from world import TurtleWorld, PowerTurtle, wrap, noisy

ACCELERATION = 0.1
ROTATION = 4.0


class Boid(PowerTurtle):

    def setup(self):
        self.world.random_position(self)
        self.penup()
        self._move = random() * 4

    def callback(self, world):

        neighbours = self.get_neighbours(60, 120)
        if not neighbours:
            self._move = noisy(self._move)
            target_heading = self.heading() + random()*ROTATION*2 - ROTATION
        else:
            # cohesion
            center_x = []
            center_y = []
            # alignment
            headings = []
            speeds = []
            # separation
            #close_x = []
            #close_y = []
            myx, myy = self.position()
            for t in neighbours:
                x, y = t.position()
                speeds.append(t._move)
                headings.append(t.heading)
                center_x.append(x)
                center_y.append(y)

            target_speed = sum(speeds) / len(speeds)
            delta_speed = min(ACCELERATION, abs(target_speed - self._move))
            if self._move > target_speed:
                delta_speed = -delta_speed
            self._move += noisy(delta_speed)

            x1 = sum(center_x) / len(center_x)
            y1 = sum(center_y) / len(center_y)

            target_heading = noisy(self.towards((x1, y1)))

        self.turn_towards(target_heading, ROTATION)
        self.forward(self._move)


w = TurtleWorld(600, 600, wrap)
for i in range(50):
    w.add_turtle(Boid(w))
w.run(-1)
