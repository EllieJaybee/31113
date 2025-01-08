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
        default="safe",
        choices=[("safe", "safe"), ("explicit", "explicit")],
    )

    async def callback(self, ctx: crescent.Context):
        await ctx.defer()
        if ctx.channel.is_nsfw is False and self.rating == "explicit":
            return await ctx.respond("horny 🫵")
        listtags = self.tags.split(" ")
        finaltags = str()
        for tag in listtags:
            try:
                finaltags += (await cunnypy.autocomplete("gel", tag))[0].replace(
                    " ", "_"
                ) + " "
            except IndexError:
                return ctx.respond(f'Tag "{tag}" not found.')
        finaltags += f"rating:{self.rating} sort:random "
        if self.rating == "explicit":
            finaltags = finaltags.replace("loli", "")
            finaltags = finaltags.replace("shota", "")
            finaltags += "-loli -shota"
        post = await cunnypy.search(
            "gelbooru",
            finaltags,
            limit=1,
            credentials={
                "user_id": plugin.model.secret.GELBOORU_ID,
                "api_key": plugin.model.secret.GELBOORU_KEY,
            },
        )
        await ctx.respond(post[0].file_url)
