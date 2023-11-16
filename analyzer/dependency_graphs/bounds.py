from os import PathLike

from tree_sitter import Language, Parser
from tree_sitter.binding import Tree, Node
from typing import List, Optional, Tuple
from dataclasses import dataclass


def get_java_language():
    java_language = Language("analyzer/tree-sitter/libtree-sitter-java.so", "java")
    return java_language


def find_first_named(node: Node, name: str) -> Optional[Node]:
    for child in node.named_children:
        if child.type == name:
            return child


def find_any_first_named_greedy(node: Node, names: List[str]) -> Optional[Node]:
    for name in names:
        for child in node.named_children:
            if child.type == name:
                return child


def find_all_named(node: Node, name: str) -> List[Node]:
    return [child for child in (child for child in node.named_children if child.type == name)]


def find_all_named_list(node: Node, *names: str):
    return [child for child in (child for child in node.named_children if child.type in names)]


def print_node_recursive(node: Node, prepend: str = "", all_parameters=False):
    print(f"{prepend}{node.type}:{node.text} ({node.start_point}:{node.end_point})")
    if all_parameters:
        for child in node.children:
            print_node_recursive(child, prepend+"  ", True)
    else:
        for child in node.named_children:
            print_node_recursive(child, prepend+"  ")


def print_tree(tree: Tree, all_parameters=False):
    print_node_recursive(tree.root_node, "", all_parameters)


def find_methods(class_body: Node) -> List[Node]:
    return find_all_named(class_body, "method_declaration")


def find_constructors(class_body: Node) -> List[Node]:
    return find_all_named(class_body, "constructor_declaration")


def find_class_node(node: Node) -> Optional[Node]:
    return find_any_first_named_greedy(node, ["class_declaration", "enum_declaration"])


def find_inner_class_nodes(class_body: Node) -> List[Node]:
    return find_all_named(class_body, "class_declaration")


def find_class_body(class_declaration: Node) -> Node:
    return find_any_first_named_greedy(class_declaration, ["class_body", "enum_body"])


def find_identifier_name(node: Node) -> str:
    identifier = find_first_named(node, "identifier")
    return identifier.text.decode("UTF-8")


def find_package_name(root_node: Node) -> str:
    package_declaration = find_first_named(root_node, "package_declaration")
    identifier = find_first_named(package_declaration, "scoped_identifier")
    return identifier.text.decode("UTF-8")


def find_parameters(node: Node) -> List[str]:
    parameters = find_first_named(node, "formal_parameters")
    parameters = find_all_named(parameters, "formal_parameter")
    list_of_types = []
    for param in parameters:
        param_type = find_any_first_named_greedy(param, ["integral_type", "floating_point_type", "boolean_type", "array_type", "type_identifier"])
        list_of_types.append(param_type.text.decode("UTF-8").replace(" ", ""))
    assert len(parameters) == len(list_of_types)
    return list_of_types


@dataclass(frozen=True)
class Bounds:
    name: str  # fully qualified name
    start_point: (int, int)
    end_point: (int, int)

    @staticmethod
    def from_class(node: Node, name_qualifier="", sep=".") -> 'Bounds':
        name = f"{name_qualifier}{sep}{find_identifier_name(node)}"
        start_point = node.start_point
        end_point = node.end_point
        return Bounds(name, start_point, end_point)

    @staticmethod
    def from_method(node: Node, name_qualifier="", sep=".") -> 'Bounds':
        # params = find_parameters(node)
        name = ".".join([f"{name_qualifier}{sep}{find_identifier_name(node)}"])  # , '.'.join(params)])
        start_point = node.start_point
        end_point = node.end_point
        return Bounds(name, start_point, end_point)

    @staticmethod
    def from_constructor(node: Node, name_qualifier="", sep=".") -> 'Bounds':
        # params = find_parameters(node)
        name = ".".join([f"{name_qualifier}{sep}<init>"])  # , '.'.join(params)])
        start_point = node.start_point
        end_point = node.end_point
        return Bounds(name, start_point, end_point)

    @staticmethod
    def from_given_name(name_qualifier="", name="", sep="."):
        name = f"{name_qualifier}{sep}{name}"
        start_point = (-1, -1)
        end_point = (-1, -1)
        return Bounds(name, start_point, end_point)


def parse_tree(tree: Tree) -> Tuple[List[Bounds], List[Bounds]]:
    """

    :param tree:
    :return: (class_bounds, method_bounds)
    """
    def parse_tree_recursive(class_root_node: Node, prepend_name: str, sep: str, _class_bounds: List[Bounds], _method_bounds: List[Bounds]):
        class_body_node = find_class_body(class_root_node)

        inner_class_nodes = find_inner_class_nodes(class_body_node)
        class_methods = find_methods(class_body_node)
        class_constructors = find_constructors(class_body_node)

        class_bound = Bounds.from_class(class_root_node, prepend_name, sep=sep)
        _class_bounds.append(class_bound)
        prepend_name = class_bound.name
        _method_bounds += [Bounds.from_method(method_node, prepend_name, sep=".") for method_node in class_methods]
        _method_bounds += [Bounds.from_constructor(constructor_node, prepend_name, sep=".") for constructor_node in class_constructors]
        # Add a default constructor if it doesn't exist
        if len(class_constructors) == 0:
            _method_bounds.append(Bounds.from_given_name(prepend_name, name="<init>", sep="."))
        # Add a class constructor
        _method_bounds.append(Bounds.from_given_name(prepend_name, name="<clinit>", sep="."))

        for node in inner_class_nodes:
            parse_tree_recursive(node, prepend_name, sep="$", _class_bounds=_class_bounds, _method_bounds=_method_bounds)

    root_node = tree.root_node
    package_name = find_package_name(root_node)
    package_name = package_name.replace(".", "/")

    root_class_node = find_class_node(root_node)
    class_bounds = []
    method_bounds = []
    parse_tree_recursive(root_class_node, prepend_name=package_name, sep="/", _class_bounds=class_bounds, _method_bounds=method_bounds)

    return class_bounds, method_bounds


def load_tree_from_file(file_path: PathLike) -> Tree:
    parser = Parser()
    parser.set_language(get_java_language())
    handle = open(file_path).read()
    tree = parser.parse(bytes(handle, "utf8"))
    return tree
