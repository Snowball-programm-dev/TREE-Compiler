import lexer, parser, json

source=open("src/example/test.te","r")
tokFile=open("test.toks","w")
astFile=open("test.ast", "w")

toks = lexer.tokenizer(source.read())
stringToks = f"{toks}"
NewStringToks = json.dumps({"toks": toks})


tokFile.write(NewStringToks)


parsed=parser.parser(toks)


newParsed=json.dumps({"ast": parsed[0]})

astFile.write(newParsed)

source.close()
tokFile.close()
astFile.close()