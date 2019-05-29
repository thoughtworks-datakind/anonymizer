from src.analyze.utils.analyzer_result import AnalyzerResult


class DropAnonymizer:

    @staticmethod
    def redact(text: str, analyzer_results: [AnalyzerResult]):
        for result in analyzer_results:
            text = text.replace(result.text, "")
        return text
