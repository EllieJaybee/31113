import crescent
import random
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()

@plugin.include
@crescent.command(description="Generates a random number in a range")
async def rng(ctx: crescent.Context, min: atd[int, "Lowest number"], max: atd[int, "Highest number"]):
	await ctx.respond(random.randint(min, max))

@plugin.include
@crescent.command(description="Pick randomly from a list of choices")
async def pick(ctx: crescent.Context, choice1: str, choice2: str = None, choice3: str = None, choice4: str = None, choice5: str = None):
    res = [choice1, choice2, choice3, choice4, choice5]
    choices = [i for i in res if i is not None]
    await ctx.respond(random.choice(choices))
