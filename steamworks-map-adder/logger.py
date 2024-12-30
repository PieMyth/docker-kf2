"""
Class to configure the logger library
"""
import logging
import sys

class Logger:
    """
    Configure the logger library
    """
    def __init__(self):
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        handlers = [stdout_handler]

        logging.basicConfig(
            level=logging.DEBUG, 
            format='%(asctime)s: %(filename)s:%(lineno)d %(levelname)s - %(message)s',
            handlers=handlers
        )
