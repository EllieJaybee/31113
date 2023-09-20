import crescent

async def is_mod(ctx: crescent.Context):
    if 939220579133845516 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission", ephemeral=True)
        return crescent.HookResult(exit=True)
    return crescent.HookResult()

async def is_member(ctx: crescent.Context):
    if 938700639771439157 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission", ephemeral=True)
        return crescent.HookResult(exit=True)
    return crescent.HookResult()

async def is_femboy(ctx: crescent.Context):
    if 965287802935853127 not in ctx.member.role_ids and ctx.member.id != 845942758421823488:
        await ctx.respond("You have no such permission", ephemeral=True)
        return crescent.HookResult(exit=True)
    return crescent.HookResult()