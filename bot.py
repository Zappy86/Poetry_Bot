import discord
from discord.ext import commands
import poetry_interface as pi

def prepare_attributes(arg1, arg2):
    global log, handler, description
    log = arg1
    handler=arg2

intents = discord.Intents.default()
intents.message_content = True
intents.guild_typing = False
intents.dm_typing = False

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents = intents, help_command=None, strip_after_prefix=True, 
case_insensitive=True, activity = discord.Game(name="!help"))

async def log_command(ctx, *args):
    if not args: args = ""
    log.info(f"'@{ctx.author}' invoked '{ctx.message.content}'{args} in '{ctx.channel}'")
    return 0

async def not_found(ctx):
    await log_command(ctx, " with no results")
    await ctx.send("```Sorry! I couldn't find what you were looking for. :/```")
    return 0

async def send_message(ctx, message, split_character = "\n"):
    '''Send messages wrapped in ``` in chunks small enough for discord'''
    
    if len(message) > 1993:
        working_chunk = []
        split = message.split(split_character)
        chunks = []
        for word in split:
            if len(split_character.join(working_chunk + [word])) <= 1990:
                working_chunk.append(word)
            else:
                chunks.append(split_character.join(working_chunk))
                working_chunk = [word]
        if working_chunk: chunks.append(split_character.join(working_chunk))
        for chunk in chunks:
                await ctx.send(f"```{chunk}```")
    else:
        await ctx.send(f"```{message}```")
    return 0

# Benefits of (semi-clean) code! I didn't have to redo everything to wrap "```" around all the messages!

@bot.event
async def on_command_error(ctx, error):
    log.error(f"'@{ctx.author}' invoked '{ctx.message.content}' in '{ctx.channel}' and it raised '{error}'")
    await ctx.send(f"```Sorry! There was an error: -> {str(error).removesuffix(".")} <-\nUse !help to see command usage```")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    log.info(f"Logged in as {bot.user}!")

@bot.command()
async def poem(ctx, title, poet=""):
    if poet:
        results = pi.get_poem_by_title(title, poet)
    else:
        results = pi.get_poem_by_title(title)
    
    if not results:
        await not_found(ctx)
        return
    
    message = f'"{title}", by {results[0]}\n{results[1]}'
    
    await log_command(ctx)
    await send_message(ctx, message)

@bot.command(name="exact-title")
async def exact_title(ctx, title):
    results = pi.get_all_poems_with_title(title)
    message = f"Poems that match '{title}':\n"
    
    if not results:
        await not_found(ctx)
        return
                
    for title, poet in results:
        message += f'\n- "{title}", by {poet}'
    
    await log_command(ctx)
    await send_message(ctx, message)

@bot.command()
async def search(ctx, search, num_of_poems = 10):
    results, num_found = pi.search_titles_for_string(str(search).lower(), int(num_of_poems))
    if not results:
        await not_found(ctx)
        return
    if num_found == 1:
        await log_command(ctx)
        await poem(ctx, results[0][0], results[0][1])
        return
    elif num_found <= num_of_poems:
        message = f"Showing **all** results for '{search}':\n"
    else:
        message = f"Showing **{num_of_poems}** of **{num_found}** results for '{search}':"

    for title, poet in results:
        message += f'\n- "{title}", by {poet}'

    await log_command(ctx)
    await send_message(ctx, message)

@bot.command(name="tags-list")
async def tags_list(ctx):
    results = pi.list_tags()
    message = f"There are **{len(results)}** tags:\n\n"
    
    message += f"{results[0]}"
    for tag in results[1:]:
        message += f", {tag}"
        
    await log_command(ctx)
    await send_message(ctx, message, " ")
    
@bot.command()
async def tags(ctx, title, poet=""):
    if poet:
        results = pi.get_tags_of_poem(title, poet)
    else:
        results = pi.get_tags_of_poem(title)
    
    if not results:
        await not_found(ctx)
        return
    
    message = f"{title} has {len(results)} tags:\n{results[0]}"
    for tag in results[1:]:
        message += f", {tag}"
    
    await log_command(ctx)
    await send_message(ctx, message)

