import yaml

from config_validator.logging_schema import logging_schema
from config_validator.basic_builder import BasicRulesBuilder
from config_validator.basic_director import BasicRulesDirector


if __name__ == "__main__":

    config_file_name = 'example.yaml'
    config_file = open(config_file_name, 'r')
    config = yaml.load(config_file)

    director = BasicRulesDirector(logging_schema, BasicRulesBuilder())
    rules = director.build_rules_tree(config)
    if not rules.validate():
        for message in rules.get_all_errors():
            print message
