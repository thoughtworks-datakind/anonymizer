import importlib
import pkgutil
import inspect
import sys
import src.analyze.detectors
from src.analyze.detectors.base_detector import BaseDetector


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

    def analyze(self, text):
        return [match for detector in self.get_detector_instances() for match in detector.execute(text)]

