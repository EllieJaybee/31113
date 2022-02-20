import lightbulb
import google_utils

from secret import TOKEN

bot = lightbulb.BotApp(token=TOKEN,
						prefix="ok google,",
						help_class=None,
						case_insensitive_prefix_commands=True)

@bot.command
@lightbulb.option("query",
					description="what you wanna search",
					type=str,
					required=True,
					modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("search", "Returns google results")
@lightbulb.implements(lightbulb.PrefixCommand)
async def search(ctx: lightbulb.Context):
	g = google_utils.Google.search(ctx.options.query, is_safe=(not ctx.get_channel().is_nsfw))
	await ctx.respond(g[0].link)

bot.run()