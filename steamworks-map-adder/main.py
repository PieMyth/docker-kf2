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

def sort_maps(maps:dict):
    maps_count = 0
    if maps is not None:
        maps = maps[constants.Constants.custom_maps]
        maps = sorted(maps, key=lambda d: d['name'])
        maps_count = len(maps)
    # print(maps)
    return maps, maps_count

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
        maps, maps_count = sort_maps(parser.read_file_if_available())
        # print(maps)
        return flask.render_template('index.html', maps= maps, maps_count= maps_count)

    # Look at making this an arry of map values to allow adding multiple maps at once
    @app.route("/add_map", methods=['POST'])
    def add_map():
        # Get the url entered from the website
        map_url = flask.request.get_json().get("map_url", "")
        try:
            # Basic check to see if the steam workshop link is in the url somewhere
            if constants.Constants.steam_workshop_url in map_url:
                # Fetch the map name
                fetcher = steam_workshop_fetcher.FetchWorkshopInfo()
                result = fetcher.fetch_page(map_url)
                # Start the parser
                parser = file_parser.YamlReader()
                # Read current file
                parser.read_file_if_available()
                # Log that we are going to add the map with the following workshop id
                print("Adding %s with steam id %d", result[0], result[1])
                # Try to save the map change to the file
                parser.write_file(new_maps=[result])
            else:
                print("Not a steam workshop url")
                print("'" + map_url + "'")
                return "fail"
        except Exception as err:
            print("Ran into error")
            print(err)
            return "fail"
        return "success"

    def run(self):
        self.logger.info("Starting the program")
        self.app.run(debug=True)

if __name__ == '__main__':
    main = Main()
    main.run()
