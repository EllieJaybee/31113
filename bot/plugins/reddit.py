import crescent
from typing_extensions import Annotated as atd

import aiohttp
import json
import random

plugin = crescent.Plugin()
subsort = ["hot", "new", "rising", "top"]
timelist = ["hour", "day", "week", "month", "year", "all"]

async def request(ctx: crescent.Context, endpoint: str):
    await ctx.defer()
    url = "https://reddit.com/"+endpoint
    params = {"t": random.choice(timelist)} if "/top.json" in endpoint else None
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                            params=params) as req:
            resp = await req.text()
        return json.loads(resp)

async def gallery(ctx: crescent.Context, gallery_data: dict):
    for p in gallery_data['media_metadata']:
        _id = p['id']
        _format = p['m'].split("/")[-1]
        await ctx.respond(f"https://i.reddit.com/{_id}.{_format}")

async def reddit(ctx: crescent.Context, subreddit: str, offset: int):
    if not ctx.channel.is_nsfw:
        return await ctx.respond("horny 🫵", ephemeral=True)
    d = await request(ctx, f"r/{subreddit}/{random.choice(subsort)}.json")
    postlist = d['data']['children'][offset:]
    post = random.choice(postlist)
    try:
        if "reddit.com/gallery/" in post['data']['url_overridden_by_dest']:
            return await gallery(ctx, post)
        await ctx.respond(post['data']['url_overridden_by_dest'])
    except KeyError:
            await ctx.respond("The post queried is not a media post")

@plugin.include
@crescent.command(name="reddit", description="Fetches hot reddit stuff")
async def _reddit(ctx: crescent.Context, subreddit: atd[str, "subreddit you wanna fetch"]):
    await reddit(ctx, subreddit, 0)

@plugin.include
@crescent.command(description="Fetches a random hot reddit femboy post")
async def femboy(ctx: crescent.Context):
    await reddit(ctx, "Femboys", 1)

@plugin.include
@crescent.command(description="Fetches a random hot reddit trap hentai post")
async def trap(ctx: crescent.Context):
    await reddit(ctx, "traphentai", 2)

@plugin.include
@crescent.command(description="Fetches a random hot reddit hentai post")
async def hentai(ctx: crescent.Context):
    await reddit(ctx, "hentai", 0)