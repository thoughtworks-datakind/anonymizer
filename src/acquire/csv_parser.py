import pandas as pd


class CsvParser:

    def __init__(self, input_path, delimiter=','):
        self.input_path = input_path
        self.delimiter = delimiter

    def parse(self):
        df = pd.read_csv(self.input_path, self.delimiter)
        return df
