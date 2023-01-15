import crescent
import random
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()

@plugin.include
@crescent.command(description="Check connection to server")
async def ping(ctx: crescent.Context):
	await ctx.respond("pong")
	if ctx.channel.is_nsfw:
		await ctx.respond("also this channel sus")

@plugin.include
@crescent.command(description="Generates a random number in a range")
async def rng(ctx: crescent.Context, min: atd[int, "Lowest number"], max: atd[int, "Highest number"]):
	await ctx.respond(random.randint(min, max))

@plugin.include
@crescent.command(description="Prints the bot's source code")
async def source(ctx: crescent.Context):
	await ctx.respond("https://github.com/EllieJaybee/31113")