import csv
from typing import Tuple, List
from glob import glob
from pathlib import Path
from analyzer.dependency_graphs import parse_program
from analyzer.ProjectManager import test_jvm2json
import os
import subprocess


def generate_bytecode_files():
    jvm2json = test_jvm2json()
    class_files = glob("./TargetSource/**/*.class", recursive=True)
    output_dir = os.path.join(".", "analyzer", "data", "bytecode")
    for class_file in class_files:
        output_name = Path(class_file).name.replace(".class", ".json")
        output = os.path.join(output_dir, output_name)
        subprocess.run([jvm2json, class_file])
        result = subprocess.run([jvm2json, "-s", class_file, "-t", output])
        if result.returncode == 0:
            print(f"created {output}")


def get_file_list() -> Tuple[List[str], List[str]]:
    csv_path = Path("analyzer/data/srcs.csv")
    bc_path = Path("analyzer/data/bytecode")

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

    def test_static_analyzer(self):
        java_path = ""
        java_test_path = ""

        generate_bytecode_files()
        bc_files, source_files = get_file_list()
        #java_files = glob(f"{bc_path}/*.json")




