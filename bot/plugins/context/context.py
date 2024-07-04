import crescent
import hikari
from pysaucenao import SauceNao, errors

from bot.__main__ import Model

Plugin = crescent.Plugin[hikari.GatewayBot, Model]
plugin = Plugin()


class NoSauceError(IndexError):
    pass


@plugin.include
@crescent.message_command(name="Find Sauce")
async def sauce(ctx: crescent.Context, message: hikari.Message):
    await ctx.defer(ephemeral=True)
    sauceclient = SauceNao(api_key=plugin.model.secret.SAUCE_TOKEN, results_limit=1)
    if message.attachments:
        for att in message.attachments:
            sourced = await sauceclient.from_url(att.url)
            if not sourced:
                raise NoSauceError
            await ctx.respond(sourced[0].url)
    elif message.content:
        if "https://" not in message.content:
            return await ctx.respond("Nothing to be sauced")
        for word in message.content.split():
            if word.startswith("https://"):
                sourced = await sauceclient.from_url(word)
                await ctx.respond(sourced[0].url)
    else:
        await ctx.respond("Nothing to be sauced")


@plugin.include
@crescent.catch_command(NoSauceError)
async def no_sauce_handler(err: NoSauceError, ctx: crescent.Context):
    await ctx.respond("Can't sauce message :<")


@plugin.include
@crescent.catch_command(errors.InvalidImageException)
async def invalid_image_handler(
    err: errors.InvalidImageException, ctx: crescent.Context
):
    await ctx.respond("Invalid url")
