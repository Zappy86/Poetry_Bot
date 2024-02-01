import logging

def get_handler():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    
    logger.addHandler(handler)
    
    return handler