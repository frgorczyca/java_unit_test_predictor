from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pydoc import locate
import uuid
import json

JsonDict = Dict[str, Any]

class JavaClass:
    def __init__(self, json_dict: JsonDict) -> None:
        self.name = json_dict['name']
        self.json_dict = json_dict

    def get_methods(self) -> List[JsonDict]:
        methods: List[JsonDict] = self.json_dict["methods"]
        return methods
    
    def get_method(self, name: str) -> Optional[JsonDict]:
        methods = self.get_methods()
        for method in methods:
            if method["name"] == name:
                return method
        return None
    
    def __str__(self) -> str:
        return self.json_dict["name"]

@dataclass
class ArrayValue:
    length: int
    value: List[Any] # The Any here is not a Value

class Value:
    def __init__(self, value: Any, type_name: str = None):
        self.value = value
        if type_name is None:
            self.type_name = type(value).__name__ 
        else:
            self.type_name = type_name

class Counter:
    def __init__(self, class_name, method_name: str, counter: int):
        self.class_name = class_name
        self.method_name = method_name
        self.counter = counter
    
    def next_counter(self):
        return Counter(self.class_name, self.method_name, self.counter + 1)

    def __eq__(self, other):
        if not isinstance(other, Counter):
            return False
        return self.class_name == other.class_name and self.method_name == other.method_name and self.counter == other.counter 

    def __hash__(self):
        return hash((self.class_name, self.method_name, self.counter))
    
    def __repr__(self):
        return f"{self.method_name} in {self.class_name} at {self.counter}"

class StackElement:
    def __init__(self, local_variables: List[Value], operational_stack, counter: Counter):
        self.local_variables: List[Value] = local_variables
        self.operational_stack: List[Value] = operational_stack
        self.counter: Counter = counter

class Operation:
    def __init__(self, json_doc):
        self.offset: int = json_doc["offset"]
        self.opr: str = json_doc["opr"]
        self.type: str = json_doc["type"] if "type" in json_doc else None
        self.index: int = json_doc["index"] if "index" in json_doc else None
        self.operant: str = json_doc["operant"] if "operant" in json_doc else None
        self.value: Value = Value(json_doc["value"]["value"], json_doc["value"]["type"]) if "value" in json_doc else None
        self.condition: str = json_doc["condition"] if "condition" in json_doc else None
        self.target: int = json_doc["target"] if "target" in json_doc else None
        self.amount: int = json_doc["amount"] if "amount" in json_doc else None
        self.class_: str = json_doc["class"] if "class" in json_doc else None
        self.method: Dict[str, Any] = json_doc["method"] if "method" in json_doc else None

    def get_name(self):
        if self.operant:
            return f"{self.opr}-{self.operant}"
        return self.opr

class Interpreter:
    def __init__(self, java_classes: Dict[str,JavaClass], java_class, method_name, method_args: List[Value], memory: Dict[str, Value] = {}):
        self.memory: Dict[str, Value] = memory
        self.stack: List[StackElement] = [StackElement(method_args, [], Counter(java_class, method_name, 0))]
        self.java_classes = java_classes
        self.trace = []

    def get_class(self, class_name, method_name) -> JavaClass:
        if class_name in self.java_classes.keys():
            return self.java_classes[class_name]
        elif class_name == "java/io/PrintStream" and method_name == "println":
            return JavaClass(json.loads('{"name": "Mock", "methods" :[{"name":"' + method_name + '", "code": { "bytecode": [ { "offset": 0, "opr": "load", "type": "str", "index": 0 }, { "offset": 1, "opr": "print" }, { "offset": 2, "opr": "return", "type": null } ] } } ] }'))
        else:
            return JavaClass(json.loads('{"name": "Mock", "methods" :[{"name":"' + method_name + '", "code": { "bytecode": [ { "offset": 0, "opr": "push", "value": { "type": "integer", "value": 4 } }, { "offset": 1, "opr": "return", "type": "int" } ] } } ] }'))

    def run(self):
        while len(self.stack) > 0:
            element = self.stack.pop()
            self.trace.append(element.counter)
            java_class = self.get_class(element.counter.class_name, element.counter.method_name)
            operation = Operation(java_class.get_method(element.counter.method_name)["code"]["bytecode"][element.counter.counter])
            if operation.get_name() == "return":
                return perform_return(self, operation, element)
            self.run_operation(operation, element)

    def run_operation(self, operation: Operation, element: StackElement):
        method = method_mapper[operation.get_name()]
        method(self, operation, element)

def perform_return(runner: Interpreter, opr: Operation, element: StackElement):
    type = opr.type
    if type == None:
        return None
    value = element.operational_stack.pop().value
    return locate(type)(value)

