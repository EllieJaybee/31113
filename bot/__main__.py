from dataclasses import dataclass
import crescent
import hikari
import miru
from bot.secret import TOKEN


@dataclass
class Model:
    miru: miru.Client


def main():
    intents = hikari.Intents.ALL
    bot = hikari.GatewayBot(TOKEN, banner="bot", intents=intents)
    miru_client = miru.Client(bot)
    crescent_client = crescent.Client(bot, Model(miru_client))
    crescent_client.plugins.load_folder("bot.plugins")
    bot.run()


if __name__ == "__main__":
    main()
