import crescent
import hikari
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()

async def is_femboy(ctx: crescent.Context):
    if 965287802935853127 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission")
        return crescent.HookResult(exit=True)
    return crescent.HookResult()

@plugin.include
@crescent.hook(is_femboy)
@crescent.command(description="Grant Member role")
async def member(ctx: crescent.Context, member: atd[hikari.User, "Person to be a member"]):
    await member.add_role(938700639771439157)
    await ctx.respond(f"🍆 Given {member.display_name} Member", mentions_everyone=False, role_mentions=False, user_mentions=False)
