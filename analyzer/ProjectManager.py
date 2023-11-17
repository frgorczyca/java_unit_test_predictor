import os
import csv
import re
import shutil
import subprocess
import json

data_old_src = "olds-src"
bytecode_path_name = "bytecode"
JVM2JSON_PATH = os.path.join(os.getcwd(), "jvm2json", "9.2.8", "bin", "jvm2json")


def test_jvm2json() -> str:
    try:
        result = subprocess.run(["jvm2json", "-h"], capture_output=True)
        if result.returncode == 0:
            return "jvm2json"
    except Exception:
        try :
            result = subprocess.run([JVM2JSON_PATH, "-h"], capture_output=True)
            if result.returncode == 0:
                return JVM2JSON_PATH
        except Exception:
            raise Exception(f"jvm2json not found on $PATH or {JVM2JSON_PATH}")

class Manager:
    path_data = os.path.join(os.getcwd(), "analyzer", "data")
    path_old_src = os.path.join(path_data, data_old_src)
    path_csv = os.path.join(path_data, "srcs.csv")
    path_tests = os.path.join(path_data, "tests.csv")

    bytecode_path = os.path.join(path_data, "bytecode")
    bytecode_old = os.path.join(bytecode_path, "old")
    bytecode_curr = os.path.join(bytecode_path, "curr")
    bytecode_tests = os.path.join(bytecode_path, "tests")

    # Change to False if you dont want to run jvm2json automatically
    use_jvm2json = True

    if use_jvm2json:
        jvm2json_path = test_jvm2json()


    @staticmethod
    def check_if_dir_exists():
        return os.path.exists(Manager.path_data)
    
    @staticmethod
    def findFile(directory, name, ext = "") :
        matching = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if (ext == "") :
                    if (name in file):
                        matching.append(os.path.join(root, file))
                else :
                    if (name in file and file.endswith(ext)):
                        matching.append(os.path.join(root, file))
        return matching

    @staticmethod
    def look_for_files(directory, extension, expr, exclud_dir = ""):
        matching = []
        for root, dirs, files in os.walk(directory):
            if ("analyzer" in root) :
                continue

            if (exclud_dir!="" and exclud_dir in root):
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
        f_path = os.path.join(Manager.path_data, data_old_src)

        os.mkdir(Manager.path_data)
        os.mkdir(f_path)
        os.mkdir(Manager.bytecode_path)
        os.mkdir(Manager.bytecode_old)
        os.mkdir(Manager.bytecode_curr)

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
        if (Manager.use_jvm2json) :
            Manager.generateByteCodeForAll(os.path.join(Manager.bytecode_old))

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
            mod_files.append(src)
        return mod_files

    @staticmethod
    def generateByteCodeForAll(dest) :
        classes = Manager.look_for_files(".", ".class", "", "test-classes")

        for cl in classes :
            base_name = os.path.basename(cl)
            base_name = base_name.split(".")[0] + ".json"
            file = os.path.join(dest, base_name)
            print(cl)
            result = subprocess.run([Manager.jvm2json_path, "-s", cl, "-t", file])
            if result.returncode != 0:
                raise Exception(f"jvm2json failed.\n\nSTDERR:\n{result.stderr}\n\nSTDOUT:\n{result.stdout}")
        # subprocess.run([jvm2json_path, "-h"])
    
    @staticmethod
    def generateByteCode(name, dest, dest_tests = "") :
        files = Manager.findFile(".", name, ".class")
        for file in files :
            if ("Test" in file or "test" in file or "TEST" in file) :
                if dest_tests == "":
                    continue

                f_name = os.path.basename(file).split(".")[0] + ".json"
                path = os.path.join(dest_tests, f_name)
                subprocess.run([Manager.jvm2json_path, "-s", file, "-t", path])
            else :
                f_name = os.path.basename(file).split(".")[0] + ".json"
                path = os.path.join(dest, f_name)
                subprocess.run([Manager.jvm2json_path, "-s", file, "-t", path])

    @staticmethod
    def getKnownTests() :
        files = []

        with open(Manager.path_tests, newline='') as csvfile :
            reader = csv.DictReader(csvfile)
            for row in reader :
                files.append(row['File'])
        return files
    
    @staticmethod
    def saveTestsDep(dict, path) :
        path = os.path.join(path, "test_dep.json")

        with open(path, "w") as json_file:
            json.dump(dict, json_file)