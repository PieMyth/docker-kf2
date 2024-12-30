"""
The purpose of this file is to handle the reading and writing of the yaml file
to add steam workshop maps for the docker container
"""
import copy
import hashlib
import json
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
        parsed_yml = self._get_parsed_yaml()
        if parsed_yml is not None:
            if constants.Constants.custom_maps in parsed_yml:
                custom_maps = list(map(lambda dictionary: dictionary[constants.Constants.name],
                    parsed_yml[constants.Constants.custom_maps]
                ))
                self.logger.info("Found %d keys", len(custom_maps))
                self.logger.info("Maps found %s", sorted(custom_maps))
        return parsed_yml

    def write_file(self, path = None, new_maps = list()):
        if path is not None:
            self.set_file_path(path)

        file_contents = self._get_parsed_yaml()
        new_file_contents = self._append_maps(copy.deepcopy(file_contents), new_maps)
        if new_file_contents is not None:
            self.logger.info("Change in map list. Creating/writing file")
            with open(self.file_path, "w", encoding="utf-8") as yml_file:
                yml_file.write(yaml.dump(new_file_contents, Dumper= yaml.Dumper))
        else:
            self.logger.info("Not updating file, should not be changed")

    def _get_parsed_yaml(self):
        parsed_yml = None
        if os.path.exists(self.file_path):
            self.logger.info("Found the file at %s", self.file_path)
            try:
                file_string = open(self.file_path, "r", encoding= "utf-8")
                parsed_yml = yaml.load(file_string.read(), Loader= yaml.Loader)
            except FileNotFoundError as file_error:
                self.logger.error("Error, file was not found %s", file_error)
            except Exception as error:
                self.logger.error("Error, general error when trying to read file %s", error)
        else:
            self.logger.debug("File not found at %s", self.file_path)
        return parsed_yml

    def _append_maps(self, file_contents, new_maps):
        new_contents = None
        if file_contents is not None and constants.Constants.custom_maps in file_contents:
            updated_list = False
            custom_map_ids = list(map(lambda dictionary: dictionary[constants.Constants.steam_id][0],
                copy.deepcopy(file_contents[constants.Constants.custom_maps])
            ))
            custom_maps = list(file_contents[constants.Constants.custom_maps])
            self.logger.info("Old list %s", custom_map_ids)
            for map_entry in new_maps:
                if map_entry[1] not in custom_map_ids:
                    self.logger.info("Adding new map to file")
                    custom_maps.append({
                        constants.Constants.name: map_entry[0],
                        constants.Constants.steam_id: [int(map_entry[1])]
                    })
                    updated_list = True
            self.logger.info("Current steam map ids: %s", custom_map_ids)
            self.logger.info("New list %s", custom_maps)
            if updated_list:
                new_contents = {
                    constants.Constants.custom_maps: custom_maps
                }
        else:
            self.logger.info("No previous file found! Adding all maps")
            custom_maps_entries = []
            for map_entry in new_maps:
                custom_maps_entries.append({
                    constants.Constants.name: map_entry[0],
                    constants.Constants.steam_id: [int(map_entry[1])]
                })
            new_contents = {
                constants.Constants.custom_maps: custom_maps_entries
            }
        return new_contents
