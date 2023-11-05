from tree_sitter import Language, Parser
import os

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

            tree.root_node.child_by_field_name

            for child in tree.root_node.children :
                if (child.type == "class_declaration") :
                    body = Syntax.getClassBody(child)
                    methods = Syntax.getMethods(body)

                    for method in methods :
                        if Syntax.checkIfTest(method) :
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
        if "@Test" in method.text.decode("UTF-8") :
            return True
        else :
            return False
        
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
