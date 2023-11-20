from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Generator
from dataclasses import dataclass
from enum import Enum
import json

from .bounds import load_tree_from_file, parse_tree, Bounds
from .interface import JavaTestAnalyzer, TestResult

"""
Semantic static analyzer
"""


class MethodBind(Enum):
    Static = 0
    Virtual = 1
    Special = 2  # Only constructors


def get_binding(method_dict: Dict[Any, Any]) -> MethodBind:
    if "static" in method_dict["access"]:
        return MethodBind.Static
    elif method_dict["name"] == "<init>":
        return MethodBind.Special
    else:
        return MethodBind.Virtual


def bytecode_eq(left: List[Dict[Any, Any]], right: List[Dict[Any, Any]]) -> bool:
    # TODO: Python does value wise comparison here, but this is too aggressive
    #       too many checks are made and certain equalities are rejected
    return left == right


@dataclass(frozen=True)
class JavaClass:
    name: str  # fully qualified name
    superclass: str  # fully qualified name
    methods: List['JavaMethod']
    start_point: (int, int)
    end_point: (int, int)

    def __hash__(self):
        return hash(self.name)  # fully qualified name guaranteed to be unique

    def get_method(self, name: str):
        for method in self.methods:
            if method.name == f"{self.name}.{name}":
                return method
        return None

    def get_test_methods(self) -> List['JavaMethod']:
        tests = list(filter(lambda x: len(x["annotations"]) > 0 and x["annotations"][0]["type"] == "org/junit/jupiter/api/Test", self.methods))
        return tests
    pass


@dataclass(frozen=True)
class JavaMethod:
    name: str  # fully qualified name
    # params: List[str]
    binding: MethodBind
    annotations: List[str]
    bytecode: List[Dict[Any, Any]]
    calls: Set[str]
    start_point: (int, int)
    end_point: (int, int)

    def signature(self) -> str:
        """
        We only care about overloadable characteristics so the signature is just name+params. Note
        that ridiculously long and convoluted signatures are possible because user created types
        are fully qualified
        :return: string signature like: ```int func(int a, float b)``` -> "func.int.float"
        """
        raise NotImplementedError
        # return f"{self.name}.{'.'.join(self.params)}"

    def __eq__(self, other):
        if isinstance(other, JavaMethod):
            # Check name
            if self.name != other.name:
                return False
            # Check binding
            if self.binding != other.binding:
                return False
            if not bytecode_eq(self.bytecode, other.bytecode):
                return False
            return True
        else:
            return NotImplemented

    def __hash__(self):
        # TODO
        pass


@dataclass(frozen=True)
class JavaProgram:
    classes: Dict[str, JavaClass]
    test_classes: Dict[str, JavaClass]
    methods: Dict[str, JavaMethod]

    def get_call_graph(self, method: str) -> Set[str]:
        """
        Greedy algorithm to find call dependencies
        :param method: call graph of method to search
        :return: set of names of all method calls listed once
        """
        method = self.methods[method]  # Fail immediately if method is not known

        def get_all_calls_recursive(call_set: Set[str], program: JavaProgram, current_method: JavaMethod):
            call_set.add(current_method.name)
            for call in current_method.calls:
                get_all_calls_recursive(call_set, program, program.methods[call])

        all_calls = set()
        get_all_calls_recursive(all_calls, self, method)

        return all_calls

    def get_method(self, class_name: str, method_name: str) -> JavaMethod:
        return self.methods[f"{class_name}.{method_name}"]


def parse_program(list_of_bytecode_files: List[str], list_of_source_files: List[str],
                  list_of_test_bytecode: List[str] = None, list_of_test_source: List[str] = None) -> JavaProgram:
    """
    :param list_of_test_source:
    :param list_of_test_bytecode:
    :param list_of_bytecode_files:
    :param list_of_source_files:
    :return:
    """
    if list_of_test_bytecode is None:
        list_of_test_bytecode = []
    if list_of_test_source is None:
        list_of_test_source = []

    class_bound_dict: Dict[str, Bounds] = {}
    method_bound_dict: Dict[str, Bounds] = {}
    for source_file in list_of_source_files + list_of_test_source:
        tree = load_tree_from_file(Path(source_file))
        class_bounds, method_bounds = parse_tree(tree)
        for bound in class_bounds:
            class_bound_dict[bound.name] = bound
        for bound in method_bounds:
            method_bound_dict[bound.name] = bound

    class_dict = {}
    test_class_dict = {}
    method_dict = {}
    for bytecode_file in list_of_bytecode_files:
        bytecode_text = get_file_text(bytecode_file)
        json_dict = json.loads(bytecode_text)
        # The entire dictionary has to be passed since classes can have inner classes
        java_class, class_methods = parse_json_class(json_dict, class_bound_dict, method_bound_dict)
        class_dict[java_class.name] = java_class
        method_dict.update(class_methods)
    for bytecode_file in list_of_test_bytecode:
        bytecode_text = get_file_text(bytecode_file)
        json_dict = json.loads(bytecode_text)
        test_class, class_methods = parse_json_class(json_dict, class_bound_dict, method_bound_dict)
        test_class_dict[test_class.name] = test_class
        method_dict.update(class_methods)

    java_program = JavaProgram(
        classes=class_dict,
        test_classes=test_class_dict,
        methods=method_dict
    )
    return java_program


