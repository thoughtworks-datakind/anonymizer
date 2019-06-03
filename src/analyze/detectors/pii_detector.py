import importlib
import pkgutil
import inspect
import sys

import pandas as pd

import src.analyze.detectors
from src.analyze.detectors.base_detector import BaseDetector
from src.anonymize.drop_anonymizer import DropAnonymizer
from src.anonymize.anonymizer_result import AnonymizerResult


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
    def analyze_and_redact(self, text: str):
        analyzer_results = []
        for detector in self.get_detector_instances():
            analyzer_results = analyzer_results + detector.execute(text)
        redacted_text = DropAnonymizer.redact(text, analyzer_results)
        return AnonymizerResult(redacted_text, analyzer_results)

    def __contains_pii(self, results):
        for result in results:
            if len(result.analyzer_results) > 0:
                return True
        return False

    def analyze_data_frame(self, input_data_frame):
        result_df = pd.DataFrame({})
        columns = list(input_data_frame)
        for col in columns:
            anonymizer_results = input_data_frame[col].apply(self.analyze_and_redact)
            if self.__contains_pii(anonymizer_results):
                result_df[col] = anonymizer_results

        return {"analyzer_results": result_df.applymap(lambda x: x.analyzer_results),
                "redacted_text": result_df.applymap(lambda x: x.redacted_text)}
