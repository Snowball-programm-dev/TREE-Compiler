
def code_generation(ast):
    code = '#include "src/lib/native.cpp"\n'
    
    
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
                        if param.get("value") == "string":
                            idk = "char"
                            n+=f"{idk}"
                        elif param.get("value") != []:
                            idk = param.get("value")
                            n+=f"*{idk}[]"
                        else:
                            pass

                    n+=");"
        
        return n

    code +=stepOne(ast)
    return code