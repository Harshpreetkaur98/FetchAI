import setup
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

from src.agents.rules_generator_utils import execute_code, generate_code_rules

class RulesGeneratorRequest(Model):
    extracted_info: str
    employees_data: str

class RulesGeneratorResponse(Model):
    employees_pensions_params_data: list[dict]

RulesGeneratorAgent = Agent(
    name="RulesGenerator",
    port=8002,
    seed="Rules Agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)

 
# Registering agent on Almananc and funding it.
fund_agent_if_low(RulesGeneratorAgent.wallet.address())

# On agent startup printing address
@RulesGeneratorAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'RulesGenerator Address is {RulesGeneratorAgent.address}')

@RulesGeneratorAgent.on_query(model=RulesGeneratorRequest, replies={RulesGeneratorResponse})
async def query_handler(ctx: Context, sender: str, msg: RulesGeneratorRequest):
    try:
        ctx.logger.info(f'Preparing data for generation of code rules')
        code = generate_code_rules(msg.extracted_info, msg.employees_data)
        employees_pensions_params_data = execute_code(code)
        await ctx.send(sender, RulesGeneratorResponse(employees_pensions_params_data=employees_pensions_params_data))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, RulesGeneratorResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    RulesGeneratorAgent.run() 