import glob
import json

from .ProjectManager import *
from .ByteCode import *
from .SyntaxAnalyzer import *
from .dependency_graphs import *
from .dependency_graphs import parse_program
from .import DynamicAnalyzer

class TestDetector:
    
    traces = {}
    modications = set()

    def get_traces(self, class_path, test_path):
        self.traces = DynamicAnalyzer.get_traces(class_path, test_path)

    def store_traces(self):
        for trace in self.traces:
            with open(f"evaluation_traces/{trace}.json", "w+") as f:
                json_data = { "data": { "test_name": trace, "trace": [{"class_name": value.class_name, "method_name": value.method_name} for value in self.traces[trace]] }}
                json.dump(json_data, fp=f)
    
    def load_traces(self):
        trace_files = glob.glob("evaluation_traces/*")
        for trace_file in trace_files:
            with open(trace_file, "r") as f:
                json_data = json.load(f)["data"]
                self.traces[json_data["test_name"]] = set(DynamicAnalyzer.TraceStep(x["class_name"], x["method_name"]) for x in json_data["trace"])

    def get_modifications(self, class_paths):
        modifications = set()
        for file in class_paths:
            name = os.path.basename(file)
            name = name.split(".")[0]

            if (Manager.use_jvm2json) :
                Manager.generateByteCode(name, Manager.bytecode_curr, Manager.bytecode_tests)

            print("Find modified methods using syntax analysis")
            old_path = os.path.join(Manager.bytecode_old, name + ".json")
            olds = [old_path]
            files = [file]
            program = parse_program(olds, files)

            test_files = Manager.getKnownTests()
            dict = Syntax.ParseTests(test_files)
            Manager.saveTestsDep(dict, Manager.path_data)
            diff, old_cont = Syntax.getDiff(file, name)

            ranges = Syntax.analyzeDiff(diff, old_cont)

            result = set()
            for rg in ranges :
                for key in program.classes:
                    if rg >= program.classes[key].start_point[0] and rg <=  program.classes[key].end_point[0] :
                        for method in program.classes[key].methods :
                            if rg <= program.methods[method].end_point[0] and rg >= program.methods[method].start_point[0] :
                                result.add(program.methods[method].name)
            for r in result:
                modifications.add(r)
        self.modications = modifications

    def get_tests_to_rerun(self, test_path: JavaClass):
        with open(test_path, "r") as fp:
            test_file = json.load(fp)
            test_class = DynamicAnalyzer.JavaClass(json_dict=test_file)

        tests_to_run: Dict[str, Set[str]] = {}
        for test_name, trace in self.traces.items():
            for step in trace:
                fully_qualified_name = f"{step.class_name}.{step.method_name}"
                if fully_qualified_name in self.modications:
                    if test_class.name not in tests_to_run:
                        tests_to_run[test_class.name] = set()
                    tests_to_run[test_class.name].add(test_name)
        return tests_to_run
