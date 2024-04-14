import aiohttp
from bs4 import BeautifulSoup as bs
import crescent
import hikari
from typing_extensions import Annotated as atd
import urllib

plugin = crescent.Plugin()


async def request(ctx: crescent.Context, params: dict = None):
    url = "https://www.google.com/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            params=params,
        ) as response:
            response_text = await response.text()
        return bs(response_text, "html.parser")


async def _search(ctx: crescent.Context, query: str):
    soup = await request(
        ctx, params={"q": query, "safe": "off" if ctx.channel.is_nsfw else "strict"}
    )
    results = soup.find_all("div", class_="egMi0 kCrYT")
    for result in results:
        if (
            result.a is not None
            and result.a["href"].startswith("/url")
            and "scholar.google" not in result.a["href"]
        ):
            return await ctx.respond(
                urllib.parse.unquote(result.a["href"]).split("?q=")[1].split("&sa=")[0]
            )
    await ctx.respond(content="uguu sowwy owo can't find it uvu")


@plugin.include
@crescent.command(description="Fetches the first google search result")
async def search(ctx: crescent.Context, query: atd[str, "Query to be searched"]):
    await ctx.defer()
    await _search(ctx, query)


@plugin.include
@crescent.command(description="Answers your burning questions, powered by google")
async def answer(ctx: crescent.Context, query: atd[str, "Your question"]):
    await ctx.defer()
    soup = await request(ctx, params={"q": query})
    result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
    await ctx.respond(result.text)


@plugin.include
@crescent.command(description="Calculates stuff humanly, powered by google")
async def calculate(ctx: crescent.Context, query: atd[str, "Your math question"]):
    await ctx.defer()
    soup = await request(ctx, params={"q": query})
    question = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
    if not question:
        await ctx.respond("Calculation invalid, reverting to a search...")
        return await _search(ctx, query)
    question = question.text
    answer = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
    embed = hikari.Embed(description=f"```\n{question}\n{answer}\n```")
    await ctx.respond(embed=embed)


@plugin.include
@crescent.command(description="Defines a word or phrase queried, powered by google")
async def define(ctx: crescent.Context, query: atd[str, "Phrase to be defined"]):
    await ctx.defer()
    soup = await request(ctx, params={"q": f"define {query}"})
    root = soup.find_all("div", class_="kCrYT")
    root2 = root[1].find("div", class_="Ap5OSd")
    if not root2:
        await ctx.respond("Phrase invalid, reverting to a search...")
        return await _search(ctx, query)
    root2 = root2.contents
    phrase = root[0].span.h3.text
    pronounciation = root[0].contents[1].text
    type = root2[0].text.strip()
    apsos = root[1].div.find_all("div", class_="Ap5OSd")[1]
    try:
        meaning = apsos.ol.li.div.div.text
    except AttributeError:
        meaning = apsos.div.div.div.text
    e = hikari.Embed(title=phrase, description=meaning).add_field(
        name=type, value=f"({pronounciation})"
    )
    await ctx.respond(embed=e)


@plugin.include
@crescent.command(description="Gives a weather forecast for query, powered by google")
async def weather(ctx: crescent.Context, query: atd[str, "Location/time query"]):
    await ctx.defer()
    soup = await request(ctx, params={"q": f"weather {query}"})
    main_weather = soup.find("div", class_="BNeawe tAd8D AP7Wnd")
    if not main_weather:
        await ctx.respond("Query invalid, reverting to a search...")
        return await _search(ctx, query)
    main_weather = main_weather.text
    supplementary_temperature = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
    response = f"{main_weather} {supplementary_temperature}"
    await ctx.respond(response)


@plugin.include
@crescent.command(description="Fetches the first (lowres) image of the query on google")
async def image(ctx: crescent.Context, query: atd[str, "Image to search for"]):
    await ctx.defer()
    soup = await request(
        ctx,
        params={
            "q": query,
            "safe": "off" if ctx.channel.is_nsfw else "strict",
            "tbm": "isch",
        },
    )
    root = soup.find("div", class_="kCmkOe")
    if not root:
        await ctx.respond("Image query invalid, reverting to a search...")
        return await _search(ctx, query)
    link = root.parent["href"]
    url = urllib.parse.unquote(link).split("?q=")[1].split("&sa=")[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        ) as response:
            response_soup = bs(await response.text(), "html.parser")
    image_element = response_soup.find(property="og:image")
    if image_element:
        image_link = image_element["content"]
    else:
        image_link = root.img["src"]
    embed = hikari.Embed(
        title="Jump to result!",
        url=urllib.parse.unquote(link).split("?q=")[1].split("&sa=")[0],
    )
    embed.set_image(image_link)
    await ctx.respond(embed=embed)
