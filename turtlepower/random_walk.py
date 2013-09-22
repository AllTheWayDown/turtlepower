import sys
from random import randint, random
from time import time

from turtle import TurtleScreen, RawTurtle, TK

from turtlepower.world import TurtleWorld, wrap

# simulation parameters
W = 800
H = 800
n = 100  # num turtles

if len(sys.argv) > 1:
    n = int(sys.argv[1])

max_speed = 2  # how fast they move
max_turn = 10  # maximum turn speed in degrees


world = TurtleWorld(W, H)


def random_walk(turtle, world=None):
    angle = random() * max_turn * 2 - max_turn
    turtle.right(angle)
    turtle.forward(max_speed)


for _ in range(n):
    x, y = (randint(0, W) - W / 2, randint(0, H) - H / 2)
    angle = randint(0, 360)
    world.create_turtle(random_walk, (x, y), angle)

world.run()
