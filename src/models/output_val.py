from pydantic import BaseModel, ConfigDict


class OutputChecker(BaseModel):
    """Pydantic model validating output file correctness.

    Class checks that the output has all required fields no
    extra keys and valid value types.

    Attributes:
        prompt: Prompt from prompts file.
        name: Name of function that matched the prompt.
        parameters: Mapping of parameter names to their values.
    """

    prompt: str
    name: str
    parameters: dict[str, float | int | str | bool]
    model_config = ConfigDict(
        extra="forbid",
        strict=True
    )
