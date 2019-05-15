



class ReportGenerator():

    def __init__(self):
        pass

    def __generate_high_level_report(self, results_df):
        return results_df.columns.values

    def __generate_medium_level_report(self, results_df):
        return

    def generate(self, results_df, high_level_report=True):
        if results_df.empty:
            print("There are no PII values in the given input file")
            return results_df
        if high_level_report:
            return self.__generate_high_level_report(results_df)
        return self.__generate_medium_level_report(results_df)