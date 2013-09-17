import sys
from random import randint, random
from time import time

from turtle import TurtleScreen, RawTurtle, TK

# simulation parameters
W = 800
H = 800
n = 100  # num turtles

if len(sys.argv) > 1:
    n = int(sys.argv[1])

max_speed = 2  # how fast they move
max_turn = 10  # maximum turn speed in degrees
too_close = 20  # how close is too close?
e = 0.1
sight = 50
fov = 270


def wrap(t):
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

    if nx is not None:
        t.penup()
        t.setx(nx)
    if ny is not None:
        t.penup()
        t.sety(ny)
    t.pendown()


def clip(t):
    """Clip turtle to window"""
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


# intialise screen and turn off auto-render
window = TK.Canvas(width=W, height=H)
window.pack()
s = TurtleScreen(window)
s.tracer(0, 0)


# random initial positions
turtles = [RawTurtle(s) for i in range(n)]
for t in turtles:
    t.ht()
    t.penup()
    t.goto(randint(0, W) - W / 2, randint(0, H) - H / 2)
    t.right(randint(0, 360))
    t.st()
    #t.pendown()


def random_walk(t):
    """Simple random walk"""
    angle = random() * max_turn * 2 - max_turn
    t.right(angle)
    t.forward(max_speed)

# fps tracking
frames = 0


def print_frames():
    global frames
    print(frames)
    frames = 0
    s.ontimer(print_frames, 1000)

s.ontimer(print_frames, 1000)

# run for 1000 ticks
mt = mc = 0
rt = rc = 0
for i in range(200):
    start = time()
    for t in turtles:
        random_walk(t)
        wrap(t)
    mt += time() - start
    mc += 1
    start = time()
    s.update()
    rt += time() - start
    rc += 1
    frames += 1


print(mt/mc)
print(rt/rc)
