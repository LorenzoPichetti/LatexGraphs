#CC=/usr/bin/cc
PY=python3
LIBS= lib.o
FLAGS= -lm -lssl -lcrypto -g

default:
	echo no default

test:
	$(PY) testGraph.py
	$(PY) testLattice.py
	$(PY) testElement.py
	pdflatex test.tex
	okular test.pdf &
	
clean:
	rm test.*
