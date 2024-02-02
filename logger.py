import logging

def get_handler():
    logger = logging.getLogger('Poetry_Bot')
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    
    logger.addHandler(handler)
    
    return logger, handler