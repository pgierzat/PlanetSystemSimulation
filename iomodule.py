import json
from errors import MalformedDataError


def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
    except json.JSONDecodeError:
        raise MalformedDataError(
            f"File {file_path} is not a valid JSON file"
        )
    required_fields = [
        "central_mass",
        "central_radius",
        "scale",
        "image_size",
        "time_step",
        "objects",
    ]
    for field in required_fields:
        if field not in config:
            raise MalformedDataError(
                f"Missing required field '{field}' in configuration file."
            )
    return config
