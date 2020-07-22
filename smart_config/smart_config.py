from yaml import safe_load as yaml_load
from toml import load as toml_load
from loguru import logger
import os
from pathlib import Path
from configparser import ConfigParser
from json import load as json_load, loads as json_loads


__version__ = "0.1.2"


class ConfigLoader:
    __version__ = __version__
    JSON_EXTENSION = [".json"]
    YAML_EXTENSION = [".yml", ".yaml"]
    CONFIG_EXTENSION = [".ini", ".cfg"]
    TOML_EXTENSION = [".toml"]
    SUPPORTED_FILES = (
        JSON_EXTENSION + YAML_EXTENSION + CONFIG_EXTENSION + TOML_EXTENSION
    )

    def __init__(self, file: str):
        """Create ConfigLoader class instance and read content from environment and files if they exists

        :param file: configuration file to load
        :return ConfigLoader: new instance of ConfigLoader
        """
        self.config = self.__check_and_process(file)

    def get_config(self):
        """
        gets loaded configuration

        :return: configuration dict
        """
        return self.config

    def __check_and_process(self, file: str):
        """
        loads the file and process

        :param file: file path
        :return: None
        :exception: Exception
        """
        data = None
        file_extension = Path(file).suffix
        if file_extension not in self.SUPPORTED_FILES:
            raise Exception(
                "Unsupported file format!. file format must be yaml, json, ini, toml & cfg"
            )
        else:
            file_stream = open(file)
            if file_extension in self.YAML_EXTENSION:
                data = yaml_load(file_stream)
            elif file_extension in self.TOML_EXTENSION:
                data = toml_load(open(file))
            elif file_extension in self.CONFIG_EXTENSION:
                config_parser = ConfigParser()
                config_parser.read_file(open(file))
                data = config_parser._sections
            elif file_extension in self.JSON_EXTENSION:
                data = json_load(open(file))

        if data:
            self.__process(data)
        return data

    def __process(self, items: dict):
        """
        processes the configuration

        :param items: configuration
        :return:None
        """
        for key in items:
            if isinstance(items[key], str):
                self.__extract_env(
                    items, key,
                )
            elif isinstance(items[key], dict):
                self.__process(items[key])

    def __extract_env(self, items: dict, key: str):
        """
        substitute the environment variable if found

        :param items: configuration
        :param key: key for which value needs to be substitute
        :return: None
        """
        value = items[key]
        if value.startswith("${") and value.endswith("}"):
            values = value[2:-1].split(":")
            if values.__len__() == 2:
                new_value = os.getenv(values[0], values[1])
            elif values.__len__() == 1:
                new_value = os.getenv(values[0], None)
                if not new_value:
                    logger.warning("Unable to find value in environment for key "+key)
            else:
                raise Exception("Invalid value format!")

            try:
                if new_value:
                    new_value = new_value.strip()
                    if new_value in ["True", "False"]:
                        new_value = new_value.lower()
                    new_value = json_loads(new_value)
            except Exception as e:
                logger.info(e)
            finally:
                items[key] = new_value

        elif value.startswith("${") or value.endswith("}"):
            raise Exception("Invalid value format!")
