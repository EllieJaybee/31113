import discord
from discord.ext import commands

import aiohttp
from bs4 import BeautifulSoup as bs
import urllib

from secret import TOKEN

bot = commands.Bot(command_prefix="ok google, ",
					help_command=None,
					allowed_mentions=None,
					case_insensitive=True,
					intents=discord.Intents.all())

async def request(params: dict = None):
		url = "https://www.google.com/search"
		async with aiohttp.ClientSession() as sess:
			async with sess.get(url,
								headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
								params=params) as req:
				resp = await req.text()
		return bs(resp, 'html.parser')

@bot.event
async def on_ready():
	print("ready!")

@bot.command(name="search")
async def search(ctx, *, query: str):
	soup = await request(params={'q':query, 'safe':"off" if ctx.channel.is_nsfw() else "strict"})
	soup = soup.find_all("div", class_="egMi0 kCrYT")
	for i in soup:
		if i.a is not None and i.a['href'].startswith("/url") and not 'scholar.google' in i.a['href']:
			return await ctx.send(urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0])
	await ctx.send(content="uguu sowwy owo can't find it uvu")

bot.run(TOKEN)