import argparse
import json
from src.acquire.csv_parser import CsvParser
from src.analyze.detectors.pii_detector import PIIDetector
from src.constants import ACQUIRE


class DPFMain():

    def __init__(self, config_file_path):
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)

    #TODO : break this down
    def run(self):
        csv_parser = CsvParser(config=self.config[ACQUIRE])
        parsed_data_frame = csv_parser.parse()
        pii_detector = PIIDetector()
        pii_analysis_report = pii_detector.analyze(parsed_data_frame)
        print(str(pii_analysis_report))

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