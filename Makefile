#CC=/usr/bin/cc
PY=python3
LIBS= lib.o
FLAGS= -lm -lssl -lcrypto -g
FNAME= test
TEXCOMPILER= pdflatex
PDFREADER= okular

default:
	echo no default

test:
	$(PY) testFigure.py
	
pdf:
	$(TEXCOMPILER) $(FNAME).tex
	$(PDFREADER) $(FNAME).pdf &
	
clean:
	rm $(FNAME).*
