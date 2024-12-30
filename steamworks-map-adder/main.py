"""
Steam Works map adder is intended to make it easier to add workshop maps
into the docker container by only needing to paste the steam link in and it will do the rest
"""
import logging

import file_parser
import logger
import steam_workshop_fetcher

logger.Logger()

class Main:
    """
    Main class for the map-adder tool
    """
    parser:file_parser.YamlReader
    logger = logging.getLogger(__name__)
    fetcher:steam_workshop_fetcher.FetchWorkshopInfo

    def __init__(self):
        self.parser = file_parser.YamlReader()
        self.fetcher = steam_workshop_fetcher.FetchWorkshopInfo()

    def run(self):
        self.logger.info("Starting the program")
        self.parser.read_file_if_available()
        keep_going = True
        new_maps = []
        while keep_going:
            url = input("Enter a url or exit by hitting enter: ")
            if len(url) != 0:
                result = self.fetcher.fetch_page(url)
                self.logger.info("Adding %s with steam id %d", result[0], result[1])
                new_maps.append(result)
            else:
                keep_going = False
        self.parser.write_file(new_maps=new_maps)

if __name__ == '__main__':
    main = Main()
    main.run()
