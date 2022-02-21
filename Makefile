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
	rm out.cpp header.h test.*

clean_cpp:
	rm a.out

commit:
	git add .
	git commit -m 'small Update'
	git push -u origin master