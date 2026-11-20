from src.models.function_definitions_val import FunctionInputListChecker
from pathlib import Path
import json


definitions_path = Path(__file__).resolve().parents[1] / "data" / "input" / "functions_definition.json"
with open(definitions_path, "r") as file:
	text = json.load(file)
	try:
		function_list = FunctionInputListChecker(text)
		print(function_list)
	except:
		print("some error")