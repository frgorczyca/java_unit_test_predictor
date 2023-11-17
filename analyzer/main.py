from ProjectManager import *
from ByteCode import *
from SyntaxAnalyzer import *
from dependency_graphs import *
from dependency_graphs import parse_program
from DynamicAnalyzer import get_tests

use_bytecode = 0
use_syntax = 1
use_dynamic = 1

if __name__ == "__main__":

    initialized = True

    if not Manager.check_if_dir_exists():
        print("Init")
        Manager.init_test_data()
        test_files = Manager.getKnownTests()
        dict = Syntax.ParseTests(test_files)
                
        # Save generated dict
        Manager.saveTestsDep(dict, Manager.path_data)
        print("Init done")
        initialized = False

    if (initialized) :
        print("Starting analyzers...")
        mod_files = Manager.findModifiedFiles()
        modifications = set()
        for file in ['./TargetSource/src/main/java/org/dtu/analysis/relations/Chosen.java'] :
            name = os.path.basename(file)
            name = name.split(".")[0]

            print()
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
                print("Find modified methods using syntax analysis")

                if (Manager.use_jvm2json) :
                    Manager.generateByteCode(name, Manager.bytecode_curr, Manager.bytecode_tests)      

                old_path = os.path.join(Manager.bytecode_old, name + ".json")
                olds = [old_path]
                files = [file]
                program = parse_program(olds, files)

                test_files = Manager.getKnownTests()
                dict = Syntax.ParseTests(test_files)
                Manager.saveTestsDep(dict, Manager.path_data)
                diff, old_cont = Syntax.getDiff(file, name)
                # a = list(diff)

                ranges = Syntax.analyzeDiff(diff, old_cont)

                result = set()
                for rg in ranges :
                    for key in program.classes:
                        if rg >= program.classes[key].start_point[0] and rg <=  program.classes[key].end_point[0] :
                            for method in program.classes[key].methods :
                                if rg <= program.methods[method].end_point[0] and rg >= program.methods[method].start_point[0] :
                                    result.add(program.methods[method].name)
                for r in result:
                    modifications.add(r)

                print(result)
            
            if use_dynamic:
                print("Identify tests to re-run based on modifications")
                old_path = os.path.join(Manager.bytecode_old, name + ".json")
                test_path = os.path.join(Manager.bytecode_tests, name + "Tests.json")
                tests_to_rerun = get_tests(old_path, modifications, test_path)
                print(tests_to_rerun)

        
        # Example output
        # ['org/dtu/analysis/arrays/NaiveArrays.sum_elements',
        #  'org/dtu/analysis/arrays/NaiveArrays.sum_elements',
        #  'org/dtu/analysis/arrays/SortingArrays.find_max',
        #  'org/dtu/analysis/arrays/SortingArrays.find_max']