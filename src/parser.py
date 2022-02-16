
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
    value=None
    def stats(self):
        return self.value

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
    #        nToks.append(tok.get("value"))
    #    return nToks


    def parseStepOne(toks, end_tok):

        i = 0

        tree = []


        while i<len(toks) and toks[i].get("value") != end_tok:
            if toks[i].get("value") in brackets:
                parsedTree, parsedCount = parseStepOne(toks[i+1:], brackets[toks[i].get("value")])
                tree.append({
                    "type": "bracket",
                    "kind": toks[i].get("value"),
                    "value": parsedTree
                })
                i+=parsedCount+1
            
            else:
                tree.append(toks[i])
                i+=1
        
        if i < len(toks) and toks[i].get("value") == end_tok:
            i+=1

        return tree, i

    def CallExpr(toks):
        i = 0
        tree = []
        Line = []
        
        while i < len(toks):
            if toks[i].get("value") == "class" or toks[i].get("value") == "func":
                nTree=[]
                while toks[i].get("type") != "bracket":
                    nTree.append(toks[i])
                    i+=1
                nTree.append(toks[i]) 
                i+=1
                nTree.append(toks[i])                   
                parsedTree, parsedCount = parseStepTwo(nTree)
                tree.append(parsedTree)
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
                if toks[i].get("value") == "class":
                    Node = Class()
                    Node.Type = "class"
                    i+=1
                    Node.Id = toks[i].get("value")
                    TYPES.append(toks[i].get("value"))
                    i+=1
                    if toks[i].get("kind") == "(":
                        Node.Params = toks[i].get("value")
                        i+=1
                    if toks[i].get("kind") == "{":
                        parsedTree, parsedCount =CallExpr(toks[i].get("value"))
                        Node.Value = parsedTree
                        i+=1
                    else:
                        ERROR(toks, i)
                    tree.append(Node.stats())
                
                elif toks[i].get("value") == "func":
                    Node = Class()
                    Node.Type = "function"
                    i+=1
                    Node.Id = toks[i].get("value")
                    i+=1
                    if toks[i].get("kind") == "(":
                        Node.Params = toks[i].get("value")
                        i+=1
                    if toks[i].get("kind") == "{":

                        parsedTree, parsedCount =CallExpr((toks[i].get("value")))
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

        
        if toks[i].get("type") == "key_word" and toks[i].get("value") != "this" or toks[i].get("value") in TYPES:
            if toks[i].get("value") != "new" and toks[i].get("value") != "ret" and toks[i].get("value") != "return":
                Node = Var()
                Node.Type = "var"
                while i<len(toks):
                    if toks[i].get("type") == "key_word" or toks[i].get("value") in TYPES:
                        if toks[i].get("value") == "private":
                            Node.visability = False
                        elif toks[i].get("value") == "public":
                            Node.visability = True
                        elif toks[i].get("value") in TYPES or "name":
                            Node.Kind = toks[i].get("value")
                    elif toks[i].get("type") == "name" and Node.Id == "":
                        Node.Id = toks[i].get("value")
                    elif toks[i].get("type") == "equ":
                        i+=1
                        Node.Value = parseStepThree(toks[i:])
                    i+=1
            elif toks[i].get("value") == "new":
                Node = NEW()
                Node.Type = toks[i].get("value")
                i+=1
                Node.Id = toks[i].get("value")
                i+=1
                Node.Params = toks[i].get("value")

                return Node.stats()
            elif toks[i].get("value") == "ret" or toks[i].get("value") == "return":
                Node = node()
                Node.Type = "return"
                Node.Id = toks[i].get("value")
                i+=1
                Node.Value = parseStepThree(toks[i:])
                return Node.stats()
        elif toks[i].get("type") == "string":
            Node = VALUE()
            Node.value = toks[i].get("value")
            i+=1
        
        
        elif i+2 < len(toks):
            if toks[i+1].get("type") == "dot":
                Node = node()
                node.Id = toks[i].get("value")
                Node.Type = "modul"
                i+=2
                Node.Value = parseStepThree(toks[i:])

            elif toks[i+2].get("type") == "equ":
                Node = Var()
                Node.Type = "var"
                if toks[i].get("value") in TYPES or toks[i].get("value") == "name":
                    Node.Kind = toks[i].get("value")
                    i+=1
                Node.Value = parseStepThree(toks[i:])

                

        elif toks[i].get("type") == "name":
            if i+1 < len(toks):
                if toks[i+1].get("type") != "equ":
                    Node = RootNode()
                    Node.Type = "identifyer"
                    Node.Id = toks[i].get("value")
                
                else:
                    Node = node()
                    Node.Type = "assignment"
                    Node.Id = toks[i].get("value")
                    i+=2
                    Node.Value = parseStepThree(toks[i:])

            else:
                Node = RootNode()
                Node.Type = "identifyer"
                Node.Id = toks[i].get("value")





        else:
            pass
        return Node.stats()





    return parseStepTwo(parseStepOne(toks, None)[0])[0], None
    

    

