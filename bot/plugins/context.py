import crescent
import hikari
from pysaucenao import SauceNao, errors
from typing_extensions import Annotated as atd

from bot.secret import SAUCETOKEN

plugin = crescent.Plugin()

@plugin.include
@crescent.message_command(name="Find Sauce")
async def sauce(ctx: crescent.Context, message: hikari.Message):
    await ctx.defer(ephemeral=True)
    sauceclient = SauceNao(api_key=SAUCETOKEN, results_limit=1)
    if message.attachments:
        for att in message.attachments:
            sourced = await sauceclient.from_url(att.url)
            await ctx.respond(sourced[0].url)
    elif message.content:
        if "https://" not in message.content:
            return await ctx.respond("Nothing to be sauced")
        for word in message.content.split():
            if word.startswith("https://"):
                try:
                    sourced = await sauceclient.from_url(word)
                    await ctx.respond(sourced[0].url)
                except errors.InvalidImageException:
                    await ctx.respond("Invalid url")
    else:
        await ctx.respond("Nothing to be sauced")