import crescent
from typing_extensions import Annotated as atd
import aiohttp
from bs4 import BeautifulSoup as bs
import urllib

from secret import TOKEN

bot = crescent.Bot(TOKEN, intents=crescent.Intents.ALL)

@bot.include
@crescent.command(description="Check connection to server")
async def ping(ctx: crescent.Context):
	await ctx.respond("pong")
	if ctx.channel.is_nsfw:
		await ctx.respond("also this channel sus")

async def request(params: dict = None):
		url = "https://www.google.com/search"
		async with aiohttp.ClientSession() as sess:
			async with sess.get(url,
								headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
								params=params) as req:
				resp = await req.text()
		return bs(resp, 'html.parser')

@bot.include
@crescent.command(description="Fetches the first google search result")
async def search(ctx: crescent.Context, *, query: atd[str, "Query to be searched"]):
	soup = await request(params={'q':query, 'safe':"off" if ctx.channel.is_nsfw else "strict"})
	soup = soup.find_all("div", class_="egMi0 kCrYT")
	for i in soup:
		if i.a is not None and i.a['href'].startswith("/url") and not 'scholar.google' in i.a['href']:
			return await ctx.respond(urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0])
	await ctx.respond(content="uguu sowwy owo can't find it uvu")

bot.run()