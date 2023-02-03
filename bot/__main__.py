import crescent
import hikari
from bot.secret import TOKEN

client = hikari.GatewayBot(TOKEN)
bot = crescent.Client(client)
bot.plugins.load_folder("bot.plugins")
client.run()