import crescent

plugin = crescent.Plugin()


@plugin.include
@crescent.command(description="Check connection to server")
async def ping(ctx: crescent.Context):
    latency = round(plugin.app.heartbeat_latency, 5) * 100
    await ctx.respond(f"{latency}ms")
    if ctx.channel.is_nsfw:
        await ctx.respond("also this channel sus")


@plugin.include
@crescent.command(description="Prints the bot's source code")
async def source(ctx: crescent.Context):
    await ctx.respond("https://github.com/EllieJaybee/31113")
