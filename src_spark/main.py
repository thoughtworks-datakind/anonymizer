import os
import sys
sys.path.append(os.path.abspath('.'))

import argparse
import json

from pyspark.sql import SparkSession
from src_spark.report.report_generator import ReportGenerator
from src_spark.acquire.csv_parser import CsvParser
from src_spark.analyze.detectors.pii_detector import PIIDetector
from src_spark.constants import ACQUIRE, REPORT
from src_spark.write.csv_writer import CsvWriter


class Main():

    def __init__(self, config_file_path):
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)

    #TODO : validate the config for the stages right here
    def run(self):
        spark = SparkSession.builder \
                                .master("local") \
                                .appName("PIIDetector") \
                                .getOrCreate()
        parsed_data_frame = CsvParser(spark, config=self.config[ACQUIRE]).parse()
        pii_analysis_report, redacted_data_frame = PIIDetector().analyze_data_frame(parsed_data_frame)
        
        report_generator = ReportGenerator(config=self.config[REPORT])
        if report_generator.is_empty_report_dataframe(pii_analysis_report):
            print("NO PII VALUES WERE FOUND!")
        else:
            report_generator.generate(results_df=pii_analysis_report)
        CsvWriter(spark, config=self.config).write_csv(df=redacted_data_frame)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', help='config file to run the tool')
    args = parser.parse_args()
    if not args.config_file:
        raise ValueError("Config file path should be provided for the tool to run.")
    return args

if __name__ == "__main__":
    args = get_args()
    Main(args.config_file).run()