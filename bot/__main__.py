import crescent
from bot.secret import TOKEN

bot = crescent.Bot(TOKEN, intents=crescent.Intents.ALL, banner=None)
bot.plugins.load_folder("bot.plugins")
bot.run()