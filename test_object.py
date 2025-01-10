from classes.object import Object
from errors import NegativeMassError
import pytest


def test_create_object():
    object1 = Object(10, 10, 1e10, 200, 300)
    assert object1.pos_x() == 10.0
    assert object1.pos_y() == 10.0
    assert object1.mass() == 1e10
    assert object1.velocity_x() == 200.0
    assert object1.velocity_y() == 300.0


def test_create_negative_mass():
    with pytest.raises(NegativeMassError):
        Object(10, 10, -1000, 200, 300)


def test_create_zero_mass():
    with pytest.raises(NegativeMassError):
        Object(10, 10, 0, 200, 300)


def test_object_pos_setters():
    object1 = Object(10, 10, 1e10, 200, 300)
    assert object1.pos_x() == 10.0
    assert object1.pos_y() == 10.0
    object1.set_pos_y(-100.65)
    object1.set_pos_x(50000.65)
    assert object1.pos_x() == 50000.65
    assert object1.pos_y() == -100.65


def test_object_vel_setters():
    object1 = Object(10, 10, 1e10, 200, 300)
    assert object1.velocity_x() == 200.0
    assert object1.velocity_y() == 300.0
    object1.set_vel_x(-100.65)
    object1.set_vel_y(50000.65)
    assert object1.velocity_x() == -100.65
    assert object1.velocity_y() == 50000.65
