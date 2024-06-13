from setup import project_root
from flask import Flask, jsonify
from flask_cors import CORS  
from uagents.query import query  
import json
from src.agents.recommendations import RecommendationsRequest  
from src.agents.extraction import ExtractionRequest
from src.agents.rules_generator import RulesGeneratorRequest
from os import path

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

extraction_agent_address = 'agent1qv5y3fs29zhqdmc79cu73xaak83a0pzmprhnh8c0m592dxm3t5qavnypuw3'

rules_generator_agent_address = 'agent1qgvjfr07fc2l243we72tvjgh2dsw2xcnhn734tqserfw489p942ej65tjca'

recommendation_agent_address = 'agent1qf35y7j3yrjvsfg69rrl7jklgrynaugshpfndu79jgd9gpq0lkfdkt4994f'

employees_data_path = path.join(project_root, './src/data/data.json')

@app.route('/')
def home():
    return "Welcome to the Insurance Premium Recommendations API!"

@app.route('/api', methods=['GET'])
async def handle_api_req():
    # 1. extract summary from PRT document
    # TODO: doc is static for now but can be changed
    extraction_response = await query(destination=extraction_agent_address,
    message=ExtractionRequest(), timeout=90.0)
    extraction_dict = json.loads(extraction_response.decode_payload())
    extracted_info = extraction_dict['extracted_info']

    # 2. TODO: for now employee data is static but can be uploaded in the future
    with open(employees_data_path, 'r') as f:
        employees_data = json.load(f)
    rules_gen_response = await query(destination=rules_generator_agent_address,
    message=RulesGeneratorRequest(extracted_info=extracted_info, employees_data=json.dumps(employees_data)), timeout=90.0)

    rules_gen_dict = json.loads(rules_gen_response.decode_payload())
    employees_pensions_params_data = rules_gen_dict['employees_pensions_params_data']

    # 3. Get recommendations based on outputs from above
    recommendation_response = await query(destination=recommendation_agent_address, message=RecommendationsRequest(employees_data=employees_data, employees_pensions_params_data=employees_pensions_params_data), timeout=90.0)
    if not recommendation_response:
        return jsonify("No response from recommendation agent")
    insurance_recommendation = json.loads(recommendation_response.decode_payload())
    return jsonify(insurance_recommendation)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)