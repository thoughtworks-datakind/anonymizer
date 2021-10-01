import pandas as pd

from src.constants import FILE_PATH


class CsvParser:

    def __init__(self, config):
        self.__validate_config(config)
        self.input_path = config["file_path"]
        self.delimiter = config["delimiter"] if "delimiter" in config and config["delimiter"] else ","

    def __validate_config(self, config):
        if FILE_PATH not in config or not config[FILE_PATH]:
            raise ValueError("Config 'file_path' needs to be provided for parsing")

    def parse(self):
        try:
            df = pd.read_csv(self.input_path, delimiter=self.delimiter)
        except pd.errors.EmptyDataError:
            return pd.DataFrame({})
        
        if df.isnull().values.any():
            raise ValueError("Dataframe contains NULL values")

        return df
