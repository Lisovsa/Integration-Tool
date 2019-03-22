import sys
import yaml
from argparse import ArgumentParser


class Config(object):
    """Config object constructor."""
    def __init__(self, config_dict):
        self.log_test = config_dict['log_test']
        self.tests = config_dict['suites_list']
        self.path = config_dict['test_suites_path']
        self.output_path = config_dict['output_path']
        self.console_redirect = config_dict['console_redirect']


def create_config(args):
    """Parses system arguments and creates config object"""
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration file in yml format, default value is "config.yml"',
                        default='config.yml')

    if not args or args == ['-h']:
        parser.print_help()
    args = parser.parse_args(args=args)

    # Loading configuration data from yml file, creating Config class object
    try:
        with open(args.config, 'r') as f:
            return Config(yaml.load(f))
    except yaml.YAMLError as e:
        sys.stderr.write('Failed to parse config file: {}'.format(e))
        return None
    except IOError as e:
        sys.stderr.write('Failed to open config file: {}'.format(e))
        return None
