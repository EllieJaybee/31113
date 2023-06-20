import crescent
import hikari
from typing_extensions import Annotated as atd

from bot.privilege import is_mod

plugin = crescent.Plugin()

@plugin.include
@crescent.hook(is_mod)
@crescent.command(name="1984", description="Assert Dominance", guild=938699961112096768)
async def mute_1984(ctx: crescent.Context, member: atd[hikari.User, "Member to silence"]):
    await member.edit(
        mute=True,
        deaf=True
    )
    await member.add_role(939351651217735760)
    await member.remove_role(938700639771439157)
    await member.remove_role(965287802935853127)
    await member.remove_role(939494839077204018)
    await ctx.respond(f"✅ Locked {member.display_name} up", ephemeral=True)

@plugin.include
@crescent.hook(is_mod)
@crescent.command(description="Release prisoner", guild=938699961112096768)
async def free(ctx: crescent.Context, member: atd[hikari.User, "Prisoner to free"]):
    if 939351651217735760 not in member.role_ids:
        return await ctx.respond("They're not gulaged", ephemeral=True)
    await member.edit(
        mute=False,
        deaf=False
    )
    await member.remove_role(939351651217735760)
    await ctx.respond(f"✅ Freed {member.display_name} (Member, Big boy and Femboy role needs to be manually given)", ephemeral=True)
