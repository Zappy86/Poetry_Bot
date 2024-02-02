import discord
from discord.ext import commands
import poetry_interface as pi
from logger import get_handler

description = "I've got over 10,000 poems'!"

def give_logger(arg1, arg2):
    global log, handler
    log = arg1
    handler=arg2

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents, description=description)

async def nonfatal_error(ctx):
    log.critical("There was an error!")
    await ctx.send("Something went wrong!\n\n(You should probably tell Dominic...)")
    return 0

async def not_found(ctx):
    await ctx.send("Sorry! I couldn't find what you were looking for. :/")
    return 0

async def send_message(ctx, message, split_character):
        
    if len(message) > 2000:
        current_chunk = []
        words = message.split(split_character)
        chunks = []
        for word in words:
            if len(split_character.join(current_chunk + [word])) <= 2000:
                current_chunk.append(word)
            else:
                chunks.append(split_character.join(current_chunk))
                current_chunk = [word]
        if current_chunk: chunks.append(split_character.join(current_chunk))
        for chunk in chunks:
                await ctx.send(chunk)
    else:
        await ctx.send(message)
    return 0

async def log_command(ctx, *args):
    if not args: args = ""
    log.info(f"@{ctx.author} invoked '{ctx.message.content}'{args}")
    return 0

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    # log.info(f"Logged in as {bot.user}!")

@bot.command()
async def title(ctx, title, poet=""):
    
    if poet:
        results = pi.get_poem_by_title(title, poet)
    else:
        results = pi.get_poem_by_title(title)
    
    if not results:
        await not_found(ctx)
        await log_command(ctx, " with no results")
        return
    
    message = f"{title}, by {results[0]}\n{results[1]}"
    
    await log_command(ctx)
    await send_message(ctx, message, "\n")

@bot.command()
async def search(ctx, search, num_of_poems = 10):
    results = pi.search_titles_for_string(str(search).lower(), int(num_of_poems))
    if not results[0]:
        await not_found(ctx)
        await log_command(ctx, " with no results")
        return

    if results[1] <= num_of_poems:
        message = f"Showing all results:\n"
    else:
        message = f"Showing {num_of_poems} of {results[1]}:"

    for title, poet in results[0]:
        message += f'\n- "{title}", by {poet}'

    await log_command(ctx)
    await send_message(ctx, message, "\n")

@bot.command()
async def tags(ctx):
    results = pi.list_tags()
    message = f"There are {len(results)} tags:\n\n"
    
    if not results:
        await nonfatal_error()
        return
    
    message + f"{results[0]}"
    for tag in results[1:]:
        message += f",{tag} "
        
    await log_command(ctx)
    await send_message(ctx, message, " ")
    
if __name__ == "__main__":
    import os
    print("\nPlease run 'main.py' to initialise bot!\n")