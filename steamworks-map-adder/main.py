"""
Steam Works map adder is intended to make it easier to add workshop maps
into the docker container by only needing to paste the steam link in and it will do the rest
"""
import logging

import file_parser
import logger

logger.Logger()

class Main:
    """
    Main class for the map-adder tool
    """
    parser:file_parser.YamlReader
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.parser = file_parser.YamlReader()

    def run(self):
        self.logger.info("Starting the program")
        self.parser.read_file_if_available()

if __name__ == '__main__':
    main = Main()
    main.run()
