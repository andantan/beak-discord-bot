import os
import sys
import dotenv
import aiohttp

import discord

from discord import (
    Intents, 
    Interaction,
    app_commands as apc
)

from discord.ext import commands

from Config.Initialize.config import config_envs

from Error.exceptions import ConfigException

from Tools.printer import boot_issue
from Tools.converter import str2bool


try:
    dotenv.load_dotenv(verbose=True)

    config_envs()

    PATCH_MODE = str2bool(os.getenv("PATCH"))
    DEBUG_MODE = str2bool(os.getenv("DEBUG"))
    NORMAL_MODE = not(PATCH_MODE | DEBUG_MODE)

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

except ConfigException as ero:
    boot_issue(
        print_message = str(ero),
        log_message = None,
        sys_exit = True
    )

except Exception as ero:
    ero_msg: str = f"\
{ero}\n\
{ero.__module__ if hasattr(ero, '__module__') else ''}\n\
{ero.__class__.__name__}\
"
    import traceback

    print(traceback.format_exc())

    boot_issue(
        print_message = ero_msg,
        log_message = None,
        sys_exit = True
    )

    

@bot.event
async def on_ready() -> None:
    try:
        synced = await bot.tree.sync()
        await bot.change_presence(status=discord.Status.online)

        print(f"Synced {len(synced)} commands")

        if PATCH_MODE:
            await bot.change_presence(
                activity = discord.Game(
                name = f"서버 패치 및 업데이트"
                )
            )
        elif DEBUG_MODE:
            await bot.change_presence(
                activity = discord.Game(
                name = f"서버 점검"
                )
            )
        else:
            await bot.change_presence(
                activity = discord.Activity(
                    type = discord.ActivityType.listening,
                    name = f"{DEFAULT_COMMAND_PREFIX}도움"
                )
            )

    except Exception as ero:
        print(ero, ero.__module__, ero.__class__.__name__, sep="\n")

        sys.exit(-1)


@tree.command(name="play", description="유튜브 또는 유튜브 레드 주소로 음원을 재생합니다.")
@apc.describe(youtube_url = "유튜브 또는 유튜브 레드 주소")
async def beak_play(itc: Interaction, youtube_url: str) -> None:
    await itc.message.delete()


    await itc.response.send_message(youtube_url)


@tree.command(name="search", description="제목으로 검색하여 음원을 재생합니다.")
@apc.describe(title = "검색할 제목")
async def beak_search(itc: Interaction, title: str) -> None:
    await itc.response.send_message(title)

@tree.command(name="reset", description="플레이리스트를 초기화합니다.")
async def beak_reset(itc: Interaction) -> None:
    await itc.response.send_message(os.getenv("BEAK_IDENTIFICATION"))


@tree.command(name="stop", description="플레이리스트를 정지하고 봇을 퇴장시킵니다.")
async def beak_stop(itc: Interaction) -> None:
    await itc.response.send_message("stop")


if __name__ == "__main__":
    if _TOKEN := os.getenv("TOKEN"):
        try:
            bot.run(token=_TOKEN)
            ...
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
