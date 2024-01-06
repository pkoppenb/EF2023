TEXSOURCES = $(wildcard *.tex) $(wildcard *.bib) $(FIGS)

all : EF23.pdf

EF23.pdf : Main.pdf
	mv Main.pdf EF23.pdf

Main.pdf: $(TEXSOURCES)
	pdflatex Main ; pdflatex Main


clean:
	rm -f *~ *.aux *.log *.bbl *.blg *.dvi *.tmp *.out *.blg *.bbl Main.pdf

update: clean all
