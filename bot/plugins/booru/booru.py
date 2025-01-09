import crescent
import hikari

import cunnypy

from bot.__main__ import Model

Plugin = crescent.Plugin[hikari.GatewayBot, Model]
plugin = Plugin()


@plugin.include
@crescent.command(
    name="booru",
    description="Search for images on booru sites!",
    default_member_permissions=hikari.Permissions.VIEW_CHANNEL,
)
class BooruCommand:
    tags = crescent.option(str, "The tags to search for.")
    rating = crescent.option(
        str,
        "The rating of the image",
        default="auto",
        choices=[("auto", "auto"), ("safe", "safe"), ("explicit", "explicit")],
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
        ],
    )

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
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
            if all(
                [plugin.model.secret.DANBOORU_LOGIN, plugin.model.secret.DANBOORU_KEY]
            )
            else None,
            "e6": None,
            "e9": None,
        }
        if ctx.channel.is_nsfw is False: 
            if self.rating == "explicit":
                return await ctx.respond("horny 🫵")
            elif self.rating == "auto":
                self.rating = "safe"
        else:
            if self.rating == "auto":
                self.rating = "explicit"
        tags_list = self.tags.split(" ")
        final_tags = str()
        for tag in tags_list:
            try:
                final_tags += (await cunnypy.autocomplete(self.booru, tag))[0].replace(
                    " ", "_"
                ) + " "
            except IndexError:
                return await ctx.respond(f'Tag "{tag}" not found.')
        if self.booru == "gb":
            final_tags += "sort:random "
        else:
            final_tags += "order:random "
        if self.booru == "db":
            final_tags += "age:<1year "
        if self.rating == "explicit" and not self.booru == "db":
            final_tags = final_tags.replace("loli", "")
            final_tags = final_tags.replace("shota", "")
            final_tags += "-loli -shota"
        try:
            post = await cunnypy.search(
                self.booru,
                final_tags,
                limit=10 if self.booru == "db" else 1,
                rating=self.rating,
                gatcha=True if self.booru == "db" else False,
                credentials=credential_dict[self.booru]
                if self.booru in ("gb", "db")
                else None,
            )
            await ctx.respond(post[0].file_url)
        except IndexError:
            return await ctx.respond("No results found.")
