from pyspark.sql import SparkSession
from src_spark.constants import FILE_PATH
import pyspark.sql.functions as f

class CsvParser:

    def __init__(self, spark: SparkSession, config):
        self.__validate_config(config)
        self.input_path = config["file_path"]
        self.delimiter = config["delimiter"] if "delimiter" in config and config["delimiter"] else ","
        self.spark = spark

    def __validate_config(self, config):
        if FILE_PATH not in config or not config[FILE_PATH]:
            raise ValueError("Config 'file_path' needs to be provided for parsing")

    def parse(self):
        df = self.spark.read.load(
                            self.input_path,
                            format="csv",
                            sep=self.delimiter,
                            header="true",
                            inferSchema="true")
        
        

        return df