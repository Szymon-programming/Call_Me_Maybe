from pydantic import BaseModel, RootModel


class PromptChecker(BaseModel):
    """Pydantic model validating one entry from prompts file.

    Class checks whether given prompt has
    string type in a prompts definition file.

    Attributes:
        prompt: Prompt given as a string.
    """

    prompt: str


class PromptsInputListChecker(RootModel[list[PromptChecker]]):
    """Pydantic model validating list of prompts.

    Class is a list of entries from the prompts file, list
    can be empty and prompts can be repeated.

    Attributes:
        root: List of prompts loaded from propmts file.
    """
