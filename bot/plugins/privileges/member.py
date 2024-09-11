import crescent
import hikari

from bot.privilege import is_member

plugin = crescent.Plugin()


@plugin.include
@crescent.hook(is_member)
@crescent.command(name="roleicon", description="Change role icon", guild=938699961112096768, default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
class RoleIcon:
    icon = crescent.option(hikari.Attachment, "Icon to be applied to role")
    async def callback(self, ctx: crescent.Context):
        for role in ctx.member.get_roles():
            if role.colour != hikari.Colour.from_int(0):
                await plugin.app.rest.edit_role(ctx.guild, role, icon=self.icon)
                return await ctx.respond("🍆 Changed role icon!")
        await ctx.respond("🤨 Can't find custom role")


@plugin.include
@crescent.hook(is_member)
@crescent.command(
    name="roleicon-clear", description="Clear role icon", guild=938699961112096768, default_member_permissions=hikari.Permissions.VIEW_CHANNEL
)
async def roleicon_clear(ctx: crescent.Context):
    for role in ctx.member.get_roles():
        if role.colour != hikari.Colour.from_int(0):
            await plugin.app.rest.edit_role(ctx.guild, role, icon=None)
            return await ctx.respond("✂️ Cleared role icon!")
    await ctx.respond("🤨 Can't find custom role")


@plugin.include
@crescent.hook(is_member)
@crescent.message_command(name="Report Message", guild=938699961112096768, default_member_permissions=hikari.Permissions.VIEW_CHANNEL)
async def report_message(ctx: crescent.Context, message: hikari.Message):
    await ctx.respond(content="Report received", ephemeral=True)
    report_channel: hikari.GuildTextChannel = ctx.guild.get_channel(1140965929824567377)
    await report_channel.send(
        content=f"{ctx.member.mention} reported this message by {message.author.mention} {message.make_link(ctx.guild)}"
    )
