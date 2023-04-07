import crescent
import hikari
import miru
from bot.secret import TOKEN

def main():
    bot = hikari.GatewayBot(TOKEN, banner="bot")
    client = crescent.Client(bot)
    miru.install(bot)
    client.plugins.load_folder("bot.plugins")
    bot.run()

if __name__ == "__main__":
    main()