from __future__ import division, print_function, absolute_import
from time import sleep

from random import randint, random, shuffle
from time import time

from world import TurtleWorld, PowerTurtle
max_speed = 3  # how fast they move
max_turn = 10  # maximum turn speed in degrees

def random_walk(t, world):
    """Simple random walk"""
    t.penup()
    angle = random() * max_turn * 2 - max_turn
    t.right(angle)
    t.forward(max_speed)


class RandomTurtle(PowerTurtle):
    type = "random"

    def callback(self, world):
        random_walk(self, world)


class Asteroid(PowerTurtle):
    type = 'asteroid'
    ship = None

    def setup(self):
        self.penup()
        self.color('brown')
        self.shape("circle")
        self.size = 0.5 + random() * 4.0
        self.radius = 10 * self.size
        self.shapesize(self.size, self.size)
        hw = self.world.half_width
        hh = self.world.half_height
        x = randint(hw - 100, hw)
        if random() < 0.5:
            x = -x
        y = randint(hh - 100, hh)
        if random() < 0.5:
            y = -y
        self.setpos(x, y)
        self.setheading(self.towards(0, 0) + (random() * 90) - 45)
        self.speed = (random() * 2.0) + 0.1

    def callback(self, world):
        ship = world.ship
        if self.distance(ship) < self.radius:
            ship.die()
        if ship.rocket and self.distance(ship.rocket) < self.radius:
            self.clear()
            world.remove_turtle(self)
            world.remove_turtle(ship.rocket)
            ship.rocket = None
        else:
            self.penup()
            self.forward(self.speed)


class Ship(PowerTurtle):
    type = 'ship'

    def setup(self):
        self.shape('turtle')
        self.fillcolor('green')
        self.setheading(90)
        self.dead = False
        self.rocket = None
        self.__range = 300

    def callback(self, world):
        self.penup()
        if not self.dead:
            asteroids = [t for t in world.turtles if t.type == 'asteroid']
            if not asteroids:
                self.write("I WIN, HUMAN")
                sleep(5)
                bye()
            distances = [(self.distance(a) - a.radius, a) for a in asteroids]
            distances.sort()
            dangerous =[(d, a) for d, a in distances if d < 100]
            if dangerous:
                self.run(dangerous)
            else:
                self.shoot(distances[0][0], distances[0][1], world)

    def run(self, dangerous):
        d, a = dangerous[0]:
        lr = -90 if random() > 0.5 else 90
        self.__running_heading = self.towards(a) + lr
        self.__running_distance = 50
        self.runto()

    def shoot(self, distance, a, world):
        diff = self.turn_towards(self.towards(a), 6)
        if distance < self.__range:
            if diff < 1:
                self.fire()
        else:
            self.forward(1)

    def fire(self):
        if self.rocket is None:
            self.rocket = Rocket(w)
            self.rocket.init(self.heading(), self.pos(), self.__range)
            self.world.add_turtle(self.rocket)

    def die(self):
        if not self.dead:
            self.write("GAME OVER")
            self.dead = True


class Rocket(PowerTurtle):
    type = 'rocket'

    def setup(self):
        self.shape('triangle')
        self.shapesize(0.2, 1)
        self.color('black')
        self.__travelled = 0

    def init(self, heading, pos, range):
        self.penup()
        self.setheading(heading)
        self.setpos(*pos)
        self.pendown()
        self.__range= range

    def callback(self, world):
        if self.__travelled > self.__range:
            world.remove_turtle(self)
            world.ship.rocket = None
        else:
            self.forward(4)
            self.__travelled += 4


if __name__ == '__main__':
    w = TurtleWorld(600, 600, wrap)
    ship = Ship(w)
    w.ship = ship
    w.add_turtle(ship)
    for i in range(10):
        a = Asteroid(w)
        w.add_turtle(a)
    w.run(-1)
