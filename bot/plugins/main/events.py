import crescent
import hikari
import logging

plugin = crescent.Plugin()
logger = logging.getLogger("hikari.gateway")


@plugin.include
@crescent.event
async def command_log(event: hikari.InteractionCreateEvent):
    interaction = event.interaction
    if interaction.type.value == 2:
        command_interaction: hikari.BaseCommandInteraction = interaction
        logger.debug(
            f"User {command_interaction.user.global_name}({command_interaction.user.id})"
            f" triggered {command_interaction.command_name}"
            f" in {command_interaction.get_channel() or "DM"}({command_interaction.channel_id})"
        )
    elif interaction.type.value == 3:
        component_interaction: hikari.ComponentInteraction = interaction
        if component_interaction.component_type == 2:
            logger.info(
                f"User {component_interaction.user.global_name}({component_interaction.user.id})"
                f" clicked button in {component_interaction.get_channel() or "DM"}"
                f"({component_interaction.channel_id})"
            )
    else:
        logger.debug(f"{interaction.type} triggered")


@plugin.include
@crescent.event
async def startup(event: hikari.GuildAvailableEvent):
    guild = event.get_guild()
    logger.debug(f"Connected to guild {guild.name}({guild.id})")
    for channel_id in guild.get_channels():
        channel = guild.get_channel(channel_id)
        logger.debug(f"L Connected to #{channel.name}({channel.id})")