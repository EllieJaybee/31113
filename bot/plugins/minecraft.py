import crescent
from difflib import get_close_matches as correct
import hikari
import aiohttp
from bs4 import BeautifulSoup as bs
from pyjsparser import parse
import requests
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()
categories = []
items = []

r = requests.get("https://www.minecraft-crafting.net/app/output/output.js")
js = parse(r.text)
for types in js['body'][0]['declarations'][0]['init']['elements']:
    categories.append(types['properties'][0]['key']['value'])
    for thing in types['properties'][0]['value']['elements']:
        items.append(thing['value'])

async def rec(item):
    for category in categories:
        if requests.get('https://www.minecraft-crafting.net/app/src/{0}/craft/craft_{1}.gif'.format(category, item)).status_code == 200:
            return 'https://www.minecraft-crafting.net/app/src/{0}/craft/craft_{1}.gif'.format(category, item)
        elif requests.get('https://www.minecraft-crafting.net/app/src/{0}/craft/craft_{1}.png'.format(category, item)).status_code == 200:
            return 'https://www.minecraft-crafting.net/app/src/{0}/craft/craft_{1}.png'.format(category, item)
    return None

async def recipe_autocomplete(
    ctx: crescent.Context,
    option: hikari.AutocompleteInteractionOption
    ) -> 'list[hikari.CommandChoice]':
    assert isinstance(option.value, str)
    choices = []
    correction = correct(option.value, items, 5, 0.4)
    for thing in correction:
        choices.append(hikari.CommandChoice(name=thing, value=''.join(thing).lower()))
    return choices

@plugin.include
@crescent.command(description="Fetches minecraft recipes")
async def recipe(
    ctx: crescent.Context,
    query: atd[str, "Recipe to search", crescent.Autocomplete(recipe_autocomplete)]):
    url = await rec(query)
    await ctx.respond(url)

@plugin.include
@crescent.command(description="Fetches status of redwell's server")
async def mcserver(ctx: crescent.Context):
    async with aiohttp.ClientSession() as sess:
        async with sess.get("https://llewder.lol") as req:
            resp = await req.text()
            soup = bs(resp, 'html.parser')
            root = soup.find_all('p')[1]
            br = root.find_all('br')
            status = root.span.text.strip()
            version = br[1].next_element.text.strip()
            players = br[-1].next_element.text.strip()
            msg = [status, version, players]
            res = '\n'.join(msg)
            await ctx.respond(res)