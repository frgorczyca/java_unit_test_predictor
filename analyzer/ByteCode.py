import json
import re

class ByteCodeAnalyzer():
    
    @staticmethod
    def compare_byte_code(old, new, tests):
        tests_to_run = []
        
        for method in old["methods"]:
            name = method["name"]
            if not ByteCodeAnalyzer.get_method_form_bytecode(new, name):
                tests_to_run = tests_to_run + ByteCodeAnalyzer.get_tests_for_method(name, tests)
                continue

            else:
                old_method = ByteCodeAnalyzer.get_method_form_bytecode(new, name)
                
                if len(old_method["params"]) != len(method["params"]):
                    tests_to_run = tests_to_run + ByteCodeAnalyzer.get_tests_for_method(name, tests)
                    continue

                if len(old_method["code"]["bytecode"]) != len(method["code"]["bytecode"]):
                    tests_to_run = tests_to_run + ByteCodeAnalyzer.get_tests_for_method(name, tests)
                    continue

                for i, op in enumerate(old_method["code"]["bytecode"]):
                    if "value" in op:
                        if "value" not in method["code"]["bytecode"][i]:
                            tests_to_run = tests_to_run + ByteCodeAnalyzer.get_tests_for_method(name, tests)
                            continue
                        elif method["code"]["bytecode"][i]["value"] != op["value"]:
                            tests_to_run = tests_to_run + ByteCodeAnalyzer.get_tests_for_method(name, tests)
                            continue
        return tests_to_run
    
    @staticmethod
    def get_method_form_bytecode(json, name):
        for method in json["methods"]:
            if name == method["name"]:
                return method
            
        return None
    
    @staticmethod
    def get_tests_for_method(name, tests):
        def format_test_name(reg):
            return re.split("\s+",reg)[2]

        rg = r"@Test\n\s*void " + name[:-1] + r"\w+"
        tests_to_run = re.findall(rg, tests)
        return tests_to_run


# new = json.load(open("path/to/json"))
# old = json.load(open('path/to/json'))
# test = open("path/to/test/file").read()

# ByteCodeAnalyzer.compare_byte_code(new, old, test)