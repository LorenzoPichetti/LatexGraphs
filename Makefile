#CC=/usr/bin/cc
PY=python3
LIBS= lib.o
FLAGS= -lm -lssl -lcrypto -g
FNAME= test

default:
	echo no default

test:
	$(PY) testElement.py
	
pdf:
	pdflatex $(FNAME).tex
	okular $(FNAME).pdf &
	
clean:
	rm $(FNAME).*
