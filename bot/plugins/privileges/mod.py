import crescent
import hikari
from typing_extensions import Annotated as atd

plugin = crescent.Plugin()

async def is_mod(ctx: crescent.Context):
    if 939220579133845516 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission")
        return crescent.HookResult(exit=True)
    return crescent.HookResult()

@plugin.include
@crescent.hook(is_mod)
@crescent.command(name="1984", description="Assert Dominance", guild=938699961112096768)
async def mute_1984(ctx: crescent.Context, member: atd[hikari.User, "Member to silence"]):
    await member.edit(
        mute=True,
        deaf=True,
        voice_channel=None
    )
    await member.add_role(939351651217735760)
    await member.remove_role(938700639771439157)
    await ctx.respond(f"✅ Locked {member.display_name} up", ephemeral=True)

@plugin.include
@crescent.hook(is_mod)
@crescent.command(description="Release prisoner", guild=938699961112096768)
async def free(ctx: crescent.Context, member: atd[hikari.User, "Prisoner to free"]):
    if 939351651217735760 not in member.role_ids:
        return await ctx.respond("He's not gulaged", ephemeral=True)
    await member.edit(
        mute=False,
        deaf=False
    )
    await member.remove_role(939351651217735760)
    await member.add_role()
    await ctx.respond(f"✅ Freed {member.display_name}", ephemeral=True)
