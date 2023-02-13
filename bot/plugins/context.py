import crescent
import hikari
from pysaucenao import SauceNao
from typing_extensions import Annotated as atd

from bot.secret import SAUCETOKEN

plugin = crescent.Plugin()

@plugin.include
@crescent.message_command(name="Find Sauce")
async def sauce(ctx: crescent.Context, message: hikari.Message):
    if not message.attachments:
        return await ctx.respond("No attachments to be sauced")
    await ctx.defer()
    sauceclient = SauceNao(api_key=SAUCETOKEN, results_limit=1)
    for att in message.attachments:
        sourced = await sauceclient.from_url(att.url)
        await ctx.respond(sourced[0].url)