import os
import csv
import re


def look_for_files(directory, extension, expr):
    matching = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension) and expr != "":
                res = re.search(expr, file)
                if res.group() != "":
                    matching.append(os.path.join(root, file))
            elif file.endswith(extension) and expr == "":
                matching.append(os.path.join(root, file))

    return matching


class TestSet:
    tests = {}
    changed_tests = {}

    @staticmethod
    def check_if_dir_exists():
        path = os.path.join(os.getcwd(), "analyzer", "data")
        return os.path.exists(path)

    @staticmethod
    def init_test_data():
        res_tests = look_for_files(".", ".java", "^.*Test.*$||^.*TEST.*$||^.*test.*$")
        res_src = look_for_files(".", ".java", "")

        # for test in res_tests :
        #     print(test)

        if len(res_src) == 0 and len(res_src) == 0:
            print("No tests neither sources were found!")
            return

        # Create test-data directory
        path = os.path.join(os.getcwd(), "analyzer", "data")
        os.mkdir(path)

        # Create src and tests csv files
        f_srcs = os.path.join(path, "srcs.csv")
        f_tests = os.path.join(path, "tests.csv")

        with open(f_tests, 'w', newline="") as file:
            writer = csv.writer(file)
            fields = ["File", "LastModTime"]
            writer.writerow(fields)

            for test in res_tests:
                modify_time = os.path.getmtime(test)
                writer.writerow([test, modify_time])

        with open(f_srcs, 'w', newline="") as file:
            writer = csv.writer(file)
            fields = ["File", "LastModTime"]
            writer.writerow(fields)

            for src in res_src:
                if "test" in src or "TEST" in src or "Test" in src:
                    continue
                modify_time = os.path.getatime(src)
                writer.writerow([src, modify_time])


if __name__ == "__main__":

    if not TestSet.check_if_dir_exists():
        print("Init")
        TestSet.init_test_data()
