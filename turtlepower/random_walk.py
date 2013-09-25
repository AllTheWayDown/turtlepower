import sys
from random import random, randint

from turtlepower.world import TurtleWorld

# simulation parameters
W = 600
H = 600
num_turtles = 100  # num turtles

if len(sys.argv) > 1:
    num_turtles = int(sys.argv[1])

max_speed = 2  # how fast they move
max_turn = 10  # maximum turn speed in degrees


world = TurtleWorld(W, H)


def random_walk(turtle, world=None):
    angle = random() * max_turn * 2 - max_turn
    turtle.right(angle)
    turtle.forward(max_speed)

shapes = [
    'turtle',
    'classic',
    'square',
    'circle',
    'triangle',
    'arrow',
]

n = num_turtles // len(shapes)

for shape in shapes:
    for _ in range(n):
        turtle = world.create_turtle(callback=random_walk)
        turtle.penup()
        turtle.shape(shape)
        turtle.color(random(), random(), random())

world.run()