def parse_json_class(json_dict: Dict[Any, Any],
                     class_bound_dict: Dict[str, Bounds],
                     method_bound_dict: Dict[str, Bounds]
                     ) -> Tuple[JavaClass, Dict[str, JavaMethod]]:
    try:
        name = json_dict["name"]
        superclass = json_dict["super"]["name"]
        methods = [parse_json_method(name, method_json, method_bound_dict) for method_json in json_dict["methods"]]
        names = [method.name for method in methods]

        bounds = class_bound_dict[name]

        java_class = JavaClass(
            name=name,
            superclass=superclass,
            methods=methods,
            start_point=bounds.start_point,
            end_point=bounds.end_point,
        )

        method_dict = {name: method for (name, method) in zip(names, methods)}
        return java_class, method_dict

    except Exception as err:
        print(f"parse_json_class: {err}")


def method_signature(name: str, params: List[str]) -> str:
    params = [param.split("/")[-1] for param in params]
    return f"{name}.{'.'.join(params)}"


def parse_json_method(class_name: str, json_dict: Dict[Any, Any], method_bound_dict: Dict[str, Bounds]) -> JavaMethod:
    try:
        name = f"{class_name}.{json_dict['name']}"
        binding = get_binding(json_dict)
        annotations = json_dict["annotations"]
        bytecode = json_dict["code"]["bytecode"]
        calls = parse_calls(bytecode)
        # params = parse_params(json_dict["params"])

        # signature = method_signature(name, params)
        bounds = method_bound_dict[name]

        return JavaMethod(
            name=name,
            # params=params,
            binding=binding,
            annotations=annotations,
            bytecode=bytecode,
            calls=set(calls),
            start_point=bounds.start_point,
            end_point=bounds.end_point,
        )
    except Exception as err:
        print(f"parse_json_method: {err}")


def parse_calls(bytecode: List[Dict[Any, Any]]) -> Generator[str, None, None]:
    def parse_data(opr):
        _access = opr["access"]  # static, virtual, special
        method_ref = opr["method"]["ref"]["name"]  # class that it belongs to
        method_name = opr["method"]["name"]  # the method name itself
        full_name = f"{method_ref}.{method_name}"
        return full_name

    try:
        # Filter only the bytecode that does invocations
        operations = filter(lambda op: op["opr"] == "invoke", bytecode)
        calls = (parse_data(opr) for opr in operations)
        return calls

    except Exception as err:
        print(f"parse_calls: {err}")



def get_file_text(file) -> str:
    """Get text from a file in the given path"""
    try:
        with open(file) as fp:
            content = fp.read()
    except OSError as err:
        print(f"Error opening file: {err}")
        exit(-1)
    return content


def get_changed_methods(old_program: JavaProgram, new_program: JavaProgram) -> Set[str]:
    changed_methods = set()
    for method_name, method in old_program.methods:
        same_method_maybe = new_program.methods.get(method_name)
        if same_method_maybe != method:
            changed_methods.add(method_name)
    return changed_methods


class DepGraphAnalyzer(JavaTestAnalyzer):

    def __init__(self):
        self.bytecode_files_new = []
        self.source_files_new = []
        self.test_bytecode_files = []
        self.test_source_files = []
        self.bytecode_files = []
        self.source_files = []
        self.program_old: JavaProgram = None
        self.program_new: JavaProgram = None

    def register_files(self, source_files, bytecode_files, test_source_files, test_byte_codes):
        self.source_files = source_files
        self.bytecode_files = bytecode_files
        self.test_source_files = test_source_files
        self.test_bytecode_files = test_byte_codes
        self.program_old = parse_program(list_of_source_files=self.source_files,
                                         list_of_bytecode_files=self.bytecode_files,
                                         list_of_test_source=self.test_source_files,
                                         list_of_test_bytecode=self.test_bytecode_files)

    def register_changes(self, source_files, bytecode_files):
        self.source_files_new = source_files
        self.bytecode_files_new = bytecode_files
        self.program_new = parse_program(list_of_source_files=self.source_files_new,
                                         list_of_bytecode_files=self.bytecode_files_new,
                                         list_of_test_source=self.test_source_files,
                                         list_of_test_bytecode=self.test_bytecode_files)

    def detect_tests_to_rerun(self) -> TestResult:
        test_result = {}
        # cache results to reduce runtime
        checked_methods = {}
        for test_class_name, test_class in self.program_old.test_classes.items():
            test_methods_to_rerun = []
            test_methods = test_class.get_test_methods()
            for test_method in test_methods:
                old_graph = self.program_old.get_call_graph(test_method.name)
                new_graph = self.program_new.get_call_graph(test_method.name)
                if len(old_graph) != len(new_graph):
                    # length mismatch could be due to inlining but we cannot cover that possibility
                    test_methods_to_rerun.append(test_method.name)
                    continue
                for method_name in old_graph:
                    if method_name not in new_graph:
                        # methods might be renamed but need a more robust analysis to check for that
                        test_methods_to_rerun.append(test_method.name)
                        break
                    else:
                        # if we previously compared this method, we do not need to re-compare
                        previously_checked = checked_methods.get(method_name)
                        if previously_checked is not None:
                            if previously_checked:
                                continue
                            else:
                                test_methods_to_rerun.append(test_method.name)
                                break
                        method_old = self.program_old.methods[method_name]
                        method_new = self.program_new.methods[method_name]
                        if method_old != method_new:
                            checked_methods[method_name] = False
                            test_methods_to_rerun.append(test_method.name)
                            break
                        else:
                            checked_methods[method_name] = True
            test_result[test_class_name.replace("/", ".")] = test_methods_to_rerun
        return test_result


def main():
    from pathlib import Path
    from analyzer.bounds import print_tree
    path = Path("analyzer/data/bytecode/old/Scene.json")
    source_path = Path("TargetSource/src/main/java/org/dtu/analysis/overloads/Overload.java")

    tree = load_tree_from_file(source_path)
    print_tree(tree, False)
    # print(parse_tree(tree)[1])


if __name__ == "__main__":
    # Needs to run from the root directory
    main()
