from dataclasses import dataclass
import crescent
import hikari
import miru
from bot import secret


@dataclass
class Model:
    miru: miru.Client
    secret: secret


def main():
    intents = hikari.Intents.ALL
    bot = hikari.GatewayBot(secret.TOKEN, banner="bot", intents=intents)
    miru_client = miru.Client(bot)
    crescent_client = crescent.Client(bot, Model(miru_client, secret))
    crescent_client.plugins.load_folder("bot.plugins.main")
    if all([secret.REDDIT_ID, secret.REDDIT_SECRET]):
        crescent_client.plugins.load_folder("bot.plugins.reddit")
    if secret.SAUCE_TOKEN:
        crescent_client.plugins.load_folder("bot.plugins.context")
    bot.run()


if __name__ == "__main__":
    main()
