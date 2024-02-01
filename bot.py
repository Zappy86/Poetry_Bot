import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import logging
import poetry_interface as pi

load_dotenv()
token = getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents)

pi.initialize_dataframe("Poetry.csv")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    logging.info(f"Logged in as {bot.user}") # FIXME
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name =f"NOTHING, I AM THE BEST"))
    print(discord.__version__)

@bot.command()
async def title(ctx, title, poet=""):
    if poet:
        result = pi.get_poem_by_title(title, poet)
    else:
        result = pi.get_poem_by_title(title)
    
    if not result:
        await ctx.send("No poem with that title found.")
        return
    
    message = f"{title}, by {result[0]}\n{result[1]}"
    
    if len(message) > 4000:
        message = [message[i:i+1900] for i in range(0, len(message), 1900)]
    
        for x in message:
            await ctx.send(x)
    else:
        await ctx.send(message)



bot.run(token, log_handler=handler, log_level=logging.INFO) # This will end up in main.py, with "bot" being imported