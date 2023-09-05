import os
import sys
import logging
import aiohttp

import discord

from discord import Intents
from discord.ext import commands
from discord import Interaction
from discord import app_commands as apc


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

    except Exception as e:
        print(e)


@bot.tree.command(name="ping", description="send pong")
@apc.describe(param1 = "text1", param2 = "text2")
async def beak_ping(interaction: Interaction, param1: str, param2: str) -> None:
    await interaction.response.send_message(f"pong! {param1}-{param2}")


if __name__ == "__main__":
    from Config.Initialize.config import (config_args, config_envs)
    from Config.Initialize.vars import ArgumentsNamespace

    args: ArgumentsNamespace = config_args()
    
    config_envs(arguments=args)

    if _TOKEN := os.getenv("TOKEN"):
        try:
            bot.run(token=_TOKEN)
        
        except discord.LoginFailure as e:
            logging.fatal(msg=repr(e))

            print(f"\n{e.__doc__}\nSystem exited returns -1.")

            sys.exit(-1)

        except aiohttp.ClientConnectorError as e:
            logging.fatal(msg=f"{e.__class__.__name__}(\'{str(e)}\')")

            print("\nclient\'s internet connection is unstable.\nSystem exited returns -1.")

            sys.exit(-1)

        except Exception as e:
            print(e, e.__module__, e.__class__.__name__, sep="\n")

            sys.exit(-1)
    
    else:
        logging.fatal(msg=f"VariableMissing(\'Environment variable does not exist.\')")

        print("\nTOKEN variable does not exist in the .env file.\nSystem exited returns -1.")

        sys.exit(-1)
