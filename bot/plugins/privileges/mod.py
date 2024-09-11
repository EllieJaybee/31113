import crescent
import hikari

from bot.privilege import is_mod

plugin = crescent.Plugin()


@plugin.include
@crescent.hook(is_mod)
@crescent.command(name="1984", description="Assert Dominance", guild=938699961112096768, default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class Mute1984:
    member = crescent.option(hikari.User, "Member to silence")
    async def callback(self, ctx: crescent.Context):
        log_channel: hikari.TextableChannel = ctx.guild.get_channel(939418125894553611)
        member: hikari.Member = self.member
        await member.edit(mute=True, deaf=True)
        roles_removed = []
        for role_id in member.role_ids:
            roles_removed.append(ctx.guild.get_role(role_id).name)
            await member.remove_role(role_id)
        await log_channel.send(
            f"Removed `{', '.join(roles_removed)}` roles from {member.username}"
        )

        await member.add_role(939351651217735760)
        await ctx.respond(f"✅ Locked {member.display_name} up", ephemeral=True)


@plugin.include
@crescent.hook(is_mod)
@crescent.command(name="free", description="Release prisoner", guild=938699961112096768, default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class Free1984:
    member = crescent.option(hikari.User, "Prisoner to free")
    async def callback(self, ctx: crescent.Context):
        member: hikari.Member = self.member
        if 939351651217735760 not in member.role_ids:
            return await ctx.respond("They're not gulaged", ephemeral=True)
        await member.edit(mute=False, deaf=False)
        await member.remove_role(939351651217735760)
        await ctx.respond(
            f"✅ Freed {member.display_name} (Roles need to be manually given)",
            ephemeral=True,
        )
