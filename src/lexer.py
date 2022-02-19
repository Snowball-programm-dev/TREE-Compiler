import re

keyWords = [
    "String","return",
    "string","ret",
    "class","int",
    "float","object",
    "public", "private",
    "func", "new",
    "this"
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
                "Value":"{"
            })
            current += 1
            myChar+=1
            continue
        if char == "}":
            toks.append({
                "type": "right_curl_paren",
                "Value":"}"
            })
            current += 1
            myChar+=1
            continue
        if char == "(":
            toks.append({
                "type":"left_paren",
                "Value":"("
            })
            current += 1
            myChar+=1
            continue
        if char == ")":
            toks.append({
                "type":"right_paren",
                "Value":")"
            })
            current += 1
            myChar+=1
            continue
        if char == "[":
            toks.append({
                "type":"left_edged_paren",
                "Value":"["
            })
            current += 1
            myChar+=1
            continue
        if char == "]":
            toks.append({
                "type":"right_edged_paren",
                "Value":"]"
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
                "Value":string
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
                "Value":string
            })
            current += 1
            myChar+=1
            continue
        if re.match(numbers, char):
            Value = ""
            while re.match(numbers, char):
                Value+= char
                current += 1
                myChar+=1
                char = inpExpr[current]
            toks.append({
                "type":"number",
                "Value": Value
            })
            continue
        if re.match(alphabet, char):
            Value = ""
            ty = ""
            while re.match(alphabet, char):
                Value += char
                current += 1
                myChar+=1
                char = inpExpr[current]
            for key in keyWords:
                if Value == key:
                    ty="key"
            if ty == "key":
                toks.append({
                        "type": "key_word",
                        "Value": Value
                    })
            #elif Value == "func":
            #    toks.append({
            #        "type": "function",
            #        "Value": Value
            #    })
            else:
                toks.append({
                    "type": "name",
                    "Value": Value
                })
            continue
        if char == ";":
            toks.append({
                "type": "semi",
                "Value":";"
            })
            current += 1
            myChar+=1
            continue
        if char == ".": 
            toks.append({
                "type": "dot",
                "Value":"."
            })
            current += 1
            myChar+=1
            continue
        if char == "=":
            toks.append({
                "type": "equ",
                "Value":"="
            })
            current += 1
            myChar+=1
            continue
        raise ValueError(f"Error at char: {myChar} in line: {line}, dont know: {char}")
    return toks
