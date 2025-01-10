from classes.base_object import BaseObject
from errors import NegativeMassError
import pytest


def test_base_object_create():
    base_object = BaseObject(10, 10, 1e10)
    assert base_object.pos_x() == 10.0
    assert base_object.pos_y() == 10.0
    assert base_object.mass() == 1e10


def test_base_object_create_negative_mass():
    with pytest.raises(NegativeMassError):
        BaseObject(10, 10, -1000)


def test_base_object_pos_setters():
    base_object = BaseObject(10, 10, 1e10)
    assert base_object.pos_x() == 10.0
    assert base_object.pos_y() == 10.0
    base_object.set_pos_y(-100.65)
    base_object.set_pos_x(50000.65)
    assert base_object.pos_x() == 50000.65
    assert base_object.pos_y() == -100.65
