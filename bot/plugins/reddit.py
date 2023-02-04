import crescent
from typing_extensions import Annotated as atd

import aiohttp
import json
import random

plugin = crescent.Plugin()

async def request(ctx: crescent.Context, gateway: str, params: dict = None):
    url = "https://reddit.com/"
    await ctx.defer()
    async with aiohttp.ClientSession() as sess:
        async with sess.get(f"{url}{gateway}",
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                            params=params) as req:
            resp = await req.text()
        return json.loads(resp)

async def gallery(ctx: crescent.Context, gallery_data: dict):
    for p in gallery_data['media_metadata']:
        _id = p['id']
        _format = p['m'].split("/")[-1]
        await ctx.respond(f"https://i.reddit.com/{_id}.{_format}")

@plugin.include
@crescent.command(description="Fetches a random hot reddit femboy post")
async def femboy(ctx: crescent.Context):
    if not ctx.channel.is_nsfw:
        return await ctx.respond("horny 🫵", ephemeral=True)
    d = await request(ctx, "r/Femboys/hot.json")
    postlist = d['data']['children'][1:]
    post = random.choice(postlist)
    if "reddit.com/gallery/" in post['data']['url_overridden_by_dest']:
        return await gallery(ctx, post)
    await ctx.respond(post['data']['url_overridden_by_dest'])

@plugin.include
@crescent.command(description="Fetches a random hot reddit trap hentai post")
async def trap(ctx: crescent.Context):
    if not ctx.channel.is_nsfw:
        return await ctx.respond("horny 🫵", ephemeral=True)
    d = await request(ctx, "r/traphentai/hot.json")
    postlist = d['data']['children'][2:]
    post = random.choice(postlist)
    if "reddit.com/gallery/" in post['data']['url_overridden_by_dest']:
        return await gallery(ctx, post)
    await ctx.respond(post['data']['url_overridden_by_dest'])

@plugin.include
@crescent.command(description="Fetches a random hot reddit hentai post")
async def hentai(ctx: crescent.Context):
    if not ctx.channel.is_nsfw:
        return await ctx.respond("horny 🫵", ephemeral=True)
    d = await request(ctx, "r/hentai/hot.json")
    postlist = d['data']['children']
    post = random.choice(postlist)
    if "reddit.com/gallery/" in post['data']['url_overridden_by_dest']:
        return await gallery(ctx, post)
    await ctx.respond(post['data']['url_overridden_by_dest'])
