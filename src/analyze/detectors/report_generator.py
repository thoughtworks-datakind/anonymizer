from enum import Enum

import pandas as pd


class ReportLevel(Enum):

    HIGH = 1
    MEDIUM = 2
    LOW = 3



class ReportGenerator():

    def __init__(self):
        pass

    def __generate_high_level_report(self, results_df):
        return results_df.columns.values

    def calculate_detector_counts_for_each_column(self, column_series):
        detector_map = {}
        for analyzer_result in column_series.iteritems():
            detector_type = analyzer_result[1].detector()
            if detector_type not in detector_map:
                detector_map[detector_type] = 1
            detector_map[detector_type] += 1
        return detector_map


    def __generate_medium_level_report(self, results_df):
        report_df = pd.DataFrame()
        for column in list(results_df):
            detector_counts_for_each_column = self.calculate_detector_counts_for_each_column(results_df[column])
            report_df[column] = pd.Series(detector_counts_for_each_column)
        return report_df

    def __generate_report_content(self, results_df, report_level):
        if report_level == ReportLevel.HIGH:
            return self.__generate_high_level_report(results_df)
        elif report_level == ReportLevel.MEDIUM:
            return self.__generate_medium_level_report(results_df)

    def generate(self, results_df, report_level=ReportLevel.HIGH):
        if results_df.empty:
            print("There are no PII values in the given input file")
            return results_df
        report = self.__generate_report_content(results_df, report_level)
        print(report)
        return report
