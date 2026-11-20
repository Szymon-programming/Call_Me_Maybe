from src.models.prompts_val import PromptsInputListChecker
from pathlib import Path
import json


definitions_path = Path(__file__).resolve().parents[1] / "data" / "input" / "function_calling_tests.json"
with open(definitions_path, "r") as file:
	text = json.load(file)
	try:
		function_list = PromptsInputListChecker(text)
		print(function_list)
	except:
		print("some error")