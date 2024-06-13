import setup
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

from src.app import get_insurance_premium_cost

class RecommendationsRequest(Model):
    employees_data: list[dict]
    employees_pensions_params_data: list[dict]

class RecommendationsResponse(Model):
    total_premium_cost: float
    yearly_premium_cost: float

RecommendationsAgent = Agent(
    name="RecommendationsAgent",
    port=8003,
    seed="Recommendations Agent secret phrase",
    endpoint=["http://127.0.0.1:8003/submit"],
)

 
# Registering agent on Almananc and funding it.
fund_agent_if_low(RecommendationsAgent.wallet.address())

# On agent startup printing address
@RecommendationsAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'RecommendationsAgent Agent Address is {RecommendationsAgent.address}')

@RecommendationsAgent.on_query(model=RecommendationsRequest, replies={RecommendationsResponse})
async def query_handler(ctx: Context, sender: str, msg: RecommendationsRequest):
    try:
        ctx.logger.info(f'Getting recommendations for uploaded PRT doc')
        [total_cost, yearly_cost] = get_insurance_premium_cost(msg.employees_data, msg.employees_pensions_params_data)
        ctx.logger.info(f"Total cost: {total_cost:.2f},\n Yearly cost: {yearly_cost:.2f}")
        await ctx.send(sender, RecommendationsResponse(total_premium_cost=total_cost, yearly_premium_cost=yearly_cost))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, RecommendationsResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    RecommendationsAgent.run() 