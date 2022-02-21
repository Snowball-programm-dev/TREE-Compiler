class Vars:
    Id = ""
    Type = ""
    Value = ""
    def stats(self):
        return {
            "id": self.Id,
            "type": self.Type,
            "value": self.Value
        }

secret = ""

def code_generation(ast):
    global secret
    header = '#include "src/lib/native.cpp"\n'
    code = '#include "header.h"\n'

    vars = []
    
    
    def stepOne(ast):
        n=""
        for branch in ast:
            if branch.get("type") == "class":
                n+="class "+ branch.get("id") + " "
                for p in branch.get("params"):
                    n+= ": public " + p
                n+=";\n"
            elif branch.get("type") == "function":
                if branch.get("id") == "main" or branch.get("id") == "Main" :
                    n+="int main(int argc,"
                    for param in branch.get("params"):
                        if param.get("Value") == "string":
                            idk = "char"
                            n+=f"{idk}"
                        elif param.get("Value") != []:
                            idk = param.get("Value")
                            n+=f"*{idk}[]"
                        else:
                            pass

                    n+=");"
        
        return n


    def get_Get(ast):
        get=[]
        if type(ast) == type([]):
            for b in ast:
                if b.get("type") == "class" or b.get("type") == "function" or b.get("kind") == "object":
                    for g in get_Get(b.get("Value")):
                        get.append(g)
                elif b.get("type") == "Call" and b.get("id") == "get":
                    get.append(b.get("Value"))
        else:
            b=ast
            if b.get("type") == "class" or b.get("type") == "function" or b.get("kind") == "object":
                for g in get_Get(b.get("Value")):
                    get.append(g)
            elif b.get("type") == "Call" and b.get("id") == "get":
                get.append(b.get("Value"))
        



        return get

    def stepTwo(ast):
        IMPORTS = ""


        for GETS in get_Get(ast):
            if GETS.get("type") == "identifyer":
                newFile = open(f"src/lib/{GETS.get('id')}.cpp", "r")
                newFile = newFile.read()
                newFile = newFile.split("\n")
                newFile = newFile[1:]
                n = "\n"
                for line in newFile:
                    n+=line+"\n"
                newFile = n
                IMPORTS+= newFile + "\n"
        return IMPORTS
    
    def param_handler(params):
        NEW_PARAMS = ""
        if params == []:
            return ""
        
        elif type(params) == type(""):
            NEW_PARAMS += '"' + params + '"'

        else:
            if params.get("type") == "identifyer":
                NEW_PARAMS += params.get("id") + ""

        
        return NEW_PARAMS

    def varView(var):
        node = Vars()
        node.Id = var.get("id")
        node.Type = var.get("kind")
        node.Value = varHandler(var)
        vars.append(node)

    def CallHandler(call):
        NEW_GENERATED_CODE = ""
        global secret
        if type(call) == type([]):
            print(call)
        else:
            if call.get("type") == "assignment":
                NEW_GENERATED_CODE += call.get("id")
                NEW_GENERATED_CODE += varHandler(call)
                NEW_GENERATED_CODE += ";\n"
            if call.get("type") == "new":
                NEW_GENERATED_CODE += "new " + call.get("id") + "(" + param_handler(call.get("params")) + ");\n"

            if call.get("type") == "identifyer":
                NEW_GENERATED_CODE += call.get("id")
                NEW_GENERATED_CODE += ";\n"
            
            if call.get("type") == "modul":
                next = call.get("Value")
                #if next.get("type") == "Call":
                #    NEW_GENERATED_CODE += call.get("id") + "." + CallHandler(next)
                #else:
                NEW_GENERATED_CODE += call.get("id") + "->" + CallHandler(next)
            
            if call.get("type") == "class" or call.get("type") == "function":
                NEW_GENERATED_CODE += stepThree(call)
            
            if call.get("type") == "Call":
                if call.get("id") == "get" and type(call.get("Value")) != type("string"):
                    secret = CallHandler(call.get("Value"))
                    NEW_GENERATED_CODE +="new "+ secret +"\n"
                else:
                    NEW_GENERATED_CODE += call.get("id") + "(" + param_handler(call.get("Value")) + ")"
                    NEW_GENERATED_CODE += ";\n"

            if call.get("type") == "var":
                if call.get("kind") == "string":
                    NEW_GENERATED_CODE += "std::string " + call.get("id")
                    NEW_GENERATED_CODE += varHandler(call)
                    varView(call)
                elif call.get("kind") == "int":
                    NEW_GENERATED_CODE += "int " + call.get("id")
                    NEW_GENERATED_CODE += varHandler(call)
                    varView(call)
                elif call.get("kind") == "float":
                    NEW_GENERATED_CODE += "float " + call.get("id")
                    NEW_GENERATED_CODE += varHandler(call)
                    varView(call)
                elif call.get("kind") == "object":
                    newList = []
                    varHandler(call)
                    newList[:0] = secret
                    for n in newList[:len(secret)-2]:
                        NEW_GENERATED_CODE += n
                    NEW_GENERATED_CODE += " *" + call.get("id")
                    NEW_GENERATED_CODE += varHandler(call)
                    


                
                else:
                    NEW_GENERATED_CODE += call.get("kind") + "* " + call.get("id")
                    NEW_GENERATED_CODE += varHandler(call)
                    varView(call)

                NEW_GENERATED_CODE += ";\n"

            if call.get("type") == "return":
                NEW_GENERATED_CODE += "return " + CallHandler(call.get("Value"))

        return NEW_GENERATED_CODE
                
    def varHandler(call):
        NEW_GENERATED_CODE = ""
        if call.get("Value") != []:
            NEW_GENERATED_CODE +=" = "
            if type(call.get("Value")) == type({}):
                NEW_GENERATED_CODE += CallHandler(call.get("Value"))
            elif call.get("kind") == "string" or type(call.get("Value")) == type(""):
                NEW_GENERATED_CODE += '"' + call.get("Value") + '"'
            else:
                if type(call.get("Value")) == type(""):
                    NEW_GENERATED_CODE += call.get("Value")
                else:
                    NEW_GENERATED_CODE += str(call.get("Value"))

        
        return NEW_GENERATED_CODE

    def stepThree(ast):
        c = ""

        if type(ast) == type({}):
            c+=funcAndClass_handler(ast)
        else:
            for a in ast:
                c+=funcAndClass_handler(a)

        return c
                    
    def funcAndClass_handler(a):
        c = ""
        if a.get("type") == "class":
            c+="class "+ a.get("id") + " "
            for p in a.get("params"):
                c+= ": public " + p
            c+="{\npublic:\n"
            for call in a.get("Value"):
                c+= CallHandler(call)
            c+="};\n"
        elif a.get("type") == "function":
            if a.get("id") == "main" or a.get("id") == "Main" :
                c+="int main(int argc,"
                for param in a.get("params"):
                    if param.get("Value") == "string":
                        idk = "char"
                        c+=f"{idk}"
                    elif param.get("Value") != []:
                        idk = param.get("Value")
                        c+=f"*{idk}[]"
                    else:
                        pass
                c+="){\n"
                for call in a.get("Value"):
                    c+= CallHandler(call)
                c+="}\n"
            else:
                FuncType = "void"
                for call in a.get("Value"):
                    if call.get("type") == "return":
                        if call.get("Value").get("type") == "modul":
                            if call.get("Value").get("Value").get("type") != "modul":
                                for var in vars:
                                    if call.get("Value").get("Value").get("id") == var.Id:
                                        if var.Type == "string":
                                            FuncType = "std::string"
                                        else:
                                            FuncType = var.Type
                        else:
                            FuncType = CallHandler(call.get("Value"))
                c+= FuncType + " " + a.get("id")
                # Better not Forget about the params later
                c+="(){\n"
                for call in a.get("Value"):
                    c+= CallHandler(call)
                c+="}\n"
            
        
        return c


    def return_handler(ret):
        newString = ""



    header +=stepOne(ast)
    header +=stepTwo(ast)
    code+= stepThree(ast)

    for var in vars:
        pass
        #print(var.stats())

    return header, code