def perform_push(runner: Interpreter, opr: Operation, element: StackElement):
    v = opr.value
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [v], element.counter.next_counter()))

def perform_load(runner: Interpreter, opr: Operation, element: StackElement):
    value = element.local_variables[opr.index]
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_add(runner: Interpreter, opr: Operation, element: StackElement):
    second = element.operational_stack.pop().value
    first = element.operational_stack.pop().value
    result = Value(first + second)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [result], element.counter.next_counter()))

def perform_sub(runner: Interpreter, opr: Operation, element: StackElement):
    second = element.operational_stack.pop().value
    first = element.operational_stack.pop().value
    result = Value(first - second)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [result], element.counter.next_counter()))

def get_comparison(opr: Operation):
      # name must match Python op names
    comparisons = {
        "ne": "__ne__",
        "eq": "__eq__",
        "gt": "__gt__",
        "ge": "__ge__",
        "le": "__le__",
        "lt": "__lt__"
    }
    return comparisons[opr.condition]

def perform_compare(runner: Interpreter, opr: Operation, element: StackElement):
    second = element.operational_stack.pop().value
    first = element.operational_stack.pop().value
    if getattr(first, get_comparison(opr))(second):
        next_counter = Counter(element.counter.method_name, opr.target)
        runner.stack.append(StackElement(element.local_variables, element.operational_stack, next_counter))
    else:
        runner.stack.append(StackElement(element.local_variables, element.operational_stack, element.counter.next_counter()))

def perform_compare_zero(runner: Interpreter, opr: Operation, element: StackElement):
    first = element.operational_stack.pop().value
    second = 0
    if getattr(first, get_comparison(opr))(second):
        next_counter = Counter(element.counter.class_name, element.counter.method_name, opr.target)
        runner.stack.append(StackElement(element.local_variables, element.operational_stack, next_counter))
    else:
        runner.stack.append(StackElement(element.local_variables, element.operational_stack, element.counter.next_counter()))

def perform_store(runner: Interpreter, opr: Operation, element: StackElement):
    value = element.operational_stack.pop()
    local_vars = [x for x in element.local_variables]
    if len(local_vars) <= opr.index:
        local_vars.append(value)
    else:
        local_vars[opr.index] = value
    runner.stack.append(StackElement(local_vars, element.operational_stack, element.counter.next_counter()))

def perform_increment(runner: Interpreter, opr: Operation, element: StackElement):
    local_vars = [x for x in element.local_variables]
    value = element.local_variables[opr.index].value
    local_vars[opr.index] = Value(value + opr.amount)
    runner.stack.append(StackElement(local_vars, element.operational_stack, element.counter.next_counter()))

def perform_multiplication(runner: Interpreter, opr: Operation, element: StackElement):
    second = element.operational_stack.pop().value
    first = element.operational_stack.pop().value
    result = Value(first * second)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [result], element.counter.next_counter()))

def perform_goto(runner: Interpreter, opr: Operation, element: StackElement):
    next_counter = Counter(element.counter.method_name, opr.target)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack, next_counter))

def perform_new_array(runner: Interpreter, opr: Operation, element: StackElement):
    size = element.operational_stack.pop().value
    memory_address = uuid.uuid4()
    runner.memory[memory_address] = ArrayValue(size, [0] * size)
    value = Value(memory_address)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_array_store(runner: Interpreter, opr: Operation, element: StackElement):
    value_to_store = element.operational_stack.pop().value
    index = element.operational_stack.pop().value
    arr_address = element.operational_stack.pop().value
    runner.memory[arr_address].value[index] = value_to_store
    runner.stack.append(StackElement(element.local_variables, element.operational_stack, element.counter.next_counter()))

def perform_array_load(runner: Interpreter, opr: Operation, element: StackElement):
    index = element.operational_stack.pop().value
    arr_address = element.operational_stack.pop().value
    arr = runner.memory[arr_address]
    if arr.length <= index:
        raise Exception("Index out of bounds")
    value = Value(arr.value[index])
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_get(runner: Interpreter, opr: Operation, element: StackElement):
    # I am not sure what get does but I am guessing it returns 0 when it succeeds and some else otherwise.
    # So we are just always going to assume that it works.
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [Value(0)], element.counter.next_counter()))

