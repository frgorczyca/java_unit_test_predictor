from tree_sitter import Language, Parser
import os
import difflib
import re

lib_path = os.path.join(os.getcwd(), "tree-sitter", "libtree-sitter-java.so")

JAVA_LANGUAGE = Language(lib_path, 'java')

class Syntax :
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)

    def ParseTests(tests) :
        test_dict = {}
        for test in tests :
            tested = []
            test_cont = open(test).read()
            tree = Syntax.parser.parse(bytes(test_cont, "utf8"))

            for child in tree.root_node.children :
                if (child.type == "class_declaration") :
                    body = Syntax.getClassBody(child)
                    methods = Syntax.getMethods(body)

                    for method in methods :
                        is_test, test_name = Syntax.checkIfTest(method) 
                        if is_test:
                            m_inv = Syntax.findInvocations(method)
                            ret = Syntax.getCreation(method)

                            for inv in m_inv :
                                if ("assert" in inv.text.decode("UTF-8")) :
                                    continue
                                else :
                                    l_dict = {}
                                    obj = inv.children[0].text.decode("UTF-8")
                                    name = inv.children[2].text.decode("UTF-8")

                                    if (obj in ret) :
                                        obj = ret[obj]
                                    l_dict["name"] = test_name
                                    l_dict[obj] = name
                                    tested.append(l_dict)

            test_dict[test] = tested
        
        return test_dict

    
    def getClassBody(declaration) :
        for child in declaration.children:
            if child.type == "class_body" :
                return child
            
    def getMethods(class_body) :
        methods = []
        for child in class_body.children :
            if (child.type == "method_declaration") :
                methods.append(child)
        return methods
    
    def checkIfTest(method) :
        text = method.text.decode("UTF-8")
        name = ""
        if "@Test" in text :
            text = text.split(' ')
            for i, word in enumerate(text) :
                if ("void" in word) :
                    index = i+1
                    while(text[index] == "") :
                        index += 1
                    name = text[index]
            return True, name
        else :
            return False, name
        
    def findInvocations(parent) :
        inv = []
        for child in parent.children :
            if (child.type == "method_invocation") :
                inv.append(child)
            inv += Syntax.findInvocations(child)
        return inv
    
    def getObjectAndName(inv) :
        return inv.children[0].text.decode("UTF-8"), inv.children[2].text.decode("UTF-8")
    
    def getCreation(test) :
        ret = {}

        for child in test.children :
            if (child.type == "local_variable_declaration") :
                type = ""
                name = ""

                for inner_child in child.children :
                    if (inner_child.type == "type_identifier") :
                        type = inner_child.text.decode("UTF-8")
                    if (inner_child.type == "variable_declarator") :
                        if (inner_child.children[2].type == "object_creation_expression") :
                            name = inner_child.children[0].text.decode("UTF-8")

                
                if (type != "" and name !="") :
                    ret[name] = type

            else :
                ret.update(Syntax.getCreation(child))

        return ret
    
    @staticmethod
    def compareReturns(old, new) :

        changed = []
        o_type = old.children[1].type
        o_text = old.children[1].text.decode("UTF-8")
        
        n_type = new.children[1].type
        n_text = new.children[1].text.decode("UTF-8")

        if (o_type != n_type) :
            # Depends what is stored in dependency graph, new or old?
            changed.append(n_text)
        else :
            if o_type == "identifier" :
                if o_text != n_text :
                    changed.append(n_text)
            if o_type == "field_access" :
                pass
            if o_type == "array_access" :
                pass
        return changed
    
    @staticmethod
    def getDiff(origin, name) :
        old = os.path.join(os.getcwd(), "analyzer", "data", "olds-src", name + ".java")
        f_origin = open(origin)
        f_old = open(old)

        cur_cont = f_origin.readlines()
        old_cont = f_old.readlines()

        diff = difflib.unified_diff(cur_cont, old_cont, fromfile=origin, tofile=old)

        return diff

    @staticmethod
    def findInNew(new_root, node_type) :
        matching = []
        for child in new_root.children:
            if child.type == node_type:
                matching.append(child)
            matching += Syntax.findInNew(child, node_type)
        return matching

    @staticmethod
    def analyzeDiff(diff) :
        ranges = []
        diff_old = []
        diff_new = []

        list_changes = []

        for line in diff:
            res = re.findall(r'^@.+@$', line)
            if res :
                ranges.append(res)
                continue
            res = re.findall(r'^\+', line)
            if res :
                if not "+++" in line:
                    line = line.replace("+", "", 1)
                    diff_old.append(line)
                    continue
            res = re.findall(r'^\-', line)
            if res:
                if not "---" in line:
                    line = line.replace("-", "", 1)
                    diff_new.append(line)
                    continue
        
        separator = '\n'
        old_str = separator.join(diff_old)
        new_str = separator.join(diff_new)

        # print(old_str)
        # print(new_str)
        res = []
        new_ranges = []

        for rng in ranges:
            res += re.findall(r'\d+', rng[0])
        
        for i in range(0, len(res)-1, 4) :
            new_ranges.append([res[i+2], res[i+3]])

        old_tree = Syntax.parser.parse(bytes(old_str, "utf8"))
        new_tree = Syntax.parser.parse(bytes(new_str, "utf8"))

        old_root = old_tree.root_node
        new_root = new_tree.root_node

        # get changed content
        for child in old_root.children:
            nodes = Syntax.findInNew(new_root, child.type)
            
            # Handle different cases
            if child.type == "return_statement" :
                res = Syntax.compareReturns(child, nodes[0])
                list_changes.append(res)

        print(list_changes)
