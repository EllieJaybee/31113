import aiohttp
from bs4 import BeautifulSoup as bs
from bs4 import Tag
import crescent
import hikari

import json
import urllib

plugin = crescent.Plugin()


async def request(params: dict = None) -> bs:
    url = "https://www.google.com/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={"User-Agent": "w3m/0.5.3+git20230121"},
            params=params,
        ) as response:
            response_text = await response.text()
        return bs(response_text, "html.parser")


async def _search(ctx: crescent.Context, query: str) -> hikari.Message | None:
    soup = await request(
        params={"q": query, "safe": "off" if ctx.channel.is_nsfw else "strict"}
    )
    results = soup.find_all("a", class_="fuLhoc ZWRArf")
    for result in results:
        if (
            result is not None
            and result["href"].startswith("/url")
            and "scholar.google" not in result["href"]
        ):
            return await ctx.respond(
                urllib.parse.unquote(result["href"]).split("?q=")[1].split("&sa=")[0]
            )
    await ctx.respond(content="No results found :c")


@plugin.include
@crescent.command(
    name="search",
    description="Fetches the first google search result",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Search:
    query = crescent.option(str, "Query to be searched")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        await _search(ctx, self.query)


@plugin.include
@crescent.command(
    name="answer",
    description="Answers your burning questions, powered by google",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Answer:
    query = crescent.option(str, "Your question")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        soup = await request(params={"q": self.query})
        result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
        await ctx.respond(result.text)


@plugin.include
@crescent.command(
    name="calculate",
    description="Calculates stuff humanly, powered by google",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Calculate:
    query = crescent.option(str, "Your math question")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        soup = await request(params={"q": f"calculate {self.query}"})
        question = soup.find("span", class_="F9iS2e")
        if not question:
            await ctx.respond("Calculation invalid, reverting to a search...")
            return await _search(ctx, self.query)
        question = question.text
        answer = soup.find("span", class_="qXLe6d epoveb").text
        embed = hikari.Embed(description=f"```\n{question}\n{answer}\n```")
        await ctx.respond(embed=embed)


@plugin.include
@crescent.command(
    name="define",
    description="Defines a word or phrase queried, powered by google",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Define:
    query = crescent.option(str, "Phrase to be defined")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        soup = await request(params={"q": f"define {self.query}"})
        phrase = soup.find("span", class_="qXLe6d x3G5ab").text
        pronounciation = soup.find("span", class_="qXLe6d F9iS2e").text
        type = soup.find("span", class_="qXLe6d FrIlee").text
        try:
            apsos = soup.find_all("div", class_="CSfvHb")[1]
        except IndexError:
            await ctx.respond("Phrase invalid, reverting to a search...")
            return await _search(ctx, self.query)
        try:
            meaning = apsos.ol.li.span.span.text
        except AttributeError:
            meaning = apsos.div.span.span.text
        e = hikari.Embed(title=phrase, description=meaning).add_field(
            name=type, value=f"({pronounciation})"
        )
        await ctx.respond(embed=e)


@plugin.include
@crescent.command(
    name="weather",
    description="Gives a weather forecast for query, powered by google",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Weather:
    query = crescent.option(str, "Location/time query")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        soup = await request(params={"q": f"weather {self.query}"})
        main_weather = soup.find("span", class_="qXLe6d F9iS2e")
        if not main_weather:
            await ctx.respond("Query invalid, reverting to a search...")
            return await _search(ctx, self.query)
        main_weather = main_weather.text
        supplementary_temperature = soup.find("span", class_="qXLe6d epoveb").text
        response = f"{main_weather} {supplementary_temperature}"
        await ctx.respond(response)


async def traverse(element: Tag) -> Tag:
    if any(
        [
            _
            in urllib.parse.unquote(element.div.div.div.div.table.tr.td.a["href"])
            .split("?q=")[1]
            .split("&sa=")[0]
            for _ in ["facebook.com", "tiktok.com"]
        ]
    ):
        if not element.next_sibling:
            if not element.parent.next_sibling:
                return None
            return await traverse(element.parent.next_sibling.td)
        return await traverse(element.next_sibling)
    else:
        return element.div.div.div.div.table.tr.td.a.div


async def find_hires(url: str) -> dict | Tag:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{url}{'.json' if 'reddit.com' in url else ''}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        ) as response:
            response_text = await response.text()
            if "reddit.com" in url:
                return json.loads(response_text)[0]["data"]["children"][0]["data"]
            return bs(response_text, "html.parser")


async def get_hires_reddit_link(response: dict) -> str:
    main_image = response["url_overridden_by_dest"]
    if "https://i.redd.it" in main_image:
        return main_image
    else:
        first_image = list(response["media_metadata"].keys())[0]
        return f"https://i.redd.it/{first_image}.{response['media_metadata'][first_image]['m'].replace('image/', '')}"


async def get_hires_other_link(response: bs) -> str | None:
    if response.find(property="og:image"):
        return response.find(property="og:image")["content"]
    elif response.find(string="twitter:image"):
        return response.find(string="twitter:image").parent["content"]
    else:
        return None


async def get_hires_link(response: dict | bs) -> str | None:
    if isinstance(response, dict):
        return await get_hires_reddit_link(response)
    else:
        return await get_hires_other_link(response)


@plugin.include
@crescent.command(
    name="image",
    description="Fetches the first (lowres) image of the query on google",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class Image:
    query = crescent.option(str, "Image to search for")

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        soup = await request(
            params={
                "q": self.query,
                "safe": "off" if ctx.channel.is_nsfw else "strict",
                "tbm": "isch",
            }
        )
        root = await traverse(soup.find("td", class_="e3goi"))
        if not root:
            await ctx.respond("Image query invalid, reverting to a search...")
            return await _search(ctx, self.query)
        link = root.parent["href"]
        url: str = urllib.parse.unquote(link).split("?q=")[1].split("&sa=")[0]
        response = await find_hires(url)
        image_link = await get_hires_link(response)
        if not image_link:
            image_link = root.img["src"]
        embed = hikari.Embed(
            title="Jump to result!",
            url=urllib.parse.unquote(link).split("?q=")[1].split("&sa=")[0],
        )
        embed.set_image(image_link)
        await ctx.respond(embed=embed)
