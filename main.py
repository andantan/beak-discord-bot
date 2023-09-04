import discord

from discord import Intents
from discord.ext import commands
from discord import Interaction
from discord import app_commands as apc

from manager import read_json

TOKEN = read_json().get("TOKEN")

intents = Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready() -> None:
    try:
        synced = await bot.tree.sync()
        print(synced)
        print(f"Synced {len(synced)} commands")

    except Exception as e:
        print(e)


@bot.tree.command(name="ping", description="send pong")
@apc.describe(param1 = "text1", param2 = "text2")
async def beak_ping(interaction: Interaction, param1: str, param2: str) -> None:
    await interaction.response.send_message(f"pong! {param1}-{param2}")


bot.run(token=TOKEN)