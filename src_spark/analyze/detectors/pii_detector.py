import importlib
import pkgutil
import inspect
import sys

from pyspark.sql import DataFrame
from pyspark.sql.types import StructField, StructType, ArrayType, StringType, LongType

import src_spark.analyze.detectors
from src_spark.analyze.detectors.base_detector import BaseDetector


class PIIDetector():

    def __init__(self):
        self.detectors = self.__get_detector_instances()

    def __get_detector_modules(self):
        modules = [modname for importer, modname, ispkg in
                        pkgutil.walk_packages(path=src_spark.analyze.detectors.__path__,
                                              prefix=src_spark.analyze.detectors.__name__+".")
                   if "tests" not in modname]
        return modules

    def __get_detector_instances(self):
        modules = self.__get_detector_modules()
        detectors = []
        for module in modules:
            importlib.import_module(module)
            classes = inspect.getmembers(sys.modules[module], inspect.isclass)
            for class_name, class_type in classes:
                if class_name != "BaseDetector" and issubclass(class_type, BaseDetector):
                    detectors.append(class_type())
        return detectors
    
    def _operation(self, row):
        new_row = []
        for element in row:
            results = []
            for detector in self.detectors:
                results += detector.execute(element)
            new_row.append(results) 

        return new_row
    
    def get_analyzer_results(self, input_data_frame: DataFrame):
        columns = input_data_frame.columns

        array_structtype = StructType([
            StructField("end", LongType(), False),
            StructField("start", LongType(), False),
            StructField("text", StringType(), False),
            StructField("type", StringType(), False)
        ])
        result_schema = []
        for column in columns:
            result_schema.append(StructField(column, ArrayType(array_structtype, True), nullable=False) )

        result = input_data_frame.rdd.map(lambda x: self._operation(x)).toDF(schema=StructType(result_schema))
        # result.show(truncate=False, vertical=True)
        # result.printSchema()
        
        return result

    def get_redacted_text(self, input_data_frame: DataFrame, report: DataFrame):
        pass

    def analyze_data_frame(self, input_data_frame: DataFrame):

        report = self.get_analyzer_results(input_data_frame)
        redacted = self.get_redacted_text(input_data_frame, report)

        return report, redacted

