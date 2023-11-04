import json
import re

class Analyzer():
    def __init__(self, old, new, tests) -> None:
        self.old = old
        self.new = new
        self.tests = tests

    def compare_byte_code(self):
        tests_to_run = []
        
        for method in self.old["methods"]:
            name = method["name"]
            if not self.get_method_form_bytecode(self.new, name):
                tests_to_run = tests_to_run + self.get_tests_for_method(name)
                continue

            else:
                old_method = self.get_method_form_bytecode(self.new, name)
                
                if len(old_method["params"]) != len(method["params"]):
                    tests_to_run = tests_to_run + self.get_tests_for_method(name)
                    continue

                if len(old_method["code"]["bytecode"]) != len(method["code"]["bytecode"]):
                    tests_to_run = tests_to_run + self.get_tests_for_method(name)
                    continue

                for i, op in enumerate(old_method["code"]["bytecode"]):
                    if "value" in op:
                        if "value" not in method["code"]["bytecode"][i]:
                            tests_to_run = tests_to_run + self.get_tests_for_method(name)
                            continue
                        elif method["code"]["bytecode"][i]["value"] != op["value"]:
                            tests_to_run = tests_to_run + self.get_tests_for_method(name)
                            continue
        return tests_to_run
    

    def get_method_form_bytecode(self, json, name):
        for method in json["methods"]:
            if name == method["name"]:
                return method
            
        return None
    
    def get_tests_for_method(self, name):
        def format_test_name(reg):
            return re.split("\s+",reg)[2]

        rg = r"@Test\n\s*void " + name + r"\w+"
        tests_to_run = list(map(format_test_name,re.findall(rg,self.tests)))
        return tests_to_run



new = json.load(open("path/to/json"))
old = json.load(open('path/to/json'))
test = open("path/to/test/file").read()

a = Analyzer(new, old , test)
a.compare_byte_code()