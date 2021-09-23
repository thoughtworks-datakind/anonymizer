import json
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

import pandas as pd

from src.constants import ACQUIRE, REPORT
from src.dpf_main import DPFMain


class TestDPFMain(TestCase):

    def setUp(self):
        test_config = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)),"config/test_config.json")
        self.dpf_main = DPFMain(test_config)
        with open(test_config) as input_file:
            self.config_json = json.load(input_file)

    @patch('src.write.csv_writer.CsvWriter.write_csv')
    @patch('src.write.csv_writer.CsvWriter.__init__')
    @patch('src.report.report_generator.ReportGenerator.generate')
    @patch('src.report.report_generator.ReportGenerator.__init__')
    @patch('src.analyze.detectors.pii_detector.PIIDetector.analyze_data_frame')
    @patch('src.acquire.csv_parser.CsvParser.parse')
    @patch('src.acquire.csv_parser.CsvParser.__init__')
    def test_run_parses_the_config_file_and_invokes_respective_stages_correctly(self, mock_csv_parser_init,
                                                                                mock_csv_parser_parse,
                                                                                mock_pii_analyze_df,
                                                                                mock_report_generator_init,
                                                                                mock_generate_report,
                                                                                mock_csv_writer_init,
                                                                                mock_csv_writer_write_csv):
        mock_csv_parser_init.return_value = None
        mock_csv_parser_parse.return_value = MagicMock()
        mock_pii_analyze_df.return_value = (pd.DataFrame({"summary" : ["test result"]}), pd.DataFrame({}))
        mock_report_generator_init.return_value = None
        mock_generate_report.return_value = MagicMock()
        mock_csv_writer_init.return_value = None
        mock_csv_writer_write_csv.return_value = None
        self.dpf_main.run()
        mock_csv_parser_init.assert_called_with(config=self.config_json[ACQUIRE])
        mock_csv_parser_parse.assert_called_with()
        mock_pii_analyze_df.assert_called_with(mock_csv_parser_parse.return_value)
        mock_report_generator_init.assert_called_with(config=self.config_json[REPORT])
        mock_generate_report.assert_called_with(results_df=mock_pii_analyze_df.return_value[0])
        mock_csv_writer_init.assert_called_with(config=self.config_json)
        mock_csv_writer_write_csv.assert_called_with(df=mock_pii_analyze_df.return_value[1])


    @patch('src.write.csv_writer.CsvWriter.write_csv')
    @patch('src.write.csv_writer.CsvWriter.__init__')
    @patch('src.report.report_generator.ReportGenerator.generate')
    @patch('src.analyze.detectors.pii_detector.PIIDetector.analyze_data_frame')
    @patch('src.acquire.csv_parser.CsvParser.parse')
    @patch('src.acquire.csv_parser.CsvParser.__init__')
    def test_run_short_circuits_generate_report_when_no_PII_values_detected(self, mock_csv_parser_init,
                                                                                mock_csv_parser_parse,
                                                                                mock_pii_analyze_df,
                                                                                mock_generate_report,
                                                                                mock_csv_writer_init,
                                                                                mock_csv_writer_write_csv):
        mock_csv_parser_init.return_value = None
        mock_csv_parser_parse.return_value = pd.DataFrame({})
        mock_pii_analyze_df.return_value = (pd.DataFrame({}), pd.DataFrame({}))
        mock_generate_report.return_value = MagicMock()
        mock_generate_report.return_value = None
        mock_csv_writer_init.return_value = None
        mock_csv_writer_write_csv.return_value = None
        self.dpf_main.run()
        mock_csv_parser_init.assert_called_with(config=self.config_json[ACQUIRE])
        mock_csv_parser_parse.assert_called_with()
        mock_pii_analyze_df.assert_called_with(mock_csv_parser_parse.return_value)
        mock_generate_report.assert_not_called()
        mock_csv_writer_init.assert_called_with(config=self.config_json)
        mock_csv_writer_write_csv.assert_called_with(df=mock_pii_analyze_df.return_value[1])



