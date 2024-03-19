import crescent
import aiohttp
from bs4 import BeautifulSoup as bs
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()


@plugin.include
@crescent.command(description="Fetches status of a minecraft server")
async def mcserver(
    ctx: crescent.Context, ip: atd[str, "IP address of the minecraft server"]
):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(ip) as req:
            resp = await req.text()
    soup = bs(resp, "html.parser")
    root = soup.find_all("p")[1]
    br = root.find_all("br")
    status = root.span.text.strip()
    version = br[1].next_element.text.strip()
    players = br[-1].next_element.text.strip()
    msg = [status, version, players]
    res = "\n".join(msg)
    await ctx.respond(res)
