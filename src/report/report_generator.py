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

    def __collate_all_detectors_per_cell(self, analyzer_result):
        return [result.detector() for result in analyzer_result[1]]

    #TODO : filter out the NAs before passing through this
    def calculate_detector_counts_for_each_column(self, column_series):
        detector_map = {}
        for analyzer_results in column_series.iteritems():
            if not analyzer_results:
                continue
            detector_types = self.__collate_all_detectors_per_cell(analyzer_results)
            for detector_type in detector_types:
                if detector_type not in detector_map:
                    detector_map[detector_type] = 0
                detector_map[detector_type] += 1
        return detector_map

    def __generate_medium_level_report(self, results_df):
        report_df = pd.DataFrame({})
        columns = list(results_df)
        column_reports = []
        for column in columns:
            detector_counts_for_each_column = self.calculate_detector_counts_for_each_column(results_df[column])
            column_report = pd.Series(detector_counts_for_each_column, name=column, index=detector_counts_for_each_column.keys())
            if not column_report.empty:
                column_reports.append(column_report)
        if column_reports:
            report_df = pd.concat(column_reports, axis=1, keys=[series.name for series in column_reports], sort=True)
        return report_df

    def __generate_report_content(self, results_df, report_level):
        if report_level == ReportLevel.HIGH:
            return self.__generate_high_level_report(results_df)
        elif report_level == ReportLevel.MEDIUM:
            return self.__generate_medium_level_report(results_df)

    def generate(self, results_df, report_level=ReportLevel.HIGH):
        return self.__generate_report_content(results_df, report_level)
