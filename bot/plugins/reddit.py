import crescent
import hikari
import miru
from typing_extensions import Annotated as atd

import aiohttp
import json

plugin = crescent.Plugin()

async def request(ctx: crescent.Context, endpoint: str):
    url = "https://reddit.com/"+endpoint
    params = {"raw_json": 1}
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                            params=params) as response:
            response_text = await response.text()
        return json.loads(response_text)

async def gallery(ctx: crescent.Context, gallery_data: dict):
    for post in gallery_data['media_metadata']:
        id_ = post['id']
        format_ = post['m'].split("/")[-1]
        await ctx.respond(f"https://i.reddit.com/{id_}.{format_}")

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
            if not ctx.channel.is_nsfw:
                return await ctx.respond("horny 🫵", flags=hikari.MessageFlag.EPHEMERAL)
        data = await request(ctx, f"r/{subreddit}/random.json")
        post= data[0]['data']['children'][0]
        try:
            if "reddit.com/gallery/" in post['data']['url_overridden_by_dest']:
                return await gallery(ctx, post)
            view = miru.View(timeout=None)
            view.add_item(MoreButton(subreddit))
            message = await ctx.respond(post['data']['url_overridden_by_dest'], components=view)
            await view.start(message)
            await view.wait()
        except KeyError:
            await ctx.respond("The post queried is not a media post")

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