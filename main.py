def main():
    try:
        from bot import bot, prepare_attributes
        from os import getenv
        from dotenv import load_dotenv
        from logger import get_handler
        from logging import INFO
        from poetry_interface import initialize_dataframe

        load_dotenv()
        token = getenv('DISCORD_TOKEN')

        initialize_dataframe("Poetry.csv")

        log, handler = get_handler()
        prepare_attributes(log, handler)
        
        bot.run(token, log_handler=handler, log_level=INFO)
    except ModuleNotFoundError:
        print("You need to install the required modules with 'pip install -U -r requirements.txt'")
    except:
        print("Something went wrong...")


if __name__ == "__main__":
    main()