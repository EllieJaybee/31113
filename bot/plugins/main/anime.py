from anime_api.apis import HmtaiAPI, NekosBest
from anime_api.apis.hmtai import ImageCategory
from anime_api.apis.nekos_best import ImageCategory as NekosCategory
import crescent
import hikari

plugin = crescent.Plugin()
hmtai = HmtaiAPI()
nekos = NekosBest()


async def action(
    ctx: crescent.Context, target: hikari.Member, category: ImageCategory.SFW, verb: str
):
    if target.id == ctx.member.id:
        targetname = "themselves"
    else:
        targetname = target.display_name
    if verb == "stared at":
        image = nekos.get_random_images(category)[0].url
    else:
        image = hmtai.get_random_image(category).url
    await ctx.respond(
        f"**{ctx.member.display_name} {verb} {targetname}!** [⠀]({image})",
        user_mentions=False,
        mentions_everyone=False,
        role_mentions=False,
    )


@plugin.include
@crescent.command(name="bite", description="Bite someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class BiteCommand:
    target = crescent.option(hikari.User, "Who do you want to bite?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.BITE, "bit")


@plugin.include
@crescent.command(name="boop", description="Boop someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class BoopCommand:
    target = crescent.option(hikari.User, "Who do you want to boop?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.BOOP, "booped")


@plugin.include
@crescent.command(name="bully", description="Bully someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class BullyCommand:
    target = crescent.option(hikari.User, "Who do you want to bully?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.THREATEN, "bullied")


@plugin.include
@crescent.command(name="cuddle", description="Cuddle someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class CuddleCommand:
    target = crescent.option(hikari.User, "Who do you want to cuddle?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.CUDDLE, "cuddled")


@plugin.include
@crescent.command(name="greet", description="Greet someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class WaveCommand:
    target = crescent.option(hikari.User, "Who do you want to greet?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.WAVE, "greeted")


@plugin.include
@crescent.command(name="handhold", description="Hold someone's hand!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class HoldCommand:
    target = crescent.option(hikari.User, "Who do you want to hold?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.HOLD, "held hands with")


@plugin.include
@crescent.command(name="hug", description="Hug someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class HugCommand:
    target = crescent.option(hikari.User, "Who do you want to hug?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.HUG, "hugged")


@plugin.include
@crescent.command(name="highfive", description="Highfive someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class FiveCommand:
    target = crescent.option(hikari.User, "Who do you want to highfive?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.FIVE, "highfived")


@plugin.include
@crescent.command(name="kill", description="Kill someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class KillCommand:
    target = crescent.option(hikari.User, "Who do you want to kill?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.KILL, "killed")


@plugin.include
@crescent.command(name="kiss", description="Kiss someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class KissCommand:
    target = crescent.option(hikari.User, "Who do you want to kiss?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.KISS, "kissed")


@plugin.include
@crescent.command(name="lick", description="Lick someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class LickCommand:
    target = crescent.option(hikari.User, "Who do you want to lick?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.LICK, "licked")


@plugin.include
@crescent.command(name="pat", description="Pat someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class PatCommand:
    target = crescent.option(hikari.User, "Who do you want to pat?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.PAT, "patted")


@plugin.include
@crescent.command(name="poke", description="Poke someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class PokeCommand:
    target = crescent.option(hikari.User, "Who do you want to poke?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.POKE, "poked")


@plugin.include
@crescent.command(name="punch", description="Punch someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class PunchCommand:
    target = crescent.option(hikari.User, "Who do you want to punch?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.PUNCH, "punched")


@plugin.include
@crescent.command(name="slap", description="Slap someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class SlapCommand:
    target = crescent.option(hikari.User, "Who do you want to slap?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.SLAP, "slapped")


@plugin.include
@crescent.command(name="stare", description="Stare at someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class StareCommand:
    target = crescent.option(hikari.User, "Who do you want to stare at?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, NekosCategory.STARE, "stared at")


@plugin.include
@crescent.command(name="tickle", description="Tickle someone!", default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class TickleCommand:
    target = crescent.option(hikari.User, "Who do you want to tickle?")

    async def callback(self, ctx: crescent.Context):
        await action(ctx, self.target, ImageCategory.SFW.TICKLE, "tickled")
