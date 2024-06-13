import subprocess
from ..setup import project_root
from .openai_utils import openai_prompt
import json
from os import path

data_path = path.join(project_root, './src/data/data.json')
def _get_employee_records(n: int):
    # load json file
    
    with open(data_path, 'r') as file:
        employees = json.load(file)
        # select n employees
    return employees[:n]


prompt_path = path.join(project_root, './src/prompts/rules.txt')
def _get_rules_prompt(extracted_info: str, employees_data: str):
    with open(prompt_path, 'r') as file:
        prompt_msg = file.read()
    prompt_msg += "\n###JSON_RECORDS\n"
    # prompt_msg += json.dumps(_get_employee_records(3)) 
    prompt_msg += employees_data
    prompt_msg += "\n\n###EXTRACTION_HERE\n"
    prompt_msg += extracted_info
    # print(prompt_msg)
    return prompt_msg

def generate_code_rules(extracted_info: str, employees_data: str):
    """
    extracted_info: the extracted summary/info from the PTR document
    employees_data: structured JSON employee data in string format
    """
    prompt = _get_rules_prompt(extracted_info, employees_data)
    raw_code = openai_prompt(prompt)
    # print(raw_code)
    return raw_code.replace('```python', '').replace('```', '')

def execute_code(code: str, file_name = path.join(project_root, './src/temp.py')): 
    """
    code: a string that contains executable Python code
    filename: optional parameter than can specify where to temporarily store the code during its
    return deserialised json result with output from the executable code string 
    """
    # write code to file
    with open(file_name, 'w') as file:
        file.write(code)
    result = subprocess.run(["python", file_name], capture_output=True, text=True)
    print("Generated code execution Output (output in data/processed_data.json):")
    print(result.stdout)
    print("Generated code execution Errors:")
    print(result.stderr)
    # return computed data
    computed_path = path.join(project_root, './src/data/processed_data.json')
    with open(computed_path, 'r') as f:
        return json.load(f)
    # os.remove(file_name)
