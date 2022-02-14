import re

keyWords = [
    "String","return",
    "string","ret",
    "class","int",
    "float","object",
    "public", "private",
    "func"
]

def tokenizer(inpExpr):
    current=0
    toks=[]
    line=1
    myChar=1

    alphabet=re.compile(r"[A-Za-z_][A-Za-z_0-9]*", re.I)
    numbers=re.compile(r"[0-9]")
    whitespace=re.compile(r"\s")

    while current < len(inpExpr):
        char = inpExpr[current]
        if char == '\n':
            line += 1
            myChar=1
            current += 1
            continue
        if re.match(whitespace, char):
            current += 1
            myChar+=1
            continue
        if char == "{":
            toks.append({
                "type": "left_curl_paren",
                "value":"{"
            })
            current += 1
            myChar+=1
            continue
        if char == "}":
            toks.append({
                "type": "right_curl_paren",
                "value":"}"
            })
            current += 1
            myChar+=1
            continue
        if char == "(":
            toks.append({
                "type":"left_paren",
                "value":"("
            })
            current += 1
            myChar+=1
            continue
        if char == ")":
            toks.append({
                "type":"right_paren",
                "value":")"
            })
            current += 1
            myChar+=1
            continue
        if char == "[":
            toks.append({
                "type":"left_edged_paren",
                "value":"["
            })
            current += 1
            myChar+=1
            continue
        if char == "]":
            toks.append({
                "type":"right_edged_paren",
                "value":"]"
            })
            current += 1
            myChar+=1
            continue
        if  char == '"':
            current += 1
            myChar+=1
            char = inpExpr[current]
            string=""
            while char != '"':
                string += char
                current += 1
                myChar+=1
                char = inpExpr[current]
            toks.append({
                "type":"string",
                "value":string
            })
            current += 1
            myChar+=1
            continue
        if  char == '/':
            current += 1
            myChar+=1
            char = inpExpr[current] 
            if char == '/':
                while char != '\n':
                    current += 1
                    myChar+=1
                    char = inpExpr[current]
            current += 1
            myChar=1
            line+=1
            continue
        if  char == "'":
            current += 1
            myChar+=1
            char = inpExpr[current]
            string=""
            while char != "'":
                string += char
                current += 1
                myChar+=1
                char = inpExpr[current]
            toks.append({
                "type":"string",
                "value":string
            })
            current += 1
            myChar+=1
            continue
        if re.match(numbers, char):
            value = ""
            while re.match(numbers, char):
                value+= char
                current += 1
                myChar+=1
                char = inpExpr[current]
            toks.append({
                "type":"number",
                "value": value
            })
            continue
        if re.match(alphabet, char):
            value = ""
            ty = ""
            while re.match(alphabet, char):
                value += char
                current += 1
                myChar+=1
                char = inpExpr[current]
            for key in keyWords:
                if value == key:
                    ty="key"
            if ty == "key":
                toks.append({
                        "type": "key_word",
                        "value": value
                    })
            #elif value == "func":
            #    toks.append({
            #        "type": "function",
            #        "value": value
            #    })
            else:
                toks.append({
                    "type": "name",
                    "value": value
                })
            continue
        if char == ";":
            toks.append({
                "type": "semi",
                "value":";"
            })
            current += 1
            myChar+=1
            continue
        if char == ".": 
            toks.append({
                "type": "dot",
                "value":"."
            })
            current += 1
            myChar+=1
            continue
        if char == "=":
            toks.append({
                "type": "equ",
                "value":"="
            })
            current += 1
            myChar+=1
            continue
        raise ValueError(f"Error at char: {myChar} in line: {line}, dont know: {char}")
    return toks
