from unittest import TestCase
from pyspark.sql import SparkSession
from src_spark.analyze.detectors.pii_detector import PIIDetector
from src.analyze.utils.analyzer_result import AnalyzerResult
from pyspark.sql.types import StructField, StructType, ArrayType, StringType, LongType, Row


class TestPIIDetector(TestCase):
    
    def setUp(self) -> None:
        self.SPARK = SparkSession.builder \
                                .master("local") \
                                .appName("Test PIIDetector") \
                                .getOrCreate()
        self.pii_detector = PIIDetector()

        self.array_structtype = StructType([
            StructField("end", LongType(), False),
            StructField("start", LongType(), False),
            StructField("text", StringType(), False),
            StructField("type", StringType(), False)
        ])
        self.schema = StructType([
            StructField("summary", ArrayType(self.array_structtype, True), nullable=False),
            StructField("phone number", ArrayType(self.array_structtype, True), nullable=False) 
        ])

    def test_analyze_data_frame_runs_analyze_against_each_cell_with_a_PII_value(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ("First President of Singapore NRIC was S0000001I", "Some examples of phone numbers are +65 62345678"),
                ("A typical email id would look something like test@sample.com","Some examples of phone numbers are +65 62345678")
            ],
            ["summary", "phone number"]
        )

        actual = self.pii_detector.get_analyzer_results(test_data_frame)

        expected_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]),
                ([AnalyzerResult("test@sample.com", "EMAIL", 45, 60)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
            ],
            self.schema
        )

        self.assertEqual(actual.schema, expected_data_frame.schema)
        self.assertEqual(actual.collect(), expected_data_frame.collect())

    def test_analyze_data_frame_runs_analyze_against_cell_with_multiple_PII_values(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ("First President of Singapore NRIC was S0000001I", "Some examples of phone numbers are +65 62345678"),
                ("email test@sample.com and phone +65 62345678","Phone one +65 62345678 Phone two +65 62345678")
            ],
            ["summary", "phone number"]
        )

        actual = self.pii_detector.get_analyzer_results(test_data_frame)

        expected_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]),
                ([AnalyzerResult("test@sample.com", "EMAIL", 6, 21), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 32, 44)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 10, 22), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 33, 45)])
            ],
            self.schema
        )

        self.assertEqual(actual.schema, expected_data_frame.schema)
        self.assertEqual(actual.collect(), expected_data_frame.collect())

    def test_analyze_data_frame_returns_empty_data_frame_when_there_are_no_PII_values(self):
        test_data_frame = self.SPARK.createDataFrame(
            [
                ("No", "Personal"),
                ("Data","Inside")
            ],
            ["summary", "phone number"]
        )

        actual = self.pii_detector.get_analyzer_results(test_data_frame)

        expected_data_frame = self.SPARK.createDataFrame(
            [
                ([], []),
                ([], [])
            ],
            self.schema
        )

        self.assertEqual(actual.schema, expected_data_frame.schema)
        self.assertEqual(actual.collect(), expected_data_frame.collect())

    def test_get_pii_list_returns_list_of_pii_words_given_row_of_list_of_analyzer_results(self):
        test_row = Row(
            summary=[
                AnalyzerResult("S0000001I", "NRIC", 38, 47),
                AnalyzerResult("S0000002I", "NRIC", 38, 47)
                ],
            phone_number=[AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)])
        actual = self.pii_detector._get_pii_list(test_row)
        expected = ["S0000001I","S0000002I","+65 62345678"]
        self.assertEqual(actual, expected)

    def test_get_pii_list_returns_empty_lists_no_analyzer_results(self):
        test_row = Row(summary=[],phone_number=[])
        actual = self.pii_detector._get_pii_list(test_row)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_redacted_text_returns_redacted_data_frame(self):
        test_report_data_frame = self.SPARK.createDataFrame(
            [
                ([AnalyzerResult("S0000001I", "NRIC", 38, 47)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 35, 47)]),
                ([AnalyzerResult("test@sample.com", "EMAIL", 6, 21), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 32, 44)], [AnalyzerResult("+65 62345678", "PHONE_NUMBER", 10, 22), AnalyzerResult("+65 62345678", "PHONE_NUMBER", 33, 45)])
            ],
            self.schema
        )

        test_input_data_frame = self.SPARK.createDataFrame(
            [
                ("First President of Singapore NRIC was S0000001I", "Some examples of phone numbers are +65 62345678"),
                ("email test@sample.com and phone +65 62345678","Phone one +65 62345678 Phone two +65 62345678")
            ],
            ["summary", "phone number"]
        )

        actual = self.pii_detector.get_redacted_text(test_input_data_frame, test_report_data_frame)
        
        expected = self.SPARK.createDataFrame(
            [
                ("First President of Singapore NRIC was ", "Some examples of phone numbers are "),
                ("email  and phone ","Phone one  Phone two ")
            ],
            ["summary", "phone number"]
        )

        self.assertEqual(actual.schema, expected.schema)
        self.assertEqual(actual.collect(), expected.collect())

    def test_get_redacted_text_returns_same_data_frame_if_analyzer_results_are_empty(self):
        test_report_data_frame = self.SPARK.createDataFrame(
            [
                ([], []),
                ([], [])
            ],
            self.schema
        )

        test_input_data_frame = self.SPARK.createDataFrame(
            [
                ("No", "Personal"),
                ("Data","Inside")
            ],
            ["summary", "phone number"]
        )

        actual = self.pii_detector.get_redacted_text(test_input_data_frame, test_report_data_frame)
        
        expected = self.SPARK.createDataFrame(
            [
                ("No", "Personal"),
                ("Data","Inside")
            ],
            ["summary", "phone number"]
        )

        self.assertEqual(actual.schema, expected.schema)
        self.assertEqual(actual.collect(), expected.collect())

