cc=/bin/clang++
py=/bin/python
src=/home/pan/workspace/cpp/tree
cppFile=out.cpp
file=src/main.py

run:
	clear
	${py} ${src}/${file}

cpp:
	${cc} ${src}/${cppFile}


clean:
	rm out.cpp header.h a.out test.*