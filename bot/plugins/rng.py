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
async def pick(ctx: crescent.Context, choices: atd[str, "Choices separated by commas"]):
    choice_list = choices.split(",")
    await ctx.respond(random.choice(choice_list), mentions_everyone=False, role_mentions=False, user_mentions=False)

@plugin.include
@crescent.command(description="Pick a random member")
async def pick_member(ctx: crescent.Context):
      await ctx.respond(random.choice(ctx.guild.get_members()), mentions_everyone=False, role_mentions=False, user_mentions=False)