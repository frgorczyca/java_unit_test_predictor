from typing import List, Dict, Any, Set, Tuple, Generator
from dataclasses import dataclass
from enum import Enum
import json

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
    methods: List[str]

    def __hash__(self):
        return hash(self.name)  # fully qualified name guaranteed to be unique


@dataclass(frozen=True)
class JavaMethod:
    name: str  # fully qualified name
    binding: MethodBind
    bytecode: List[Dict[Any, Any]]
    calls: Set[str]

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
    methods: Dict[str, JavaMethod]
    pass

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

    def dumps(self, file_name):
        # TODO
        raise NotImplementedError()

    @staticmethod
    def loads(file_name) -> "JavaProgram":
        # TODO
        raise NotImplementedError()


def parse_program(list_of_bytecode_files: List[str]) -> JavaProgram:
    class_dict = {}
    method_dict = {}
    for file in list_of_bytecode_files:
        text = get_file_text(file)
        json_dict = json.loads(text)
        java_class, class_methods = parse_json_class(json_dict)
        class_dict[java_class.name] = java_class
        method_dict.update(class_methods)

    java_program = JavaProgram(
        classes=class_dict,
        methods=method_dict
    )
    return java_program


def parse_json_class(json_dict: Dict[Any, Any]) -> Tuple[JavaClass, Dict[str, JavaMethod]]:
    try:
        name = json_dict["name"]
        superclass = json_dict["super"]["name"]
        methods = [parse_json_method(name, method_json) for method_json in json_dict["methods"]]
        names = [method.name for method in methods]

        java_class = JavaClass(
            name=name,
            superclass=superclass,
            methods=names
        )

        method_dict = {name: method for (name, method) in zip(names, methods)}
        return java_class, method_dict

    except Exception as err:
        print(f"parse_json_class: {err}")


def parse_json_method(class_name: str, json_dict: Dict[Any, Any]) -> JavaMethod:
    try:
        name = f"{class_name}.{json_dict['name']}"
        binding = get_binding(json_dict)
        bytecode = json_dict["code"]["bytecode"]
        calls = parse_calls(bytecode)
        return JavaMethod(
            name=name,
            binding=binding,
            bytecode=bytecode,
            calls=set(calls),
        )
    except Exception as err:
        print(f"parse_json_method: {err}")


def parse_calls(bytecode: List[Dict[Any, Any]]) -> Generator[str, None, None]:
    def parse_data(opr):
        _access = opr["access"]  # static, virtual, special, TODO: might wish to use this later
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


def main():
    from pathlib import Path
    from tree_sitter.binding import Tree, Node
    from tree_sitter import Language, Parser
    from analyzer.dependency_graphs.util import print_tree, JAVA_LANGUAGE, parse_tree
    path = Path("analyzer/data/bytecode/old/Scene.json")
    source_path = Path("TargetSource/src/main/java/org/dtu/analysis/vector/Scene.java")

    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    handle = open(source_path).read()
    tree = parser.parse(bytes(handle, "utf8"))
    # print_tree(tree)
    print(parse_tree(tree)[1])

    text = get_file_text(path)
    json_dict = json.loads(text)
    program = parse_json_class(json_dict)
    # print(program)


if __name__ == "__main__":
    # Needs to run from the root directory
    main()
