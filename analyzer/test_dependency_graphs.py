import csv
from glob import glob
from pathlib import Path
from dependency_graphs import parse_program


def get_file_list():
    csv_path = Path("analyzer/data/srcs.csv")
    bc_path =  Path("analyzer/data/bytecode/old")
    fields = []
    rows = []
    with open(csv_path, "r") as fp:
        reader = csv.reader(fp)
        fields = next(reader)
        source_files = [row[0] for row in reader]

    bc_files = glob(f"{bc_path}/*.json")

    return bc_files, source_files


class TestDependencyGraphs:

    def test_file_list(self):
        print(get_file_list())

    def test_dependency_graph_creation(self):
        bc_files, source_files = get_file_list()
        parse_program(bc_files, source_files)