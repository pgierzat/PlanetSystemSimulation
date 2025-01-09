import pytest
from classes.system import System
from classes.central_object import CentralObject
from classes.object import Object


@pytest.fixture
def config():
    return {
        "central_mass": 1.0,  # Masa obiektu centralnego [kg]
        "central_radius": 1.0,  # Promień obiektu centralnego [m]
        "scale": 1.0,  # Liczba metrów na piksel
        "image_size": (800, 800),  # Rozmiar obrazu w pikselach
        "time_step": 0.1,  # Odstęp czasowy (1 godzina) [s]
        "objects": [
            {"x": 0, "y": 0, "mass": 1.0, "velocity_x": 1.0, "velocity_y": 1.0},
            {"x": 0, "y": 0, "mass": 1.0, "velocity_x": -1.0, "velocity_y": -1.0},
            {"x": 1, "y": 1, "mass": 1.0, "velocity_x": 5.0, "velocity_y": -1.0}
        ],
    }


def test_system_initialization(config):
    system = System(config)
    assert isinstance(system.central_object(), CentralObject)
    assert len(system.objects()) == 3
    assert isinstance(system.objects()[0], Object)
    assert system.scale() == 1.0
    assert system.dt() == 0.1


def test_system_create_no_objects():
    config = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "objects": [],
        "image_size": (800, 800),
        "time_step": 0.1
    }
    system = System(config)
    assert len(system.objects()) == 0


def test_check_collisions_start(config):
    system = System(config)
    collisions = system.check_collisions()
    assert len(collisions) == 1  # Two objects start at the same position


def test_calculate_distance(config):
    system = System(config)
    obj1 = system.objects()[0]
    obj3 = system.objects()[2]
    distance = system.calculate_distance(obj1, obj3)
    assert distance == pytest.approx(1.414, rel=1e-2)  # sqrt(2) ≈ 1.414


def test_large_number_of_objects():
    config = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "objects": [{"x": i, "y": i, "mass": 1.0} for i in range(1000)],
        "image_size": (800, 800),
        "time_step": 0.1
    }
    system = System(config)
    assert len(system.objects()) == 1000


def test_extreme_coordinates():
    config = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "objects": [
            {"x": 1e12, "y": 1e12, "mass": 1.0},
            {"x": -1e12, "y": -1e12, "mass": 1.0}
        ],
        "image_size": (800, 800),
        "time_step": 0.1
    }
    system = System(config)
    obj1 = system.objects()[0]
    obj2 = system.objects()[1]
    distance = system.calculate_distance(obj1, obj2)
    assert distance == pytest.approx(2.828e12, rel=1e-2)  # sqrt(2) * 1e12 ≈ 2.828e12
