import os
from subprocess import run
from datetime import datetime

from analyzer.test_detector import TestDetector
from analyzer.ProjectManager import Manager

command = ["java",
           "-jar",
           ".\\bin\\junit-platform-console-standalone-1.10.1.jar",
           "execute",
           "-cp", ".\\TargetSource\\target\\classes\\",
           "-cp", ".\\TargetSource\\target\\test-classes\\",
           ]  # "-m",  "org.dtu.analysis.arrays.NaiveArraysTest#sum_elements"]

command_all_tests = "java -jar ./bin/junit-platform-console-standalone-1.10.1.jar execute -cp ./TargetSource/target/classes -cp ./TargetSource/target/test-classes --scan-class-path -n org.dtu.analysis.relations.ChosenTests"

class_name = "Chosen"
new_path = f'./TargetSource/src/main/java/org/dtu/analysis/relations/{class_name}.java'
old_path_compiled = os.path.join(Manager.bytecode_old, class_name + ".json")
test_path_compiled = os.path.join(Manager.bytecode_tests, class_name + "Tests.json")

analyzer = TestDetector()

trace_start = datetime.now()
analyzer.get_traces(old_path_compiled, test_path_compiled)
trace_time = datetime.now() - trace_start

modifications_start = datetime.now()
analyzer.get_modifications([new_path])
modifications_time = datetime.now() - modifications_start

matching_start = datetime.now()
tests_to_run = analyzer.get_tests_to_rerun(test_path_compiled)
matching_time = datetime.now() - matching_start

for (cls, names) in tests_to_run.items():
    class_name = cls.replace("/", ".")
    for name in names:
        command += ["-m", f"{class_name}#{name}"]

trimmed_tests_start = datetime.now()
if len(tests_to_run.keys()) > 0: 
    run(command)
trimmed_tests_time = datetime.now() - trimmed_tests_start

all_tests_start = datetime.now()
run(command_all_tests)
all_tests_time = datetime.now() - all_tests_start

print(f"trace time: {trace_time}")
print()
print(f"modification time: {modifications_time}")
print(f"matching time: {matching_time}")
print(f"trimmed test time: {trimmed_tests_time}")
print()
print(f"modications + trimmed: {modifications_time + matching_time + trimmed_tests_time}")
print(f"all tests time: {all_tests_time}")


