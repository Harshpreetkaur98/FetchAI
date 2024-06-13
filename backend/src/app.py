from setup import project_root
from src.agents.extraction_utils import extract_prt_summary
from src.agents.recommendations_utils import get_insurance_premium_cost
from os import path
import json
from src.agents.rules_generator_utils import generate_code_rules, execute_code



# TODO: structured employee data should become another dynamic step
# app.py
employees_data_path = path.join(project_root, './src/data/data.json')
if __name__ == "__main__":
    extracted_info = extract_prt_summary()
    with open(employees_data_path, 'r') as f:
        employees_data = json.load(f)
    code = generate_code_rules(extracted_info, json.dumps(employees_data))
    employees_pensions_parameters = execute_code(code)
    [total_premium_cost, yearly_premium] = get_insurance_premium_cost(employees_data=employees_data, employees_pensions_params=employees_pensions_parameters)
    formatted_total_premium_cost = f"Total Cost: £{total_premium_cost:.2f}"
    print(formatted_total_premium_cost)
    formatted_yearly_premium = f"Yearly minimum premium: £{yearly_premium:.2f}"
    print(formatted_yearly_premium)