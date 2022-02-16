import lexer, parser, code_generation, json

source=open("src/example/test.te","r")
tokFile=open("test.toks","w")
astFile=open("test.ast", "w")
outputFile=open("out.cpp", "w")


toks = lexer.tokenizer(source.read())
stringToks = f"{toks}"
NewStringToks = json.dumps({"toks": toks})
tokFile.write(NewStringToks)

ast=parser.parser(toks)[0]
newParsed=json.dumps({"ast": ast})
astFile.write(newParsed)


cppCode = code_generation.code_generation(ast)

outputFile.write(cppCode)


source.close()
tokFile.close()
astFile.close()
outputFile.close()