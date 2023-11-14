from subprocess import run
from analyzer.interface import DummyTestAnalyzer
from datetime import datetime

command = ["java",
           "-jar",
           ".\\bin\\junit-platform-console-standalone-1.10.1.jar",
           "execute",
           "-cp", ".\\TargetSource\\target\\classes\\",
           "-cp", ".\\TargetSource\\target\\test-classes\\",
           ]  # "-m",  "org.dtu.analysis.arrays.NaiveArraysTest#sum_elements"]

command_all_tests = ["java",
                     "-jar",
                     ".\\bin\\junit-platform-console-standalone-1.10.1.jar",
                     "execute",
                     "-cp", ".\\TargetSource\\target\\classes\\",
                     "-cp", ".\\TargetSource\\target\\test-classes\\",
                     "--scan-class-path",
                     ]  # "-m",  "org.dtu.analysis.arrays.NaiveArraysTest#sum_elements"]

analyzer_start = datetime.now()
analyzer = DummyTestAnalyzer()
analyzer.register_files(None, None, None, None)
analyzer.register_changes(None, None)
tests_to_run = analyzer.detect_tests_to_rerun()
analyzer_time = datetime.now() - analyzer_start

for (cls, names) in tests_to_run.items():
    for name in names:
        command += ["-m", f"{cls}#{name}"]

trimmed_tests_start = datetime.now()
run(command)
trimmed_tests_time = datetime.now() - trimmed_tests_start

all_tests_start = datetime.now()
run(command_all_tests)
all_tests_time = datetime.now() - all_tests_start

print(f"analysis time: {analyzer_time}")
print(f"trimmed test time: {trimmed_tests_time}")
print(f"all tests time: {all_tests_time}")


