def main():
    try:
        from bot import bot, pass_attributes, load_phrases
        from os import getenv
        from dotenv import load_dotenv
        from logger import get_handler
        from logging import INFO
        from poetry_interface import initialize_dataframe

        load_dotenv()
        token = getenv('DISCORD_TOKEN')

        initialize_dataframe("Poetry.csv")
        load_phrases()

        log, handler = get_handler()
        pass_attributes(log, handler)
        
        bot.run(token, log_handler=handler, log_level=INFO)
    except ModuleNotFoundError:
        print("You need to install the required modules with 'pip install -r requirements.txt'")


if __name__ == "__main__":
    main()