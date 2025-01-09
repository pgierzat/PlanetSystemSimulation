from classes.central_object import CentralObject
from pipr_24z_pgierzat.errors import NegativeRadiusError
import pytest


def test_create_central_object():
    central_object = CentralObject(1e22, 1e3)
    assert central_object.pos_x() == 0
    assert central_object.pos_y() == 0
    assert central_object.mass() == 1e22
    assert central_object.radius() == 1e3


def test_create_central_object_with_negative_radius():
    with pytest.raises(NegativeRadiusError):
        CentralObject(1e22, -1)


def test_set_radius():
    central_object = CentralObject(1e22, 1e3)
    central_object.set_radius(2e3)
    assert central_object.radius() == 2e3


def test_set_radius_with_zero_value():
    central_object = CentralObject(1e22, 1e3)
    with pytest.raises(NegativeRadiusError):
        central_object.set_radius(0)


def test_set_radius_with_negative_value():
    central_object = CentralObject(1e22, 1e3)
    with pytest.raises(NegativeRadiusError):
        central_object.set_radius(-1)
