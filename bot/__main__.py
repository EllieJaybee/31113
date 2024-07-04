import argparse
from dataclasses import dataclass
import crescent
import hikari
import logging
import miru
from bot import secret

parser = argparse.ArgumentParser(description="Run 31113")
parser.add_argument("--debug", dest="debug", help="set log level to DEBUG", action="store_true")
args = parser.parse_args()


@dataclass
class Model:
    miru: miru.Client
    secret: secret


def main():
    intents = (
        hikari.Intents.ALL_UNPRIVILEGED |
        hikari.Intents.GUILD_MEMBERS    |
        hikari.Intents.MESSAGE_CONTENT
    )
    bot = hikari.GatewayBot(secret.TOKEN, banner="bot", intents=intents, force_color=True)
    logger = logging.getLogger("hikari.gateway")
    if args.debug:
        logger.setLevel("DEBUG")
    logger.info("Logger initialized")
    miru_client = miru.Client(bot)
    logger.info("Loaded Miru")
    crescent_client = crescent.Client(bot, Model(miru_client, secret))
    logger.info("Loaded Crescent")
    crescent_client.plugins.load_folder("bot.plugins.main")
    logger.info("Activated Main Modules")
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
