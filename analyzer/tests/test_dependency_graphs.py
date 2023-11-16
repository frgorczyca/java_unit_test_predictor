import csv
from typing import Tuple, List
from glob import glob
from pathlib import Path
from analyzer.dependency_graphs import parse_program


def get_file_list() -> Tuple[List[str], List[str]]:
    csv_path = Path("analyzer/data/srcs.csv")
    bc_path = Path("analyzer/data/bytecode/old")

    with open(csv_path, "r") as fp:
        reader = csv.reader(fp)
        _ = next(reader)
        source_files = [row[0] for row in reader]

    bc_files = glob(f"{bc_path}/*.json")

    return bc_files, source_files


def get_files_from_package(package_name: str) -> Tuple[List[str], List[str]]:
    bc_files, source_files = get_file_list()
    bc_files_out, source_files_out = [], []
    for file in bc_files:
        if package_name in file:
            bc_files_out.append(file)

    for file in source_files:
        if package_name in file:
            source_files_out.append(file)

    return bc_files_out, source_files_out


class TestDependencyGraphs:

    def test_file_list(self):
        print(get_file_list())

    def test_dependency_graph_creation(self):
        bc_files, source_files = get_file_list()
        parse_program(bc_files, source_files)

    def test_dependency_graph_creation2(self):
        pass



