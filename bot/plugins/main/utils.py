import crescent
import hikari

plugin = crescent.Plugin()


@plugin.include
@crescent.command(
    description="Check connection to server",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
async def ping(ctx: crescent.Context):
    latency = round(plugin.app.heartbeat_latency, 5) * 100
    await ctx.respond(f"{latency}ms")
    if ctx.channel.is_nsfw:
        await ctx.respond("also this channel sus")


@plugin.include
@crescent.command(
    description="Prints the bot's source code",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
async def source(ctx: crescent.Context):
    await ctx.respond("https://github.com/EllieJaybee/31113")
