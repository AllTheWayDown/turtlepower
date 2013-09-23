"""Basic ramming together of turtlepower and pymunk.
Bouncing ball demo with a turtle?
Requires pymunk"""
from turtlepower.world import TurtleWorld, PowerTurtle, clamp, RawTurtle
import pymunk as pm


class SpaceWorld(TurtleWorld):
    """World with physics for turtles"""
    def __init__(self, *args, **kwargs):
        self.space = pm.Space()
        super(SpaceWorld, self).__init__(*args, **kwargs)

    def tick(self):
        super(SpaceWorld, self).tick()
        #note - if the step is too high - right now it can break its bounds.
        #This may be an interaction between tick, and the physics.
        self.space.step(0.01)


class SpaceTurtle(PowerTurtle):
    """Turtle with physics.
    Needs a SpaceWorld (normal turtle world will break)."""

    def setup(self):
        self.body = pm.Body(1, 1666)
        self.pm_shape = pm.Circle(self.body, 10.0, (0, 0))
        self.pm_shape.elasticity = 0.95
        self.body.position = self.position()
        self.world.space.add(self.body, self.pm_shape)
        self.goto = self.setposition = self.setpos
        self.ondrag(self.start_drag)
        self.onrelease(self.end_drag)

    def start_drag(self, x, y):
        #print("Drag received!")
        if not self.body.is_sleeping:
            self.body.sleep()
        self.goto(x, y)

    def end_drag(self, x, y):
        self.goto(x, y)
        self.body.activate()

    def setpos(self, x, y=None):
        if y is None:
            position = x
        else:
            position = x, y
        #print("Setting position %s", repr(position))
        self.body.position = position
        super(SpaceTurtle, self).setpos(position)

    def setx(self, x):
        print("Setting x %d", x)
        super(SpaceTurtle, self).setx(x)
        self.body.position = self.position()

    def sety(self, y):
        print("Setting y %d", y)
        super(SpaceTurtle, self).sety(y)
        self.body.position = self.position()

    def callback(self, world):
        super(SpaceTurtle, self).setpos(self.body.position)
        super(SpaceTurtle, self).settiltangle(self.body.angle)


class WorldWithLines:
    def __init__(self, world):
        self.world = world
        self.make_line_bodies()
        self.draw()

    def make_line_bodies(self):
        """Create a line for the turtles to interact with"""
        self.static_body = pm.Body()
        self.static_lines = [
            pm.Segment(self.static_body, (-299.0, -250.0),
                       (299.0, -259.0), 0.0),
            pm.Segment(self.static_body,
                       (299.0, -259.0), (299.0, 250.0), 0.0),
            pm.Segment(self.static_body,
                       (-299.0, -250.0), (-299.0, 250.0), 0.0)
        ]
        for line in self.static_lines:
            line.elasticity = 0.95
        self.world.space.add(self.static_lines)

    def draw(self):
        """Draw the static lines"""
        #create turtle (no shape - just dot?)
        dt = RawTurtle(self.world.screen)
        #self.world.add_turtle(dt)
        dt.hideturtle()
        for line in self.static_lines:
            dt.penup()
            #Go to line first coord
            dt.goto(line.a)
            #pen down
            dt.pendown()
            #Go to line 2nd coord
            dt.goto(line.b)


def world_edge(*args, **kwargs):
    pass


def setup():
    """Setup turtles world, and physics world"""
    world = SpaceWorld(600, 600, world_edge, "test")
    world.space.gravity = 0, -500
    st = SpaceTurtle(world)
    st.color('red')
    st.shape('circle')
    st.sety(300)
    #st.body.apply_impulse((10, 0))
    world.add_turtle(st)
    st2 = SpaceTurtle(world)
    st2.setx(150)
    st2.sety(300)
    st2.color('blue')
    world.add_turtle(st2)
    #st.body.mass = 4
    #st.body.inertia = 1000
    wl = WorldWithLines(world)
    return world


if __name__ == "__main__":
    w = setup()
    w.run(-1)
