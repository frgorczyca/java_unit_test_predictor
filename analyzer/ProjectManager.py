import os
import csv
import re
import shutil
import difflib

class Manager:
    path_data = os.path.join(os.getcwd(), "analyzer", "data")
    path_old_src = os.path.join(path_data, "olds")
    path_csv = os.path.join(path_data, "srcs.csv")

    @staticmethod
    def check_if_dir_exists():
        return os.path.exists(Manager.path_data)
    
    @staticmethod
    def look_for_files(directory, extension, expr):
        matching = []
        for root, dirs, files in os.walk(directory):
            if ("analyzer" in root) :
                continue
            for file in files:
                if file.endswith(extension) and expr != "":
                    res = re.search(expr, file)
                    if res.group() != "":
                        matching.append(os.path.join(root, file))
                elif file.endswith(extension) and expr == "":
                    matching.append(os.path.join(root, file))

        return matching

    @staticmethod
    def init_test_data():
        res_tests = Manager.look_for_files(".", ".java", "^.*Test.*$||^.*TEST.*$||^.*test.*$")
        res_src = Manager.look_for_files(".", ".java", "")

        if len(res_src) == 0 and len(res_src) == 0:
            print("No tests neither sources were found!")
            return

        # Create test-data directory
        f_path = os.path.join(Manager.path_data, "olds")

        os.mkdir(Manager.path_data)
        os.mkdir(f_path)

        # Create src and tests csv files
        f_tests = os.path.join(Manager.path_data, "tests.csv")

        with open(f_tests, 'w', newline="") as file:
            writer = csv.writer(file)
            fields = ["File", "LastModTime"]
            writer.writerow(fields)

            for test in res_tests:
                modify_time = os.path.getmtime(test)
                writer.writerow([test, modify_time])

        with open(Manager.path_csv, 'w', newline="") as file:
            writer = csv.writer(file)
            fields = ["File", "LastModTime"]
            writer.writerow(fields)

            for src in res_src:
                if "test" in src or "TEST" in src or "Test" in src:
                    continue
                modify_time = os.path.getmtime(src)
                writer.writerow([src, modify_time])
                shutil.copy2(src, f_path)

    @staticmethod
    def findModifiedFiles():
        res_src = Manager.look_for_files(".", ".java", "")

        files_mod_time = {}
        mod_files = []

        with open(Manager.path_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader :
                files_mod_time[row['File']] = row['LastModTime']

        for src in res_src:
            if "test" in src or "TEST" in src or "Test" in src:
                continue

            mod_time = os.path.getmtime(src)
            if float(files_mod_time[src]) != mod_time :
                # print("Different mod time: ", src, ", was :", files_mod_time[src], ", got: ", mod_time)
                mod_files.append(src)
        return mod_files
    
    @staticmethod
    def getDiff(origin, name) :
        old = os.path.join(os.getcwd(), "analyzer", "data", "olds", name)
        f_origin = open(origin)
        f_old = open(old)

        cur_cont = f_origin.readlines()
        old_cont = f_old.readlines()

        diff = difflib.unified_diff(cur_cont, old_cont, fromfile=origin, tofile=old)

        for line in diff:
            print(line)