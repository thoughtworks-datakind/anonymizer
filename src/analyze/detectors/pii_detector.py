import importlib
import pkgutil
import inspect
import sys

import pandas as pd

import src.analyze.detectors
from src.analyze.detectors.base_detector import BaseDetector

#TODO : refactor this to use the annotations instead of the module path.

class PIIDetector:

    def __init__(self):
        pass

    def get_detector_modules(self):
        modules = [modname for importer, modname, ispkg in
                        pkgutil.walk_packages(path=src.analyze.detectors.__path__,
                                              prefix=src.analyze.detectors.__name__+".")
                   if "tests" not in modname]
        return modules

    def get_detector_instances(self):
        modules = self.get_detector_modules()
        detectors = []
        for module in modules:
            importlib.import_module(module)
            classes = inspect.getmembers(sys.modules[module], inspect.isclass)
            for class_name, class_type in classes:
                if class_name != "BaseDetector" and issubclass(class_type, BaseDetector):
                    detectors.append(class_type())
        return detectors

    #TODO : Should we make this static?
    def analyze(self, text):
        return [match for detector in self.get_detector_instances() for match in detector.execute(text)]

    def __has_PII_values(self, columns):
        return any([len(col) > 0 for col in columns])

    def analyze_data_frame(self, input_data_frame):
        result_df = pd.DataFrame({})
        columns = list(input_data_frame)
        for col in columns:
            analyzer_results = input_data_frame[col].apply(self.analyze)
            if self.__has_PII_values(analyzer_results):
                result_df[col] = analyzer_results
        return result_df
