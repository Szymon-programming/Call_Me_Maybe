from pathlib import Path
import json
from src.models import OutputChecker
from src.parser import FileException


def output_writer(file_path: Path,
                  result_list: list[OutputChecker]) -> None:
    """Write results to a JSON file.

    Args:
        file_path: Path to the output file.
        result_list: list of outputs one per prompt.

    Raises:
        FileException: If the destination file cannot be created,
            cannot be opened to write, has no permission,
            path is a directory, serialization error
            or there is no space left on the device.
    """
    write_data = [x.model_dump() for x in result_list]
    try:
        json_text = json.dumps(write_data, ensure_ascii=False,
                               allow_nan=False, indent=2)
    except TypeError as e:
        raise FileException(f"In file with path: {file_path} "
                            "result cannot be serialized "
                            f"to JSON: {e}") from e
    except ValueError as e:
        raise FileException("Result cannot be written as JSON: "
                            f"{e} in file with path: "
                            f"{file_path}") from e
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise FileException("No permission to create directory with path: "
                            f"{file_path.parent}") from e
    except OSError as e:
        raise FileException(f"Cannot make an output directory: {e}"
                            ", in directory with path: "
                            f"{file_path.parent}") from e
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json_text)
    except PermissionError as e:
        raise FileException("No permission to create file with path: "
                            f"{file_path}") from e
    except OSError as e:
        raise FileException(f"Cannot make an output file: {e}"
                            ", with path: "
                            f"{file_path}") from e
