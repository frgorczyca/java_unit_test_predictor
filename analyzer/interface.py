from typing import Dict, List


TestResult = Dict[str, List[str]]
sample_result = {
    "org.dtu.analysis.arrays.NaiveArraysTest": [
        "sum_elements"
    ]
}


class JavaTestAnalyzer:
    def register_files(self, source_files, bytecode_files, test_source_files, test_byte_codes):
        raise NotImplementedError

    def register_changes(self, source_files, bytecode_files):
        raise NotImplementedError

    def detect_tests_to_rerun(self) -> TestResult:
        raise NotImplementedError


class DummyTestAnalyzer(JavaTestAnalyzer):

    def __init__(self):
        self.test_byte_codes = None
        self.test_source_files = None
        self.bytecode_files = None
        self.source_files = None

    def register_files(self, source_files, bytecode_files, test_source_files, test_byte_codes):
        self.source_files = source_files
        self.bytecode_files = bytecode_files
        self.test_source_files = test_source_files
        self.test_byte_codes = test_byte_codes

    def register_changes(self, source_files, bytecode_files):
        pass

    def detect_tests_to_rerun(self) -> TestResult:
        return sample_result


def run_analysis(analyzer: JavaTestAnalyzer):
    # Time this
    analyzer.register_files(None, None, None, None)
    analyzer.register_changes(None, None)
    tests_to_rerun = analyzer.detect_tests_to_rerun()

    # Time this
    # Run all tests initial state

    # Time this
    # Run all tests changed state

    # Time this
    # Run only tests to rerun





