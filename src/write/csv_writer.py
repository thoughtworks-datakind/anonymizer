import pandas as pd
from pandas import DataFrame

from os import makedirs
from os.path import exists, dirname

from src.constants import OUTPUT_FILE_PATH, FILE_PATH


class CsvWriter:

    def __init__(self, config):
        self.__validate_config(config)
        self.output_path = config["anonymize"][OUTPUT_FILE_PATH]
        self.input_file_name = config["acquire"][FILE_PATH]

    def __validate_config(self, config):
        if "anonymize" not in config or not config["anonymize"] or OUTPUT_FILE_PATH not in config["anonymize"] or not config["anonymize"][OUTPUT_FILE_PATH]:
            raise ValueError("Config 'output_file_path' needs to be provided for parsing")

    def get_output_file_path(self):
        file_name = self.input_file_name.split('/')[-1]
        file_name_no_extension = file_name.split('.')[0]
        result = f"{self.output_path}/{file_name_no_extension}_anonymized_.csv"
        return result

    def write_csv(self, df: DataFrame):
        output_file_path = self.get_output_file_path()
        if not exists(dirname(output_file_path)):
            makedirs(dirname(output_file_path), exist_ok=True)

        df.to_csv(output_file_path, index=False)
        print("Anonymized csv has been successfully created!")