import crescent
import hikari
import miru
from bot.secret import TOKEN

def main():

    intents = hikari.Intents.ALL
    bot = hikari.GatewayBot(TOKEN, banner="bot", intents=intents)
    client = crescent.Client(bot)
    miru.install(bot)
    client.plugins.load_folder("bot.plugins")
    bot.run()

if __name__ == "__main__":
    main()