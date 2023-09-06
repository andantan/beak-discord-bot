import os
import sys
import aiohttp

import discord

from discord import (
    Intents, 
    Interaction,
    app_commands as apc
)

from discord.ext import commands

from Config.Initialize.config import config_envs


config_envs()


if DEFAULT_COMMAND_PREFIX := os.getenv("DEFAULT_COMMAND_PREFIX"):
    bot = commands.Bot(
        command_prefix = DEFAULT_COMMAND_PREFIX,
        intents = Intents.all()
    )

    tree = bot.tree
else:
    boot_issue(
        print_message = f"VariableMissing(\'Environment variable does not exist.\')",
        log_message = "\DEFAULT_COMMAND_PREFIX variable does not exist in the .env file.\nSystem exited returns -1.",
        sys_exit = True
    )


@bot.event
async def on_ready() -> None:
    try:
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.online)

        print(f"Synced {len(synced)} commands")

    except Exception as ero:
        print(ero, ero.__module__, ero.__class__.__name__, sep="\n")

        sys.exit(-1)


@tree.command(name="ping", description="send pong")
@apc.describe(param1 = "text1", param2 = "text2")
async def beak_ping(interaction: Interaction, param1: str, param2: str) -> None:
    await interaction.response.send_message(f"pong! {param1}-{param2}")


if __name__ == "__main__":
    if _TOKEN := os.getenv("TOKEN"):
        from Tools.printer import boot_issue

        try:
            bot.run(token=_TOKEN)
        
        except discord.LoginFailure as ero:
            boot_issue(
                print_message = f"\n{ero.__doc__}\nSystem exited returns -1.",
                log_message = repr(ero),
                sys_exit = True
            )

        except aiohttp.ClientConnectorError as ero:
            boot_issue(
                print_message = "\nclient\'s internet connection is unstable.\nSystem exited returns -1.",
                log_message = f"{ero.__class__.__name__}(\'{str(ero)}\')",
                sys_exit = True
            )

        except Exception as ero:
            boot_issue(
                print_message = f"{ero}\n{ero.__class__.__name__}\n{ero.__module__}",
                log_message = None,
                sys_exit = True
            )

    else:
        boot_issue(
            print_message = f"VariableMissing(\'Environment variable does not exist.\')",
            log_message = "\nTOKEN variable does not exist in the .env file.\nSystem exited returns -1.",
            sys_exit = True
        )
