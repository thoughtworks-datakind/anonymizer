from enum import Enum
import pandas as pd


class ReportLevel(Enum):

    HIGH = 1
    MEDIUM = 2
    LOW = 3

class ReportAggregationType(Enum):

    COUNT = 1
    PERCENTAGE = 2

class ReportGenerator():

    def __init__(self):
        pass

    def __generate_high_level_report(self, results_df):
        report_df = pd.DataFrame({"Columns with PII values" : results_df.columns.values})
        return report_df

    def __collate_all_detectors_per_cell(self, analyzer_result):
        return [result.detector() for result in analyzer_result[1]]

    def __calculate_percentage(self, item_count, total_count):
        return round((item_count/total_count) * 100.0, 2)

    def __calculate_detector_percentage(self, row_count, count_map):
        percentage_map = {}
        for key, value in count_map.items():
            percentage_map[key] = "{}%".format(self.__calculate_percentage(value, row_count))
        return percentage_map

    def __calculate_detector_count(self, column_series):
        detector_count_map = {}
        for analyzer_results in column_series.iteritems():
            if not analyzer_results:
                continue
            detector_types = self.__collate_all_detectors_per_cell(analyzer_results)
            for detector_type in detector_types:
                if detector_type not in detector_count_map:
                    detector_count_map[detector_type] = 0
                detector_count_map[detector_type] += 1
        return detector_count_map


    #TODO : filter out the NAs before passing through this
    def calculate_detector_stats_for_each_column(self, column_series):
        stats_map = {}
        count_map = self.__calculate_detector_count(column_series)
        percentage_map = self.__calculate_detector_percentage(len(column_series), count_map)
        for key, value in count_map.items():
            stats_tuple = (value, percentage_map[key])
            stats_map[key] = stats_tuple
        return stats_map

    def __generate_medium_level_report(self, results_df):
        report_df = pd.DataFrame({})
        columns = list(results_df)
        column_reports = []
        for column in columns:
            detector_stats_for_each_column = self.calculate_detector_stats_for_each_column(results_df[column])
            column_report = pd.Series(detector_stats_for_each_column, name=column, index=detector_stats_for_each_column.keys())
            if not column_report.empty:
                column_reports.append(column_report)
        if column_reports:
            report_df = pd.concat(column_reports, axis=1, keys=[series.name for series in column_reports], sort=True)
        return report_df.fillna(value=0)

    def generate_report_content(self, results_df, report_level):
        if report_level == ReportLevel.HIGH:
            return self.__generate_high_level_report(results_df)
        elif report_level == ReportLevel.MEDIUM:
            return self.__generate_medium_level_report(results_df)

    def __print_report(self, report):
        print("\n\n****************************PII ANALYSIS REPORT**************************\n\n")
        if report.empty:
            print("NO PII VALUES WERE FOUND!")
        else:
            print(report)
        print("\n\n****************************DONE!**************************\n\n")

    def generate(self, results_df, report_level=ReportLevel.HIGH):
        final_report = self.generate_report_content(results_df, report_level)
        self.__print_report(final_report)
        return final_report