def perform_array_length(runner: Interpreter, opr: Operation, element: StackElement):
    arr_address = element.operational_stack.pop().value
    arr_length = runner.memory[arr_address].length
    value = Value(arr_length)
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_new(runner: Interpreter, opr: Operation, element: StackElement):
    memory_address = uuid.uuid4() # Create random memory access
    runner.memory[memory_address] = opr.class_
    value = Value(memory_address, "ref")
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_dup(runner: Interpreter, opr: Operation, element: StackElement):
    value = element.operational_stack[-1]
    runner.stack.append(StackElement(element.local_variables, element.operational_stack + [value], element.counter.next_counter()))

def perform_invoke(runner: Interpreter, opr: Operation, element: StackElement):
    method_name = opr.method["name"]
    class_name = opr.method["ref"]["name"]
    args = []
    for _ in range(len(opr.method["args"])):
        args.append(element.operational_stack.pop().value)
    args.reverse()
    _args, _memory = get_args_and_memory(args, runner.memory)
    interpreter = Interpreter(runner.java_classes, class_name, method_name, _args, _memory)
    result = interpreter.run()
    runner.trace.extend(interpreter.trace)
    if opr.method["returns"] is not None:
        runner.stack.append(StackElement(element.local_variables, element.operational_stack + [Value(result)], element.counter.next_counter()))
    else:
        runner.stack.append(StackElement(element.local_variables, element.operational_stack, element.counter.next_counter()))

def peform_throw(runner: Interpreter, opr: Operation, element: StackElement):
    exception_pointer = element.operational_stack.pop().value
    excpetion = runner.memory[exception_pointer]
    raise Exception(excpetion)

def perform_print(runner: Interpreter, opr: Operation, element: StackElement):
    value = element.operational_stack.pop().value
    print(value, end="")
    runner.stack.append(StackElement(element.local_variables, element.operational_stack, element.counter.next_counter()))

method_mapper = {
    "push": perform_push,
    "return": perform_return,
    "load": perform_load,
    "binary-add": perform_add,
    "binary-sub": perform_sub,
    "binary-mul": perform_multiplication,
    "if": perform_compare,
    "store": perform_store,
    "ifz": perform_compare_zero,
    "incr": perform_increment,
    "goto": perform_goto,
    "newarray": perform_new_array,
    "array_store": perform_array_store,
    "array_load": perform_array_load,
    "arraylength": perform_array_length,
    "get": perform_get,
    "new": perform_new,
    "dup": perform_dup,
    "invoke": perform_invoke,
    "throw": peform_throw,
    "print": perform_print,
}

def get_args_and_memory(method_args: List[Value], memory: Dict):
    args = []
    _memory = memory
    for arg in method_args:
        type_name = type(arg).__name__
        if type_name == "list":
            memory_address = uuid.uuid4()
            _memory[memory_address] = ArrayValue(len(arg), arg)
            args.append(Value(memory_address))
        else:
            args.append(Value(arg, type_name))
    return args, _memory

if __name__ == "__main__":
    with open("TargetSource/target/classes/org/dtu/analysis/control/Conditions.json", "r") as fp:
        original_file = json.load(fp)
        original_class = JavaClass(json_dict=original_file)
    with open("TargetSource/target/classes/org/dtu/analysis/controlChanges1/ConditionalChanges1.json", "r") as fp:
        change_file = json.load(fp)
        change_class = JavaClass(json_dict=change_file)
    with open("TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json", "r") as fp:
        test_file = json.load(fp)
        test_class = JavaClass(json_dict=test_file)

    a = test_class.get_methods()
    tests = list(filter(lambda x: len(x["annotations"]) > 0 and x["annotations"][0]["type"] == "org/junit/jupiter/api/Test", test_class.get_methods()))
    traces: Dict[str, List[Counter]] = {}
    for test in tests:
        test_name = test["name"]
        interpreter = Interpreter({"org/dtu/analysis/control/Conditions": original_class, "org/dtu/analysis/control/ControlFlowTests": test_class}, "org/dtu/analysis/control/ControlFlowTests", test_name, [], {})
        interpreter.run()
        traces[test_name] = interpreter.trace
    
    original_methods = { x["name"]: x for x in original_class.get_methods() }
    changed_methods = { x["name"]: x for x in change_class.get_methods() }
    tests_to_run = set()
    for method_name in original_methods.keys():
        changed_method = changed_methods[method_name]
        for i, opr in enumerate(original_methods[method_name]["code"]["bytecode"]):
            changed_code = changed_method["code"]["bytecode"]
            changed_code[i]["offset"] = "ignore"
            opr["offset"] = "ignore"
            if i >= len(changed_code) or opr != changed_code[i]:
                for test_name, trace in traces.items():
                    for step in trace:
                        if step.class_name == original_class.name and step.method_name == method_name and step.counter == i:
                            tests_to_run.add(test_name)
    print(sorted(tests_to_run))
                