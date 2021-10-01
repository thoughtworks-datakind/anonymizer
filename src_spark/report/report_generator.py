from datetime import datetime
from enum import Enum
import os
import logging

import pandas as pd
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import Row
from src_spark.constants import LOCATION, REPORT_LEVEL


class ReportLevel(Enum):

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ReportGenerator():

    def __init__(self, config):
        self.report_file_location = config[LOCATION]
        self.report_level = config[REPORT_LEVEL]
        self.setup_logging_config()
        self.dataframe_is_empty = None

    def setup_logging_config(self):
        date = datetime.today().strftime("%Y%m%d")
        file_name = "{}/report_{}.log".format(self.report_file_location, date)
        if os.path.exists(file_name):
            mode = "a"
        else:
            if not os.path.exists(self.report_file_location):
                os.makedirs(self.report_file_location)
            mode = "x"
        file_handler = logging.FileHandler(filename=file_name, mode=mode)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().setLevel(logging.INFO)

    def __generate_high_level_report(self, results_df: DataFrame):
        columns = results_df.columns
        report_df = pd.DataFrame({"Columns with PII values" : columns})
        return report_df

    def __calculate_percentage(self, item_count, total_count):
        return round((item_count/total_count) * 100.0, 2)
    
    def _get_detector_results(self, row:Row, columns:list):
        new_row = []
        for index, cell in enumerate(row):
            current_col = columns[index]
            if cell != []:
                for analyzer_result in cell:
                    detector = analyzer_result["type"]
                    new_row.append(((current_col, detector), 1))
            else:
                new_row.append(((current_col, "no_pii"), 1))
        return new_row
        
    def __get_list_of_detectors(self, detector_results):
        report_detectors = []
        for key, _ in detector_results:
            detector = key[1]
            if detector not in report_detectors and detector != "no_pii":
                report_detectors.append(detector)
        return report_detectors

    def spark_generate_medium_level_report(self, results_df: DataFrame) -> pd.DataFrame:
        columns = results_df.columns
        detector_results = results_df.rdd.flatMap(lambda row: self._get_detector_results(row, columns)).reduceByKey(lambda acc, next: acc + next).collect()
        report_detectors = self.__get_list_of_detectors(detector_results)
        num_rows = results_df.count()
        pd_columns = []
        for column in columns:
            detection_stats = self.__get_detection_stats(column, report_detectors, detector_results, num_rows)
            pd_columns.append(pd.Series(data=detection_stats, index=report_detectors, name=column))
        report_df = pd.concat(pd_columns,axis=1).fillna(0)
        return report_df

    def __get_detection_stats(self, column: list, report_detectors: list, detector_results: list, num_rows: int) -> dict:
        detection_stats = {}
        default_value = ()
        for detector in report_detectors:
            column_detector_count = next(filter(lambda result: result[0] == (column, detector), detector_results), default_value)
            if len(column_detector_count) > 0:
                count = column_detector_count[1]
                percentage_value = self.__calculate_percentage(item_count=count, total_count=num_rows)
                detection_stats[detector] = (count, f"{percentage_value}%")
        return detection_stats
        

    def generate_report_content(self, results_df: DataFrame) -> pd.DataFrame:
        if self.report_level == ReportLevel.HIGH.value:
            return self.__generate_high_level_report(results_df)
        elif self.report_level == ReportLevel.MEDIUM.value:
            return self.spark_generate_medium_level_report(results_df)
        return self.spark_generate_medium_level_report(results_df)

    def __print(self, msg):
        formatted_msg = f"\n{msg}"
        print(formatted_msg)
        logging.info(formatted_msg)

    def __print_report(self, report):
        self.__print("\n\n****************************PII ANALYSIS REPORT**************************\n\n")
        if report.empty:
            self.__print("NO PII VALUES WERE FOUND!")
        else:
            self.__print(report)
        self.__print("\n\n****************************DONE!**************************\n\n")

    def generate(self, results_df: DataFrame):
        if self.is_empty_report_dataframe(results_df):
            print("NO PII VALUES WERE FOUND!")

        final_report = self.generate_report_content(results_df)
        self.__print_report(final_report)
        return final_report

    def is_empty_report_dataframe(self, results_df: DataFrame) -> bool:
        if self.dataframe_is_empty == None:
            self.dataframe_is_empty = results_df.rdd.flatMap(lambda row: self._row_is_empty_list(row)).reduce(lambda acc, item: acc and item)
        return self.dataframe_is_empty

    def _row_is_empty_list(self, row: Row) -> map:
        return map(lambda cell: True if cell == [] else False , row)


