.SUFFIXES: .pdf .py

ALLFILES = $(patsubst %.py,%.pdf,$(wildcard *.py))
all: $(ALLFILES)

.py.pdf:
	python $*.py
