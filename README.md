# <div align="center"> <img src="https://prisonerexpress.org/wp-content/uploads/2016/09/Pe-Poetry-Icon.png" alt="drawing" width="75"/> A Simple Poetry Discord Bot <img src="https://prisonerexpress.org/wp-content/uploads/2016/09/Pe-Poetry-Icon.png" alt="drawing" width="75"/> </div>

The code may not be the cleanest, but at least I tried! As Teddy Roosevelt said, not in reference to art or code but regardless, the worst thing you can do is *nothing*.

This was my first real Python project too!

In the code is a csv file generously provided by *someone else*! The formatting was a little wonky, and I had to clean it up quite a bit, but that helped me learn how pandas worked, and I would've ended up slogging my way through learning it eventually anyways. Even still lots of the text of the poems themselves is all wrong, and it seems like sometimes new lines got smushed in with the one before, but there's not much I can do to fix it. Webscraping doesn't seem like a bad next project, so maybe I'll try scraping Poetry Foundation myself :)

This took quite a while (not that it was necessarily hard, but I'm still learning python, and lots of errors came up), probably a couple dozen hours (not counting the couple dozen I spent learning python in the first place), but ultimately it turned out about how I wanted.

I turned off intellisense, and tried to use AI as little as possible, so I think I actually learned a lot... at least about these libraries, but also about how to read documentation. Discord.py was tricky because there isn't a ton of it.

Maybe I should've used SQLite... when I started I was *not* in the mood to learn another programming language, but in the end I think figuring out pandas and re-formatting everything with that was probably just as tricky. Too late now!

## Setup
You probably shouldn't use this bot! But if you'd like to you certainly can!

These are instructions for *Windows*, and they're probably a little different on other operating systems.
1) Download the code, and make sure Python is installed
2) Use the [Discord Developer Portal](https://discord.com/developers/applications) to make a bot and get a token, and enable the Message Content Intent
3) Create a file named `.env` file after the example
4) For if you don't want to clutter python's modules, otherwise skip this:
    - With the code's directory open, run `python -m venv .venv`
    - Run `.venv\scripts\activate`
5) Run `pip install -r requirements.txt`
6) Run the main file with `py main.py`'
7) Invite the bot to a server at some point:
    - In the Developer Portal, OAuth2 > URL Generator, select bot
    - Enable "Read Messages/View Channels", "Send Messages", and "Send Messages in Threads"... or just admin
    - Invite the bot to a server you're an admin in

If you made the venv you have to start it up again so you have access to the modules every time in the future that you need to start up the bot.

## Commands
Parameters (except those with *) usually need to be wrapped in quotes, brackets specify an optional parameter.
| Command        | Description                                                   | Usage                                              |
| -------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| random         | Gets a random number of poems                                 | `!random *[number of poems]`                        |
| poem           | Find the text of a poem                                       | `!poem title [poet]`                             |
| find           | Paste a title and author or search in the same format         | `!find *title-and-poet`                             |
| exact-title    | Get a list of poems that match title exactly                  | `!exact-title title`                               |
| search         | Search titles for query                                       | `!search query [number of results]`             |
| tags-list      | Lists all of the tags                                         | `!tags-list`                                        |
| tags           | Get the tags of specified poem                                | `!tags title [poet]`                             |
| poems-with-tag | Gets a list of poems with specified tag                       | `!poems-with-tag tag [number of results]`       |
| poet           | Gets list of poet's poems                                      | `!poet poet [number of results]`                |
| num-of-tag     | Gets the number of poems with specified tag                   | `!num-of-tag tag`                                 |

(If you're sending one parameter with only one word, or using a command with only one parameter, you don't need quotes. There's a few more fun commands too, but they're not related to the function of the bot, just fun personal things for my server, use em or remove em if you'd like, they're at the bottom of `bot.py`.)


Thanks for looking at this, I had lots of fun making it and lost a week's worth of free time :)
