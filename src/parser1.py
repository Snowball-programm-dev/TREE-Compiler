def parser(toks):
    global current
    current = 0
    def walk():
        global current
        tok = toks[current]

        if tok.get('type') == 'number':
            current+=1
            return {
                "type": "NumberLiteral",
                "value": tok.get("value")
            }
        
        if tok.get("type") == "left_paren":
            node = {
                "type": "Brackets",
                "value": []
            }
            current +=1
            tok = toks[current]
            while tok.get("type") != "right_paren":
                node["value"].append(walk())
            current += 1
            return node

        if tok.get("type") == "equ":
            current+=1
            return {
                "type" : "Equalse",
                "value": tok.get("value")
            }
        
        if tok.get("type") == "left_curl_paren":
            node = {
                "type" : "Object",
                "value": []
            }
            current += 1
            tok = toks[current]
            while tok.get("type") != "right_curl_paren":
                node["value"].append(walk())
            current += 1
            return node
        
        if tok.get("type") == "left_edged_paren":
            node = {
                "type" : "EdgedBrackets",
                "value": []
            }
            current += 1
            tok = toks[current]
            while tok.get("type") != "right_edged_paren":
                node["value"].append(walk())
            current+=1
            return node
        
        if tok.get("type") == "semi":
            current += 1
            return {
                "type": "CallExpression"
            }
        
        if tok.get("type") == "name":
            current += 1
            return {
                "type": "identifyer",
                "value": tok.get("value")
            }
        
        if tok.get("type") == "function":
            current+=1
            node = {
                "type": "function",
                "id": walk(),
                "args": [],
                "value": []
            }
            print(node)
            tok=toks[current]
            if tok.get("type") == "left_paren":
                while tok.get("type") != "right_paren":
                    node["args"].append(walk())
                    print(node)
            else:
                print("error")
                exit()
            tok=toks[current]
            if tok.get("type") == "left_curl_paren":
                while tok.get("type") == "right_curl_paren":
                    node["value"].append(walk())
                    print(node)
            else:
                print("error")
                exit()
            current+=1
        
        if tok.get("type") == "key_word":
            node = {
                "type": "KeyWord",
                "kind": tok.get("value"),
                "value": []
            }
            print(node)
            current+=1
            tok = toks[current]
            node["value"].append(walk())
            print(node)
            while tok.get("type") != "semi" and tok.get("type") != "right_paren":
                node["value"].append(walk())
                tok=toks[current]
            print(node)
            return node

    ast = {
        "type": "root",
        "truk":[]
    }

    while current < len(toks):
        ast["truk"].append(walk())
    return ast

def ast_beatifyer(ast):
    nast=""
    ast = str(ast).split(",")
    for a in ast:
        nast += a+",\n"
    return nast

