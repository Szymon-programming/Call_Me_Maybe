import json
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel, ValidationError
from src.models.function_definitions_val import FunctionInputListChecker
from src.models.prompts_val import PromptsInputListChecker


T = TypeVar("T", bound=BaseModel)


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
        raise FileException(f"Access to file with path: {file_path} "
                            "denied or trying to open directory") from e
    except OSError as e:
        raise FileException(f"Error: {e} role: {role} to file with "
                            f"path: {file_path}") from e
    except json.JSONDecodeError as e:
        raise FileException(f"Error in file with path: {file_path} "
                            f"with role: {role}. "
                            f"{e.msg}: line: {e.lineno} "
                            f"column: {e.colno}") from e
    except UnicodeDecodeError as e:
        raise FileException(f"Error in file with path: {file_path} "
                            f"with role: {role}. "
                            "Not correct utf-8 file") from e


def validate_data_error(exception: ValidationError, role: str) -> str:
    errors_list_of_dicts = exception.errors()
    count_of_errors = exception.error_count()
    return_list: list[str] = []
    return_list.append(f"Errors: {count_of_errors}. "
                       f"file role: {role}")
    for i, log in enumerate(errors_list_of_dicts[:5], start=1):
        loc = log["loc"]
        str_loc = [str(item) for item in loc]
        if not str_loc:
            loc_message = "whole file"
        else:
            loc_message = " -> ".join(str_loc)
        msg = log["msg"]
        return_list.append(f"error {i}: loc is: {loc_message}, "
                           f"msg is: {msg}")
    if count_of_errors > 5:
        return_list.append(f"and {count_of_errors - 5} more errors.")
    return "\n".join(return_list)


def validate_data(data: Any, model_class: type[T],
                  role: str) -> T:
    try:
        return model_class.model_validate(data)
    except ValidationError as e:
        long_error = validate_data_error(e, role)
        raise FileException(long_error) from e


def functions_definitions_reader(file_path:
                                 Path) -> FunctionInputListChecker:
    role = "functions definitions"
    content = read_file_content(file_path, role)
    return validate_data(content, FunctionInputListChecker, role)


def prompts_reader(file_path: Path) -> PromptsInputListChecker:
    role = "prompts"
    content = read_file_content(file_path, role)
    return validate_data(content, PromptsInputListChecker, role)
