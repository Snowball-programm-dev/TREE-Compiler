

def parser(toks):

    global brackets
    brackets = {
        "(":")",
        "[":"]",
        "{":"}"
    }



    def idk(toks):
        nToks = []
        for tok in toks:
            nToks.append(tok.get("value"))
        return nToks


    def parse(toks, end_tok):
        #print(end_tok)
        #print(idk(toks))

        i = 0

        tree = []

        while i<len(toks) and toks[i].get("value") != end_tok:
            if toks[i].get("value") in brackets:
                parsedTree, parsedCount = parse(toks[i+1:], brackets[toks[i].get("value")])
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
            tree=tree[:-1]

        #print(tree)
        return tree, i
    
    return parse(toks, None)
    