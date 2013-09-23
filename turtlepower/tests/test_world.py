import random

from mock import call, Mock, patch
from nose.tools import eq_

from turtlepower.world import clamp, TurtleWorld, wrap


def _make_mock_turtle(x, y):
    turtle = Mock()
    turtle.pos.return_value = (x, y)
    return turtle


@patch('turtlepower.world.TurtleScreen', Mock())
@patch('turtlepower.world.TK.Canvas', Mock())
def _get_screenless_world():
    return TurtleWorld(10, 10)


def _bound_check(bound_func, before, expected):
    mock_turtle = _make_mock_turtle(*before)
    bound_func(mock_turtle, 10, 10)
    after_x, after_y = before
    if len(mock_turtle.setx.call_args_list):
        setx_args, _ = mock_turtle.setx.call_args
        after_x = setx_args[0]
    if len(mock_turtle.sety.call_args_list):
        sety_args, _ = mock_turtle.sety.call_args
        after_y = sety_args[0]
    eq_(expected, (after_x, after_y))


def test_wrap():
    # Assume a width and height of 10
    for before, expected in [
        ((0, 0), (0, 0)),  # Middle of screen
        ((-9, 2), (1, 2)),  # Off left
        ((9, 2), (-1, 2)),  # Off right
        ((2, -9), (2, 1)),  # Off bottom
        ((2, 9), (2, -1)),  # Off top
        ((-9, -9), (1, 1)),  # Off both
    ]:
        yield _bound_check, wrap, before, expected


def test_wrap_doesnt_put_the_pen_down_if_it_isnt_already_down():
    turtle = _make_mock_turtle(-9, -9)
    turtle.isdown.return_value = False
    wrap(turtle, 10, 10)
    eq_(0, turtle.pendown.call_count)


def test_wrap_puts_the_pen_down_if_it_was_already_down():
    turtle = _make_mock_turtle(-9, -9)
    turtle.isdown.return_value = True
    wrap(turtle, 10, 10)
    eq_(1, turtle.pendown.call_count)


def test_clamp():
    # Assume a width and height of 10
    for before, expected in [
        ((0, 0), (0, 0)),  # Middle of screen
        ((-9, 2), (-5, 2)),  # Off left
        ((9, 2), (5, 2)),  # Off right
        ((2, -9), (2, -5)),  # Off bottom
        ((2, 9), (2, 5)),  # Off top
        ((-9, -9), (-5, -5)),  # Off both
    ]:
        yield _bound_check, clamp, before, expected


class TestTurtleWorld(object):

    def test_position_turtle_uses_parameters(self):
        turtle = _make_mock_turtle(0, 0)
        world = _get_screenless_world()
        x, y, angle = 1, 2, 3
        world.position_turtle(turtle, (x, y), angle)
        eq_([call(x, y)], turtle.goto.call_args_list)
        eq_([call(angle)], turtle.setheading.call_args_list)

    def test_random_position(self):
        random.seed(0)
        turtle = _make_mock_turtle(0, 0)
        world = _get_screenless_world()
        world.random_position(turtle)
        world.random_position(turtle)
        eq_([call(1, 1), call(3, 2)], turtle.goto.call_args_list)
        eq_([call(14.574376145079917), call(145.77628948214914)],
            turtle.setheading.call_args_list)
