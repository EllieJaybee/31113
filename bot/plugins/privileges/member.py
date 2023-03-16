import crescent
import hikari
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()

async def is_member(ctx: crescent.Context):
    if 938700639771439157 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission")
        return crescent.HookResult(exit=True)
    return crescent.HookResult()

@plugin.include
@crescent.hook(is_member)
@crescent.command(description="Get the event role")
async def event(ctx: crescent.Context):
    if 1085808035831746570 not in ctx.member.role_ids:
        await ctx.member.add_role(1085808035831746570)
        await ctx.respond("🍆 Added role `Event`")
    else:
        await ctx.member.remove_role(1085808035831746570)
        await ctx.respond("✂️ Removed role `Event`")