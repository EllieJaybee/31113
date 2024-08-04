import crescent
import random

plugin = crescent.Plugin()


@plugin.include
@crescent.command(description="Pick a random member")
async def pickmember(ctx: crescent.Context):
    membersview = plugin.app.cache.get_members_view_for_guild(ctx.guild_id)
    await ctx.respond(
        random.choice(list(membersview.values())),
        mentions_everyone=False,
        role_mentions=False,
        user_mentions=False,
    )


@plugin.include
@crescent.command(name="rng", description="Generates a random number in a range")
class RNG:
    min = crescent.option(int, "Lowest number")
    max = crescent.option(int, "Highest number")
    async def callback(self, ctx: crescent.Context):
        await ctx.respond(random.randint(self.min, self.max))


@plugin.include
@crescent.command(name="pick", description="Pick randomly from a list of choices")
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
