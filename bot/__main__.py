import crescent
import hikari
import miru
from bot.secret import TOKEN

client = hikari.GatewayBot(TOKEN, banner="bot")
bot = crescent.Client(client)
miru.install(client)
bot.plugins.load_folder("bot.plugins")
client.run()