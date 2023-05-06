import crescent
import hikari
from typing_extensions import Annotated as atd

from bot.privilege import is_femboy

plugin = crescent.Plugin()

async def give_member(ctx: crescent.Context, member: hikari.Member):
    if 938700639771439157 in member.role_ids:
        return await ctx.respond(f"💀 {member.display_name} already has Member", mentions_everyone=False, role_mentions=False, user_mentions=False)
    await member.add_role(938700639771439157)
    await ctx.respond(f"🍆 Given {member.display_name} Member", mentions_everyone=False, role_mentions=False, user_mentions=False)

@plugin.include
@crescent.hook(is_femboy)
@crescent.command(name="member" ,description="Grant Member role", guild=938699961112096768)
async def member_slash(ctx: crescent.Context, member: atd[hikari.User, "Person to be a member"]):
    await give_member(ctx, member)

# @plugin.include
# @crescent.hook(is_femboy)
# @crescent.message_command(name="Grant Member role")
# async def member_message(ctx: crescent.Context, message: hikari.Message):
#     await give_member(ctx, message.member)