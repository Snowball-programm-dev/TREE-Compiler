import lexer, parser

source=open("src/example/test.te","r")
tokFile=open("test.toks","w")
astFile=open("test.ast", "w")

toks = lexer.tokenizer(source.read())
stringToks = f"{toks}"
NewStringToks = ""
for tok in stringToks.split("},"):
    NewStringToks+=tok+"},\n"

tokFile.write(f"toks = {NewStringToks}")


parsed=parser.parser(toks)

newParsed=""

for a in str(parsed).split("},"):
    newParsed+=a+"},\n"

astFile.write(newParsed)

source.close()
tokFile.close()
astFile.close()