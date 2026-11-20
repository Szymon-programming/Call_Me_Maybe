import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel


class FileException(Exception):
    pass


def read_file_content(file_path: Path, role: str) -> Any:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileException(f"file with role: {role} and "
                            f"path {file_path} not found") from e
    except PermissionError as e:
        raise FileException(f"Access to file with path: {file_path}"
                            "denied or trying to open directory") from e
    except OSError as e:
        raise FileException(f"Error: {e} role: {role} to file with"
                            f"path: {file_path}") from e
    except json.JSONDecodeError as e:
        raise FileException(f"{e.msg}: line: {e.lineno} column: {e.colno}") from e
    except UnicodeDecodeError as e:
        raise FileException("Not correct utf-8 file") from e


def validate_data(data: Any, model_class: type[BaseModel], role: str) -> BaseModel:
    try:
        return model_class.model_validate(data)