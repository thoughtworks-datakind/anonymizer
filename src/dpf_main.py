import argparse
import json

from src.report.report_generator import ReportGenerator, ReportLevel
from src.acquire.csv_parser import CsvParser
from src.analyze.detectors.pii_detector import PIIDetector
from src.constants import ACQUIRE


class DPFMain():

    def __init__(self, config_file_path):
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)

    def run(self):
        parsed_data_frame = CsvParser(config=self.config[ACQUIRE]).parse()
        pii_analysis_report = PIIDetector().analyze_data_frame(parsed_data_frame)
        generated_report = ReportGenerator().generate(results_df=pii_analysis_report,
                                                      report_level=ReportLevel.MEDIUM)
        print(generated_report)
        return generated_report

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', help='config file to run the tool')
    args = parser.parse_args()
    if not args.config_file:
        raise ValueError("Config file path should be provided for the tool to run.")
    return args

if __name__ == "__main__":
    args = get_args()
    DPFMain(args.config_file).run()