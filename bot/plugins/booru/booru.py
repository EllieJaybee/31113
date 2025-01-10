import crescent
import hikari

import cunnypy

from bot.__main__ import Model

Plugin = crescent.Plugin[hikari.GatewayBot, Model]
plugin = Plugin()

the_naughties = ("explicit", "questionable", "sensitive", "autoexplicit")
credential_dict = {
    "gb": {
        "user_id": plugin.model.secret.GELBOORU_ID,
        "api_key": plugin.model.secret.GELBOORU_KEY,
    }
    if all([plugin.model.secret.GELBOORU_ID, plugin.model.secret.GELBOORU_KEY])
    else None,
    "db": {
        "login": plugin.model.secret.DANBOORU_LOGIN,
        "api_key": plugin.model.secret.DANBOORU_KEY,
    }
    if all([plugin.model.secret.DANBOORU_LOGIN, plugin.model.secret.DANBOORU_KEY])
    else None,
    "e6": None,
    "e9": None,
    "r34": None,
}


@plugin.include
@crescent.command(
    name="booru",
    description="Search for images on booru sites!",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class BooruCommand:
    tags = crescent.option(
        str,
        "The tags to search for separated by comma. For example: thistle (dungeon meshi), 1boy",
    )
    rating = crescent.option(
        str,
        "The rating of the image",
        default="auto",
        choices=[
            ("auto", "auto"),
            ("safe", "safe"),
            ("explicit", "explicit"),
            ("questionable", "questionable"),
            ("sensitive", "sensitive"),
            ("general", "general"),
        ],
    )
    booru = crescent.option(
        str,
        "The booru site to search on.",
        default="gb",
        choices=[
            ("Gelbooru", "gb"),
            ("E621", "e6"),
            ("E926", "e9"),
            ("Danbooru", "db"),
            ("Rule34", "r34"),
        ],
    )

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        if ctx.channel.is_nsfw is False:
            if self.rating in the_naughties:
                return await ctx.respond("horny 🫵")
            elif self.rating == "auto":
                self.rating = "safe"
        else:
            if self.rating == "auto":
                self.rating = "autoexplicit"
        tags_list = [_.strip().replace(" ", "_") for _ in self.tags.split(",")]
        final_tags = str()
        for tag in tags_list:
            try:
                final_tags += (await cunnypy.autocomplete(self.booru, f"{tag}*"))[
                    0
                ].replace(" ", "_") + " "
            except IndexError:
                return await ctx.respond(f'Tag "{tag}" not found.')
        if self.booru == "gb":
            final_tags += "sort:random "
        elif self.booru == "r34":
            pass
        else:
            final_tags += "order:random "
        if self.booru == "db":
            final_tags += "age:<1year "
        if self.rating in the_naughties and self.booru in (
            "gb",
            "e6",
        ):
            final_tags = final_tags.replace("loli", "")
            final_tags = final_tags.replace("shota", "")
            final_tags += "-loli -shota"
        if self.rating == "autoexplicit":
            if self.booru == "gb":
                final_tags += "-rating:general "
                self.rating = None
            else:
                final_tags += "-rating:safe "
                self.rating = None
        try:
            post = await cunnypy.search(
                self.booru,
                final_tags,
                limit=10 if self.booru in ("db", "r34") else 1,
                rating=self.rating,
                gatcha=True if self.booru in ("db", "r34") else False,
                credentials=credential_dict[self.booru]
                if self.booru in ("gb", "db")
                else None,
            )
            await ctx.respond(post[0].file_url)
        except IndexError:
            return await ctx.respond("No results found.")
