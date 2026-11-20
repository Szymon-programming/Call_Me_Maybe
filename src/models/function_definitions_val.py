from typing import Literal, Annotated
from collections import Counter
from pydantic import BaseModel, Field, RootModel, model_validator


class TypeChecker(BaseModel):
    """Pydantic model validating parameter type.

    Class checks whether given parameter has
    right type in a functions definition file.

    Attributes:
        type: Type of parameters in function definition
    """

    type: Literal["number", "integer", "string", "boolean"]


class FunctionCorrectnessChecker(BaseModel):
    """Pydantic model validating function correctness.

    Class checks whether the function definitions are
    correct and whether they have all required fields.

    Attributes:
        name: Name of a function.
        description: Description of what the function does.
        parameters: Function parameters.
        returns: Type of the value that this
            function is returning.
    """

    name: str = Field(min_length=1)
    description: str
    parameters: dict[Annotated[str, Field(min_length=1)], TypeChecker]
    returns: TypeChecker


class FunctionInputListChecker(RootModel[Annotated
                                         [list[FunctionCorrectnessChecker],
                                          Field(min_length=1)]]):
    """Pydantic model validating non-empty list of functions definitions.

    Class validates whether there are duplicates in function names
    given as a list from the definitions file and whether there is
    at least one function.

    Attributes:
        root: List of functions definitions loaded from input file.
    """

    @model_validator(mode='after')
    def check_if_unique_names(self) -> 'FunctionInputListChecker':
        """Check whether function names are unique.

        This function validates whether name of functions loaded from
        input file as a list of functions are unique and have
        no duplicates.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If any function appears more than once.
        """
        functions_names = [f.name for f in self.root]
        duplicates = [name for name, count in
                      Counter(functions_names).items() if count > 1]
        if len(duplicates) > 0:
            raise ValueError(f"duplicated function name: {duplicates}")
        return self
