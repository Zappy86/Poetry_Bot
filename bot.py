import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import logging

load_dotenv()
token = getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name =f"NOTHING, I AM THE BEST"))
    print(discord.__version__)

bot.run(token, log_handler=handler, log_level=logging.INFO)