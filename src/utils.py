import configparser
import os


def get_root_folder():
    return os.path.dirname(os.path.abspath(__file__))


def read_conf_file():
    config_file = 'config.cfg'
    # load all input params from config file
    config = configparser.ConfigParser()

    # reading config file
    config.read(config_file)

    return config
