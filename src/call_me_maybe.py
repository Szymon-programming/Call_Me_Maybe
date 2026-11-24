from src.parser import (parse_arguments, functions_definitions_reader,
                        prompts_reader, output_writer, FileException,
                        OutputChecker)
import sys


def main() -> int:
    """Run the program: load the input files and write the results.

    The function reads command-line arguments, loads
    and validates the functions definitions and the prompts,
    and saves the result to the output file.

    Returns:
        Exit code: 0 on success, 1 if input output
        or any unexpected error.
    """
    paths = parse_arguments()
    try:
        functions_defs = functions_definitions_reader(
            paths.functions_definition)
        prompts = prompts_reader(paths.input)
        # there will be generation
        results_list: list[OutputChecker] = []
        print(f"Loaded {len(functions_defs.root)} functions "
              f"and {len(prompts.root)} prompts")
        output_writer(paths.output, results_list)
        print(f"Saved {len(results_list)} elements "
              f"to {paths.output}")
    except FileException as e:
        print(e, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
    return 0
