import pytest
import json
from iomodule import load_config
from errors import MalformedDataError


def test_load_config_valid(tmp_path):
    config_data = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "image_size": [800, 800],
        "time_step": 0.1,
        "objects": [{"x": 0, "y": 0, "mass": 1.0}, {"x": 1, "y": 1, "mass": 1.0}],
    }
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    config = load_config(config_file)
    assert config == config_data


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_file.json")


def test_load_config_invalid_json(tmp_path):
    invalid_json = "{central_mass: 1.0, central_radius: 1.0}"
    config_file = tmp_path / "invalid_config.json"
    with open(config_file, "w") as f:
        f.write(invalid_json)

    with pytest.raises(MalformedDataError):
        load_config(config_file)


def test_load_config_missing_required_field(tmp_path):
    config_data = {
        "central_mass": 1.0,
        "central_radius": 1.0,
        "scale": 1.0,
        "image_size": [800, 800],
        "time_step": 0.1,
        # Missing "objects" field
    }
    config_file = tmp_path / "config_missing_field.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    with pytest.raises(MalformedDataError):
        load_config(config_file)
