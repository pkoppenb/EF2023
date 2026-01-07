FIGS = $(wildcard ../pdf/*.pdf)
GCFIGS = $(wildcard ../GC-pdf/*.pdf)
TEXSOURCES = $(filter-out $(wildcard Main*.tex),$(wildcard *.tex)) $(wildcard *.sty) $(wildcard *.bib)
ECSOURCES =  Main.tex $(TEXSOURCES) $(FIGS)
GCSOURCES = Main-EC27.tex $(TEXSOURCES) $(GCFIGS)
TABLES = $(wildcard ../tables/*.tex)

all : EC27.pdf EF23.pdf

Main.pdf: $(ECSOURCES)
	pdflatex Main ; pdflatex Main

Main-EC27.pdf: $(GCSOURCES) $(TABLES)
	pdflatex Main-EC27 ; pdflatex Main-EC27

EF23.pdf : Main.pdf
	cp Main.pdf EF23.pdf

EC27.pdf : Main-EC27.pdf
	cp Main-EC27.pdf EC27.pdf

clean:
	rm -f *~ *.aux *.log *.bbl *.blg *.dvi *.tmp *.out *.toc *.lot *.lof Main.pdf Main-EC27.pdf EF23.pdf EC27.pdf

update: clean all

print:
	echo $(TEXSOURCES)
