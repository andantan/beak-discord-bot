import os
import sys
import logging
import aiohttp

import discord

from discord import (
    Intents, 
    Interaction,
    app_commands as apc
)

from discord.ext import commands


intents = Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready() -> None:
    try:
        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} commands")

    except Exception as ero:
        print(ero, ero.__module__, ero.__class__.__name__, sep="\n")

        sys.exit(-1)


@tree.command(name="ping", description="send pong")
@apc.describe(param1 = "text1", param2 = "text2")
async def beak_ping(interaction: Interaction, param1: str, param2: str) -> None:
    await interaction.response.send_message(f"pong! {param1}-{param2}")


if __name__ == "__main__":
    from Config.Initialize.config import config_envs
    
    config_envs()

    if _TOKEN := os.getenv("TOKEN"):
        try:
            bot.run(token=_TOKEN)
        
        except discord.LoginFailure as ero:
            logging.fatal(msg=repr(ero))

            print(f"\n{ero.__doc__}\nSystem exited returns -1.")

            sys.exit(-1)

        except aiohttp.ClientConnectorError as ero:
            logging.fatal(msg=f"{ero.__class__.__name__}(\'{str(ero)}\')")

            print("\nclient\'s internet connection is unstable.\nSystem exited returns -1.")

            sys.exit(-1)

        except Exception as ero:
            print(ero, ero.__module__, ero.__class__.__name__, sep="\n")

            sys.exit(-1)
    
    else:
        logging.fatal(msg=f"VariableMissing(\'Environment variable does not exist.\')")

        print("\nTOKEN variable does not exist in the .env file.\nSystem exited returns -1.")

        sys.exit(-1)
