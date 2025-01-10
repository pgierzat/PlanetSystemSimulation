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
            {
                "x": 0,
                "y": 0,
                "mass": 1.0,
                "velocity_x": 1.0,
                "velocity_y": 1.0,
            },
            {
                "x": 0,
                "y": 0,
                "mass": 1.0,
                "velocity_x": -1.0,
                "velocity_y": -1.0,
            },
            {
                "x": 1,
                "y": 1,
                "mass": 1.0,
                "velocity_x": 5.0,
                "velocity_y": -1.0,
            },
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
        "time_step": 0.1,
    }
    system = System(config)
    assert len(system.objects()) == 0


def test_check_collisions_start(config):
    system = System(config)
    collisions = system.check_collisions()
    assert len(collisions) == 3  # Objects are initialized in the center


def test_check_collisions_no_collisions():
    config = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "objects": [{"x": i, "y": i, "mass": 1.0} for i in range(1, 1000)],
        "image_size": (800, 800),
        "time_step": 0.1,
    }
    system = System(config)
    collisions = system.check_collisions()
    assert len(collisions) == 0


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
        "time_step": 0.1,
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
            {"x": -1e12, "y": -1e12, "mass": 1.0},
        ],
        "image_size": (800, 800),
        "time_step": 0.1,
    }
    system = System(config)
    obj1 = system.objects()[0]
    obj2 = system.objects()[1]
    distance = system.calculate_distance(obj1, obj2)
    assert distance == pytest.approx(2.828e12, rel=1e-2)  # sqrt(2) * 1e12
    # ≈ 2.828e12


def test_simulate(config):
    system = System(config)
    trajectories, collision_report = system.simulate(10)
    assert len(trajectories) == 3
    assert len(collision_report) >= 0


def test_objects_moving(config):
    system = System(config)
    initial_positions = [
        (obj.pos_x(), obj.pos_y()) for obj in system.objects()
    ]
    system.simulate(10)
    final_positions = [(obj.pos_x(), obj.pos_y()) for obj in system.objects()]
    for initial, final in zip(initial_positions, final_positions):
        assert initial != final


def test_objects_collide_and_move_as_combined(config):
    config = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "image_size": (800, 800),
        "time_step": 0.1,
        "objects": [
            {
                "x": 10,
                "y": 5,
                "mass": 1.0,
                "velocity_x": 1.0,
                "velocity_y": 0.0,
            },
            {
                "x": 10,
                "y": 5,
                "mass": 1.0,
                "velocity_x": -1.0,
                "velocity_y": 0.0,
            },
        ],
    }
    system = System(config)
    initial_positions = [
        (obj.pos_x(), obj.pos_y()) for obj in system.objects()
    ]
    assert len(system.objects()) == 2
    system.simulate(10)
    final_positions = [(obj.pos_x(), obj.pos_y()) for obj in system.objects()]
    # check if objects have moved
    for initial, final in zip(initial_positions, final_positions):
        assert initial != final
    # check if objects have collided and merged
    assert len(system.objects()) == 1
    combined_object = system.objects()[0]
    assert (
        combined_object.pos_x() != initial_positions[0][0]
        and combined_object.pos_y() != initial_positions[0][1]
    )
    assert combined_object.mass() == 2.0
