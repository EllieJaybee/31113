import crescent
import hikari
import miru
from typing_extensions import Annotated as atd

import asyncpraw
from asyncpraw.models import Subreddit, Submission

from bot.secret import REDID, REDSECRET

plugin = crescent.Plugin()

class RedditView(miru.View):

    async def on_timeout(self):
        await self.message.edit(components=None)
        await MoreButton.preddit.close()

class MoreButton(miru.Button):
    def __init__(self, subreddit: str):
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label="More🔄️")
        self.sub = subreddit

    async def callback(self, ctx: miru.ViewContext):
        await ctx.edit_response(components=None)
        await MoreButton.reddit(ctx, self.sub, False)
        self.view.stop()

    @classmethod
    async def reddit(cls, ctx: crescent.Context, subreddit: str, new_: bool = True):
        if new_:
            await ctx.defer()
            cls.preddit = asyncpraw.Reddit(
            client_id=REDID,
            client_secret=REDSECRET,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )
        sub: Subreddit = await cls.preddit.subreddit(subreddit, fetch=True)
        if sub.over18:
            if isinstance(ctx, crescent.Context) and not ctx.channel.is_nsfw:
                await cls.preddit.close()
                return await ctx.respond("horny 🫵", flags=hikari.MessageFlag.EPHEMERAL)
        post = await sub.random()
        view = RedditView(timeout=600)
        view.add_item(MoreButton(subreddit))
        message = await ctx.respond(f"[⠀](https://rxddit.com{post.permalink})", components=view)
        await view.start(message)
        await view.wait()

@plugin.include
@crescent.command(name="reddit", description="Fetches hot reddit stuff")
async def reddit_(ctx: crescent.Context, subreddit: atd[str, "subreddit you wanna fetch"]):
    await MoreButton.reddit(ctx, subreddit)

@plugin.include
@crescent.command(description="Fetches a random hot reddit femboy post")
async def femboy(ctx: crescent.Context):
    await MoreButton.reddit(ctx, "Femboys")

@plugin.include
@crescent.command(description="Fetches a random hot reddit trap hentai post")
async def trap(ctx: crescent.Context):
    await MoreButton.reddit(ctx, "traphentai")

@plugin.include
@crescent.command(description="Fetches a random hot reddit hentai post")
async def hentai(ctx: crescent.Context):
    await MoreButton.reddit(ctx, "hentai")

@plugin.include
@crescent.command(description="Fetches cat pics")
async def meow(ctx: crescent.Context):
    await MoreButton.reddit(ctx, "cats")