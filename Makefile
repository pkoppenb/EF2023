INFILES = $(widcard *.csv)

# pour l'output je prends un fichier au hasard. Le code en génères des milliers
all: csv/Parti-Bilan-PVL.csv LaTeX/EF23.pdf

csv/Parti-Bilan-PVL.csv : BulletinsModifies.py $(INFILES)
	python3 BulletinsModifies.py | tee log

LaTeX/EF23.pdf : csv/Parti-Bilan-PVL.csv
	( cd  LaTeX/ ; make )

