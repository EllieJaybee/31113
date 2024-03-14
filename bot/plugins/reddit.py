import crescent
import hikari
import miru
from typing_extensions import Annotated as atd

import asyncpraw
from asyncpraw.models import Subreddit

from bot.secret import REDID, REDSECRET
from bot.__main__ import Model

Plugin = crescent.Plugin[hikari.GatewayBot, Model]
plugin = Plugin()


class RedditView(miru.View):
    def __init__(self, subreddit):
        self.subreddit: str = subreddit
        super().__init__(timeout=600)

    @miru.button(label="More🔄️", style=hikari.ButtonStyle.SUCCESS)
    async def more(self, ctx: miru.ViewContext, button: miru.Button):
        button.custom_id = self.subreddit
        await ctx.edit_response(components=None)
        await reddit(ctx, self.subreddit)

    async def on_timeout(self):
        await self.message.edit(components=None)


async def reddit(ctx: crescent.Context | miru.ViewContext, subreddit: str):
    if isinstance(ctx, crescent.Context):
        await ctx.defer()
    preddit = asyncpraw.Reddit(
        client_id=REDID,
        client_secret=REDSECRET,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    )
    sub: Subreddit = await preddit.subreddit(subreddit, fetch=True)
    if sub.over18:
        if isinstance(ctx, crescent.Context) and not ctx.channel.is_nsfw:
            await preddit.close()
            return await ctx.respond("horny 🫵", ephemeral=True)
    post = await sub.random()
    view = RedditView(subreddit=subreddit)
    respkwargs = {"components": view}
    if isinstance(ctx, crescent.Context):
        respkwargs["ensure_message"] = True
    message = await ctx.respond(
        f"[⠀](https://rxddit.com{post.permalink})", **respkwargs
    )
    await preddit.close()
    if isinstance(ctx, miru.ViewContext):
        message = await message.retrieve_message()
    plugin.model.miru.start_view(view, bind_to=message)
    await view.wait()


@plugin.include
@crescent.command(name="reddit", description="Fetches hot reddit stuff")
async def reddit_(
    ctx: crescent.Context, subreddit: atd[str, "subreddit you wanna fetch"]
):
    await reddit(ctx, subreddit)


@plugin.include
@crescent.command(description="Fetches a random hot reddit femboy post")
async def femboy(ctx: crescent.Context):
    await reddit(ctx, "Femboys")


@plugin.include
@crescent.command(description="Fetches a random hot reddit trap hentai post")
async def trap(ctx: crescent.Context):
    await reddit(ctx, "traphentai")


@plugin.include
@crescent.command(description="Fetches a random hot reddit hentai post")
async def hentai(ctx: crescent.Context):
    await reddit(ctx, "hentai")


@plugin.include
@crescent.command(description="Fetches cat pics")
async def meow(ctx: crescent.Context):
    await reddit(ctx, "cats")
