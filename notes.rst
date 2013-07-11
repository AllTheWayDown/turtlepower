
PowerTurtle API
===============

Small steps
-----------

 - constrained turtle for moving in small steps
 - turtle move every time slice (dt), default ~33ms (30/sec)
 - max_speed is world distance/second
 - max_turn is degrees/second
 - speed as normal (1..10)
 - forward/back are capped by max_speed * dt * speed()/10.0
 - left/right are capped by max_turn * dt speed()/10.0
 - in interactive mode, just run until no more actions

 - forward()/back() with no args moves constrained amount
 - forward(n)/back(n) is may take multiple time slices

Helper methods
--------------

difference, distance = Turtle.turn_towards(x, y)
difference, distance = Turtle.turn_towards_heading(angle)
difference, distance = Turtle.turn_away(x, y)
difference, distance = Turtle.move_towards(x, y)
difference, distance = Turtle.move_towards_heading(angle)
difference, distance = Turtle.move_away_from(x, y)
difference, distance = Turtle.move_towards_heading(angle)

Actions
-------
    long running actions that occur over multiple time slices
    e.g.

    Turtle.actions.move_to(x, y)



Ink
---

 - represent whatever the the turtle draws/stamps.
 - where placed in world depends on normal pen characteristics
 - default ink is just Ink

 - other inks:
   - Wall - not passable (need collisions)
   - Acid - hurts to cross (needs health)
   - Resource (food, water, etc)


Game ideas
----------

 - predator/prey
 - tron/snakes
 - traffic/cars
 - flocking
 - asteroids
 - maze solving
 - race course
 - resource search/competions
 - ant colony


World ideas
-----------

Small amount of noise to all turn/move values?
