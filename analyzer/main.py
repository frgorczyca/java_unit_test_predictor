from ProjectManager import *
from ByteCode import *
from SyntaxAnalyzer import *

use_bytecode = 1
use_syntax = 0

if __name__ == "__main__":

    initialized = True

    if not Manager.check_if_dir_exists():
        print("Init")
        Manager.init_test_data()
        print("Init done")
        initialized = False

    if (initialized) :
        print("Starting analyzers...")
        mod_files = Manager.findModifiedFiles()
        for file in mod_files :
            name = os.path.basename(file)
            name = name.split(".")[0]

            if (use_bytecode) :
                print("Doing bytecode analyzis...")
                if (Manager.use_jvm2json) :
                    Manager.generateByteCode(name, Manager.bytecode_curr)
                
                new_path = os.path.join(Manager.bytecode_curr, name + ".json")
                old_path = os.path.join(Manager.bytecode_old, name + ".json")
                
                new = json.load(open(new_path))
                old = json.load(open(old_path))

                # Get Tests from .csv file, avoid directory traversing
                test_files = []
                test_files = Manager.getKnownTests()

                for test in test_files :
                    test_cont = open(test).read()
                    rerun = ByteCodeAnalyzer.compare_byte_code(new, old, test_cont)
                    if (len(rerun) > 0) :
                        print("For file test: ", test, ", consider reruning: ")
                        for rer in rerun :
                            print(rer)
                print("")
            
            if (use_syntax) :
                print("Doing plain syntax analyzis...")
                test_files = Manager.getKnownTests()
                dict = Syntax.ParseTests(test_files)
                
                # Save generated dict
                Manager.saveTestsDep(dict, Manager.path_data)

            # Manager.getDiff(file, name)