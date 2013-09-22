from mock import Mock
from nose.tools import eq_

from turtlepower.world import clamp, wrap


def _make_mock_turtle(x, y):
    turtle = Mock()
    turtle.pos.return_value = (x, y)
    return turtle


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
