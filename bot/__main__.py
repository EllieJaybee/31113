from dataclasses import dataclass
import crescent
import hikari
import logging
import miru
from bot import secret


@dataclass
class Model:
    miru: miru.Client
    secret: secret


def main():
    intents = hikari.Intents.ALL
    bot = hikari.GatewayBot(secret.TOKEN, banner="bot", intents=intents)
    logger = logging.getLogger("hikari.gateway")
    miru_client = miru.Client(bot)
    crescent_client = crescent.Client(bot, Model(miru_client, secret))
    crescent_client.plugins.load_folder("bot.plugins.main")
    if bot.get_me().id == 937305077281071124:
        crescent_client.plugins.load_folder("bot.plugins.privileges")
    if all([secret.REDDIT_ID, secret.REDDIT_SECRET]):
        crescent_client.plugins.load_folder("bot.plugins.reddit")
        logger.info("Activated Reddit Module")
    else:
        logger.warning("Reddit Credentials empty, ignoring..")
    if secret.SAUCE_TOKEN:
        crescent_client.plugins.load_folder("bot.plugins.context")
        logger.info("Activated Saucenao Module")
    else:
        logger.warning("Saucenao credentials empty, ignoring..")
    bot.run()


if __name__ == "__main__":
    main()