@bot.command(name="poems-with-tag")
async def poems_with_tag(ctx, tag, num_of_poems = 10):
    results = pi.get_poems_with_tag(tag, num_of_poems)
    if not results:
        not_found()
        return
    
    message = "Poems with that tag:\n"
    
    for title, poet in results:
        message += f'\n- "{title}", by {poet}'
    
    await log_command(ctx)
    await send_message(ctx, message)

@bot.command()
async def poet(ctx, search : str, num_of_poems = 10):
    results, num_results = pi.get_poems_by_a_poet(search, num_of_poems)
    if not results:
        await not_found(ctx)
        return
    
    if len(results) == num_results:
        message = f"Showing all results:\n"
    else:
        message = f"Showing **{len(results)}** of **{num_results}** results:\n"
    
    for title in results:
        message += f'\n-"{title}", by {search.title()}'

    await log_command(ctx)
    await send_message(ctx, message)

@bot.command(name="num-of-tag")
async def num_of_tag(ctx, tag):
    result = pi.get_num_of_tag(tag.lower())
    
    if not result:
        await not_found()
        return
    
    await log_command(ctx)
    if result == 1:
        await ctx.send(f"1 poem has that tag.")
    else:
        await ctx.send(f"{result} poems have that tag.")

@bot.command()
async def random(ctx, number_of_poems = 1):
    results = pi.get_rand_poem(number_of_poems)

    if number_of_poems == 1:
        message = f"Here is a random poem:\n"
        for title, poet, poem in results:
            message += f'\n- "{title}", by {poet}\n\n{poem}'
    else:
        message = f"Here are {number_of_poems} random poems:"
        for index, item in enumerate(results):
            message += f'\n{index + 1}.) "{item[0]}", by {item[1]}'
            
        for index, item in enumerate(results):
            message += f'\n\n{index + 1}.) "{item[0]}", by {item[1]}\n{item[2]}'
    
    await log_command(ctx)
    await send_message(ctx, message)

@bot.command()
async def find(ctx, *, search : str):
    search = search[search.index('"') + 1:]
    search = search.split('", by ', 1)
    try:
        search[1] = search[1].strip('"')
        await poem(ctx, search[0], search[1])
    except:
        await ctx.send('''```Something went wrong, the format is:\n"Poem Title", by Poet\n\nDon't forget the comma!```''')

@bot.command()
async def help(ctx, *, arg : str = ""):
    description = "I'm a helpful bot for displaying and searching for poems, I know more than 10000 of them! :)"
    
    help_messages = {
        "search" : "Search titles for query: !search query [number of results]",
        "poem" : "Find the text of a poem: !poem title [poet]",
        "poet" : "Gets list of poet's poems: !poet poet [number of results]",
        "random" : "Gets a random number of poems: !random *[number of poems]",
        "find" : "Paste a title and author from the bot or search in the same format: !find *title-and-poet",
        "tags-list" : "Lists all of the tags: !tags-list",
        "tags" : "Get the tags of specified poem: !tags title [poet]",
        "poems-with-tag" : "Gets a list of poems with specified tag: !poems-with-tag tag [number of results]",
        "num-of-tag" : "Gets the number of poems with specified tag: !num-of-tag tag",
        "exact-title" : "Get a list of poems that match title exactly: !exact-title title"
    }
    if arg:
        if arg in help_messages:
            await ctx.send(f"```\nHelp message for '{arg}':\n{help_messages[arg]}\n```")
            await log_command(ctx)
        else:
            await ctx.send("```Command not found, say '!help' for a list of commands.```")
            log.info(f"'@{ctx.author}' invoked '{ctx.message.content}' in {ctx.channel} and it failed")
    else:
        message = (f"\n{description}\n\nParameters (except those with *) usually need to be wrapped in quotes, brackets specify an optional parameter.\n\n")
        for command in help_messages:
            message += f"{command} - {help_messages[command]}\n\n"
        await log_command(ctx)
        await send_message(ctx, message)


if __name__ == "__main__":
    import os
    print("\nPlease run 'main.py' to initialise bot!\n")
