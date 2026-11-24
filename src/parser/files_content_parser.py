import json
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel, ValidationError
from src.models.function_definitions_val import FunctionInputListChecker
from src.models.prompts_val import PromptsInputListChecker


T = TypeVar("T", bound=BaseModel)


class FileException(Exception):
    """Error raised when file cannot be read or validated.

    The message is written for the user
    and is printed as it is.
    """


def read_file_content(file_path: Path, role: str) -> Any:
    """Read a JSON file and return its parsed content.

    Args:
        file_path: Path to the JSON file.
        role: Short name of the file's purpose,
            used in error messages.

    Returns:
        Parsed JSON content.

    Raises:
        FileException: If the file is missing, cannot be opened,
            is not valid UTF-8 or does not contain
            valid JSON.
    """
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
    """Format a pydantic validation error as a readable message.

    The message contains the number of errors, the first five errors with
    the path to the invalid field and the number of hidden errors.

    Args:
        exception: Validation error raised by pydantic.
        role: Short name of the file's purpose, used in the message.

    Returns:
        Multi-line text describing the errors.
    """
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
    """Validate data with a pydantic model.

    Args:
        data: Parsed JSON content to validate.
        model_class: Model class that the data must match.
        role: Short name of the file's purpose, used in error messages.

    Returns:
        Instance of model_class built from the data.

    Raises:
        FileException: If the data does not match the model.
    """
    try:
        return model_class.model_validate(data)
    except ValidationError as e:
        long_error = validate_data_error(e, role)
        raise FileException(long_error) from e


def functions_definitions_reader(file_path:
                                 Path) -> FunctionInputListChecker:
    """Read and validate the functions definitions file.

    Args:
        file_path: Path to the functions definitions file.

    Returns:
        Validated list of function definitions.

    Raises:
        FileException: If the file cannot be read or its content is invalid.
    """
    role = "functions definitions"
    content = read_file_content(file_path, role)
    return validate_data(content, FunctionInputListChecker, role)


def prompts_reader(file_path: Path) -> PromptsInputListChecker:
    """Read and validate the prompts file.

    Args:
        file_path: Path to the prompts file.

    Returns:
        Validated list of prompts.

    Raises:
        FileException: If the file cannot be read or its content is invalid.
    """
    role = "prompts"
    content = read_file_content(file_path, role)
    return validate_data(content, PromptsInputListChecker, role)
