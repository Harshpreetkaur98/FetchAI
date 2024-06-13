import setup
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

from src.agents.extraction_utils import extract_prt_summary

class ExtractionRequest(Model):
    pass

class ExtractionResponse(Model):
    extracted_info: str
    n_words: int


ExtractionAgent = Agent(
    name="ExtractionAgent",
    port=8001,
    seed="Extraction Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

 
# Registering agent on Almananc and funding it.
fund_agent_if_low(ExtractionAgent.wallet.address())

# On agent startup printing address
@ExtractionAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'ExtractionAgent Address is {ExtractionAgent.address}')

@ExtractionAgent.on_query(model=ExtractionRequest, replies={ExtractionResponse})
async def query_handler(ctx: Context, sender: str, msg: ExtractionRequest):
    try:
        ctx.logger.info(f'Getting extracted info from uploaded PRT doc')
        extracted_info = extract_prt_summary()
        n_words = len(extracted_info.split(' '))
        ctx.logger.info(f"Extracted {n_words} words")
        await ctx.send(sender, ExtractionResponse(extracted_info=extracted_info, n_words=n_words))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ExtractionResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    ExtractionAgent.run() 