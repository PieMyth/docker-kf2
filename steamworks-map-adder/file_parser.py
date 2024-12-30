"""
The purpose of this file is to handle the reading and writing of the yaml file
to add steam workshop maps for the docker container
"""
import logging
import os
import yaml

import constants

class YamlReader:
    file_path:str = constants.Constants.default_file_path
    logger = logging.getLogger(__name__)

    def __init__(self, different_file_path = None):
        if different_file_path is not None:
            self.set_file_path(different_file_path)
     
    def set_file_path(self, different_file_path:str):
        """
        Allow to select where to store the file
        """
        self.file_path = different_file_path

    def read_file_if_available(self):
        parsed_yml = None
        if os.path.exists(self.file_path):
            self.logger.info("Found the file at %s", self.file_path)
            try:
                file_string = open(self.file_path, "r", encoding= "utf-8")
                parsed_yml = yaml.load(file_string.read(), Loader= yaml.Loader)
                if constants.Constants.custom_maps in parsed_yml:
                    custom_maps = list(map(lambda dictionary: dictionary[constants.Constants.name],
                        parsed_yml[constants.Constants.custom_maps]
                    ))
                    self.logger.info("Found %d keys", len(custom_maps))
                    self.logger.info("Maps found %s", sorted(custom_maps))
            except FileNotFoundError as file_error:
                self.logger.error("Error, file was not found %s", file_error)
            except Exception as error:
                self.logger.error("Error, general error when trying to read file %s", error)
        else:
            self.logger.debug("File not found at %s", self.file_path)
        return parsed_yml
