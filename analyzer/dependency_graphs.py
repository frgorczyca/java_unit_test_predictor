from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Generator
from dataclasses import dataclass
from enum import Enum
import json

from .bounds import load_tree_from_file, parse_tree, Bounds

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
    start_point: (int, int)
    end_point: (int, int)

    def __hash__(self):
        return hash(self.name)  # fully qualified name guaranteed to be unique


@dataclass(frozen=True)
class JavaMethod:
    name: str  # fully qualified name
    # params: List[str]
    binding: MethodBind
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

    def dumps(self, file_name):
        # TODO
        raise NotImplementedError()

    @staticmethod
    def loads(file_name) -> "JavaProgram":
        # TODO
        raise NotImplementedError()


def parse_program(list_of_bytecode_files: List[str], list_of_source_files: List[str]) -> JavaProgram:
    """
    :param list_of_bytecode_files:
    :param list_of_source_files:
    :return:
    """
    class_bound_dict: Dict[str, Bounds] = {}
    method_bound_dict: Dict[str, Bounds] = {}
    for source_file in list_of_source_files:
        tree = load_tree_from_file(Path(source_file))
        class_bounds, method_bounds = parse_tree(tree)
        for bound in class_bounds:
            class_bound_dict[bound.name] = bound
        for bound in method_bounds:
            method_bound_dict[bound.name] = bound

    class_dict = {}
    method_dict = {}
    for bytecode_file in list_of_bytecode_files:
        bytecode_text = get_file_text(bytecode_file)
        json_dict = json.loads(bytecode_text)
        # The entire dictionary has to be passed since classes can have inner classes
        java_class, class_methods = parse_json_class(json_dict, class_bound_dict, method_bound_dict)
        class_dict[java_class.name] = java_class
        method_dict.update(class_methods)

    java_program = JavaProgram(
        classes=class_dict,
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
            methods=names,
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
        bytecode = json_dict["code"]["bytecode"]
        calls = parse_calls(bytecode)
        # params = parse_params(json_dict["params"])

        # signature = method_signature(name, params)
        bounds = method_bound_dict[name]

        return JavaMethod(
            name=name,
            # params=params,
            binding=binding,
            bytecode=bytecode,
            calls=set(calls),
            start_point=bounds.start_point,
            end_point=bounds.end_point,
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


def parse_params(params: List[Dict[str, Any]]) -> List[str]:
    parameter_list = []
    for param in params:
        reference_dict_maybe = param.get("type")
        if reference_dict_maybe:
            # try base types
            base_type_maybe = reference_dict_maybe.get("base")
            if base_type_maybe is not None:
                parameter_list.append(base_type_maybe)
                continue
            # try list types
            list_type_maybe = reference_dict_maybe.get("kind")
            if list_type_maybe == "array":
                base_type_maybe = reference_dict_maybe["type"].get("base")
                if base_type_maybe:
                    parameter_list.append(f"{base_type_maybe}[]")
                    continue
                reference_type_maybe = reference_dict_maybe["type"].get("name")
                if reference_type_maybe:
                    parameter_list.append(f"{reference_type_maybe}[]")
                    continue
            # try inner types
            inner_type_maybe = reference_dict_maybe.get("inner")
            if inner_type_maybe:
                inner_type = inner_type_maybe.get("name")
                if inner_type:
                    parameter_list.append(inner_type)
                    continue
            # try reference types
            reference_type_maybe = reference_dict_maybe.get("name")
            if reference_type_maybe:
                parameter_list.append(reference_type_maybe)
                continue
        raise Exception(f"An unknown type was reached in: {params}\n{param}")

    return parameter_list


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
    from analyzer.bounds import print_tree
    path = Path("analyzer/data/bytecode/old/Scene.json")
    source_path = Path("TargetSource/src/main/java/org/dtu/analysis/overloads/Overload.java")

    tree = load_tree_from_file(source_path)
    print_tree(tree, False)
    # print(parse_tree(tree)[1])

if __name__ == "__main__":
    # Needs to run from the root directory
    main()
