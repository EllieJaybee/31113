import crescent
import hikari
import random

plugin = crescent.Plugin()


@plugin.include
@crescent.command(description="Pick a random member", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
async def pickmember(ctx: crescent.Context):
    membersview = plugin.app.cache.get_members_view_for_guild(ctx.guild_id)
    await ctx.respond(
        random.choice(list(membersview.values())),
        mentions_everyone=False,
        role_mentions=False,
        user_mentions=False,
    )


@plugin.include
@crescent.command(name="rng", description="Generates a random number in a range", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class RNG:
    min = crescent.option(int, "Lowest number")
    max = crescent.option(int, "Highest number")
    async def callback(self, ctx: crescent.Context):
        await ctx.respond(random.randint(self.min, self.max))


@plugin.include
@crescent.command(name="pick", description="Pick randomly from a list of choices", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class Pick:
    choices = crescent.option(str, "Choices separated by commas")
    async def callback(self, ctx: crescent.Context):
        choice_list = self.choices.split(",")
        await ctx.respond(
            random.choice(choice_list),
            mentions_everyone=False,
            role_mentions=False,
            user_mentions=False,
        )
