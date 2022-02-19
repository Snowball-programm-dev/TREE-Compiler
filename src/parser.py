
class RootNode:
    Type = ""
    Id = ""
    def stats(self):
        return{
            "type": self.Type,
            "id": self.Id
        }

class NEW(RootNode):
    Params = []
    def stats(self):
        return{
                "type": self.Type,
                "id": self.Id,
                "params": self.Params
            }

class node(RootNode):
    Value = []
    def stats(self):
        return{
            "type": self.Type,
            "id": self.Id,
            "Value": self.Value
        }



class Class(node):
    Params = []
    def stats(self):
        return{
            "type": self.Type,
            "id": self.Id,
            "params": self.Params,
            "Value": self.Value
        }

class Var(node):
    visability = ""
    Kind = ""
    def stats(self):
        return{
            "type": self.Type,
            "id": self.Id,
            "vis": self.visability,
            "kind": self.Kind,
            "Value": self.Value
        }

class VALUE:
    Value=None
    def stats(self):
        return self.Value

def ERROR(toks, i):
    print(f"error at token: {i}")
    print(f"token:{toks[i]}")
    exit(-20)


TYPES = [
    "int","string",
    "float","object"
]

def parser(toks):

    global brackets
    brackets = {
        "(":")",
        "[":"]",
        "{":"}"
    }



    #def idk(toks):
    #    nToks = []
    #    for tok in toks:
    #        nToks.append(tok.get("Value"))
    #    return nToks


    def parseStepOne(toks, end_tok):

        i = 0

        tree = []


        while i<len(toks) and toks[i].get("Value") != end_tok:
            if toks[i].get("Value") in brackets:
                parsedTree, parsedCount = parseStepOne(toks[i+1:], brackets[toks[i].get("Value")])
                tree.append({
                    "type": "bracket",
                    "kind": toks[i].get("Value"),
                    "Value": parsedTree
                })
                i+=parsedCount+1
            
            else:
                tree.append(toks[i])
                i+=1
        
        if i < len(toks) and toks[i].get("Value") == end_tok:
            i+=1

        return tree, i

    def CallExpr(toks):
        i = 0
        tree = []
        Line = []
        
        while i < len(toks):
            if toks[i].get("Value") == "class" or toks[i].get("Value") == "func":
                nTree=[]
                while toks[i].get("type") != "bracket":
                    nTree.append(toks[i])
                    i+=1
                nTree.append(toks[i]) 
                i+=1
                nTree.append(toks[i])                   
                parsedTree, parsedCount = parseStepTwo(nTree)
                for t in parsedTree:
                    tree.append(t)
                i+=1
            
            elif toks[i].get("type") == "semi":
                tree.append(parseStepThree(Line))
                Line = []
                i+=1
            
            else:
                Line.append(toks[i])
                i+=1
        
        return tree, i

            

    
    def parseStepTwo(toks):
        i = 0

        tree = []

        while i < len(toks):
            if toks[i].get("type") == "key_word":
                if toks[i].get("Value") == "class":
                    Node = Class()
                    Node.Type = "class"
                    i+=1
                    Node.Id = toks[i].get("Value")
                    TYPES.append(toks[i].get("Value"))
                    i+=1
                    if toks[i].get("kind") == "(":
                        Node.Params = toks[i].get("Value")
                        i+=1
                    if toks[i].get("kind") == "{":
                        parsedTree, parsedCount =CallExpr(toks[i].get("Value"))
                        Node.Value = parsedTree
                        i+=1
                    else:
                        ERROR(toks, i)
                    tree.append(Node.stats())
                
                elif toks[i].get("Value") == "func":
                    Node = Class()
                    Node.Type = "function"
                    i+=1
                    Node.Id = toks[i].get("Value")
                    i+=1
                    if toks[i].get("kind") == "(":
                        Node.Params = toks[i].get("Value")
                        i+=1
                    if toks[i].get("kind") == "{":

                        parsedTree, parsedCount =CallExpr((toks[i].get("Value")))
                        Node.Value = parsedTree
                        i+=1
                    else:
                        ERROR(toks, i)
                    tree.append(Node.stats())



                else:
                    ERROR(toks, i)



            
            else:
                ERROR(toks, i)

        return tree, i



    def parseStepThree(toks):

        i = 0

        Node = node()

        
        if toks[i].get("type") == "key_word" and toks[i].get("Value") != "this" or toks[i].get("Value") in TYPES:
            if toks[i].get("Value") != "new" and toks[i].get("Value") != "ret" and toks[i].get("Value") != "return" and toks[i].get("Value") != "this":
                Node = Var()
                Node.Id = ""
                Node.Type = "var"
                while i<len(toks):
                    if toks[i].get("type") == "key_word" or toks[i].get("Value") in TYPES:
                        if toks[i].get("Value") == "private":
                            Node.visability = False
                        elif toks[i].get("Value") == "public":
                            Node.visability = True
                        elif toks[i].get("Value") in TYPES or "name":
                            Node.Kind = toks[i].get("Value")
                    elif toks[i].get("type") == "name" and Node.Id == "":
                        Node.Id = toks[i].get("Value")
                    elif toks[i].get("type") == "equ":
                        i+=1
                        Node.Value = parseStepThree(toks[i:])
                    i+=1
            elif toks[i].get("Value") == "new":
                Node = NEW()
                Node.Type = toks[i].get("Value")
                i+=1
                Node.Id = toks[i].get("Value")
                i+=1
                Node.Params = toks[i].get("Value")

                return Node.stats()
            elif toks[i].get("Value") == "ret" or toks[i].get("Value") == "return":
                Node = node()
                Node.Type = "return"
                Node.Id = toks[i].get("Value")
                i+=1
                Node.Value = parseStepThree(toks[i:])
                return Node.stats()
        elif toks[i].get("type") == "string":
            Node = VALUE()
            Node.Value = toks[i].get("Value")
            i+=1
        
        
        elif i+2 < len(toks):
            if toks[i+1].get("type") == "dot":
                Node = node()
                Node.Id = toks[i].get("Value")
                Node.Type = "modul"
                i+=2
                Node.Value = parseStepThree(toks[i:])

            elif toks[i+2].get("type") == "equ":
                Node = Var()
                Node.Type = "var"
                if toks[i].get("Value") in TYPES or toks[i].get("Value") == "name":
                    Node.Kind = toks[i].get("Value")
                    i+=1
                Node.Value = parseStepThree(toks[i:])
            elif toks[i].get("type") == "name":
                Node = node()
                Node.Type = "assignment"
                Node.Id = toks[i].get("Value")
                i+=2
                Node.Value = parseStepThree(toks[i:])

                

        elif toks[i].get("type") == "name":
            if i+1 < len(toks):
                if toks[i+1].get("type") != "equ" and toks[i+1].get("type") != "bracket":
                    Node = RootNode()
                    Node.Type = "identifyer"
                    Node.Id = toks[i].get("Value")
                elif toks[i+1].get("type") == "bracket":
                    Node = node()
                    Node.Type="Call"
                    Node.Id = toks[i].get("Value")
                    i+=1
                    if toks[i].get("Value") != []:
                        Node.Value = parseStepThree(toks[i].get("Value"))
                    else:
                        Node.Value = []

                else:
                    Node = node()
                    Node.Type = "assignment"
                    Node.Id = toks[i].get("Value")
                    i+=2
                    Node.Value = parseStepThree(toks[i:])

            else:
                Node = RootNode()
                Node.Type = "identifyer"
                Node.Id = toks[i].get("Value")





        else:
            pass
        return Node.stats()





    return parseStepTwo(parseStepOne(toks, None)[0])[0], None
    

    

