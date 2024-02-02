def main():
    try:
        from bot import bot, give_logger
        from os import getenv
        from dotenv import load_dotenv
        from logger import get_handler
        from logging import INFO
        from poetry_interface import initialize_dataframe

        load_dotenv()
        token = getenv('DISCORD_TOKEN')

        log, handler = get_handler()
        give_logger(log, handler)
        
        initialize_dataframe("Poetry.csv")

        bot.run(token, log_handler=handler, log_level=INFO)
    except:
        print("Something went wrong...")
        
if __name__ == "__main__":
    main()