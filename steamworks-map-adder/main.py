"""
Steam Works map adder is intended to make it easier to add workshop maps
into the docker container by only needing to paste the steam link in and it will do the rest
"""
import logging
import flask

import constants
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
    app = flask.Flask(__name__)

    def __init__(self):
        self.parser = file_parser.YamlReader()
        self.fetcher = steam_workshop_fetcher.FetchWorkshopInfo()

    @app.route("/")
    def home():
        parser = file_parser.YamlReader()
        maps_count = 0
        maps = parser.read_file_if_available()
        if maps is not None:
            maps = maps[constants.Constants.custom_maps]
            maps = sorted(maps, key=lambda d: d['name'])
            print(maps)
            maps_count = len(maps)
        print(maps)
        return flask.render_template('index.html', maps= maps, maps_count= maps_count)

    def run(self):
        self.logger.info("Starting the program")
        self.app.run(debug=True)

if __name__ == '__main__':
    main = Main()
    main.run()
