import crescent
import hikari

from bot.privilege import is_femboy

plugin = crescent.Plugin()


async def give_member(ctx: crescent.Context, member: hikari.Member):
    if 938700639771439157 in member.role_ids:
        return await ctx.respond(
            f"💀 {member.display_name} already has Member",
            mentions_everyone=False,
            role_mentions=False,
            user_mentions=False,
        )
    await member.add_role(938700639771439157)
    await ctx.respond(
        f"🍆 Given {member.display_name} Member",
        mentions_everyone=False,
        role_mentions=False,
        user_mentions=False,
    )
    log_channel: hikari.TextableChannel = ctx.guild.get_channel(939418125894553611)
    await log_channel.send(
        content=f"{ctx.member.mention} verified {member.mention} in {ctx.channel.mention}"
    )


@plugin.include
@crescent.hook(is_femboy)
@crescent.command(
    name="member", description="Grant Member role", guild=938699961112096768
)
class MemberSlash:
    member = crescent.option(hikari.User, "Person to be a member")
    async def callback(self, ctx: crescent.Context):
        await give_member(ctx, self.member)
