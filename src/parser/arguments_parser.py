from pathlib import Path
from argparse import ArgumentParser
from pydantic import BaseModel


class PathChecker(BaseModel):
    """Pydantic model validating program start flags.

    Class checks correctness of 3 flags given at program start.
    First is a functions definitions file path, second is a
    prompt file path and 3rd is an output file path.

    Attributes:
        functions_definition: Path to the file with functions definitions.
        input: Path to the file with prompts.
        output: Path to the file where output will be written.
    """

    functions_definition: Path
    input: Path
    output: Path


def parse_arguments() -> PathChecker:
    """Parse command-line arguments.

    This function sets the Paths to functions definitions,
    input and output files. If a flag is missing, the default
    path is used. If a flag is given, its value is used.

    Returns:
        PathChecker object with three paths.

    Raises:
        SystemExit: When flag is incorrect.
    """
    file_directory = Path(__file__).resolve().parents[2]
    parser = ArgumentParser(description="Parse files names")
    parser.add_argument("--functions_definition", type=Path,
                        default=file_directory / "data" /
                        "input" / "functions_definition.json")
    parser.add_argument("--input", type=Path,
                        default=file_directory / "data" /
                        "input" / "function_calling_tests.json")
    parser.add_argument("--output", type=Path,
                        default=file_directory / "data" /
                        "output" / "function_calls.json")
    args = parser.parse_args()
    return PathChecker.model_validate(vars(args))
