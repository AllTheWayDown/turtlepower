from mock import Mock
from nose.tools import eq_

from turtlepower.world import wrap


def _make_mock_turtle(x, y):
    turtle = Mock()
    turtle.pos.return_value = (x, y)
    return turtle


def _wrap_check(before, expected):
    mock_turtle = _make_mock_turtle(*before)
    wrap(mock_turtle, 10, 10)
    after_x, after_y = before
    if len(mock_turtle.setx.call_args_list):
        args, _ = mock_turtle.setx.call_args
        after_x = args[0]
    if len(mock_turtle.sety.call_args_list):
        args, _ = mock_turtle.sety.call_args
        after_y = args[0]
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
        yield _wrap_check, before, expected
