from pydantic import BaseModel
from typing import Literal

class Function_checker(BaseModel):
	type: Literal["number", "integer", "string", "boolean"]