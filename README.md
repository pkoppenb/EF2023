# EF2023
[Accès direct au rapport en pdf](https://github.com/pkoppenb/EF2023/blob/main/LaTeX/EF23.pdf). Attention, il fait 250 pages!

## Présentation du 10 janvier 2023

[Accès direct aux transparents](https://github.com/pkoppenb/EF2023/blob/main/Echallens/Koppenburg-Echallens.pdf). 

# Code
Analyse des elections fédérales de 2023, canton de Vaud

Demande une installation récente de `python 3` et de `latex`. 

Pour tourner:
```
make
```

Cela génère 1200 plots en png et autant en pdf, ainsi qu'un petit nombre de fichiers csv. Ça met bien 5 à 10 minutes.

Ensuite, ça génère le rapport.

## Fichiers
`CHCN20231022.csv` : voix par commune pour chaque candidat et d'où les voix viennent. Attention ne liste pas les voix de listes.
`sd-t-17_02-NRW2023-parteien-appendix.csv`: fichier OFS des voix de chaque parti pour chaque commune. Attention ne distingue pas les listes, et ne connait pas lis libres et les pirates.
`LibresEtPirates.csv`: Voix des libres et pirates par arrondissement de vote, obtenus du site du canton
`export-bulletins-PR-CHCN-20231022.csv`: Toutes les combinaisons de bulletins modifés. Permet de savoir qui aime qui. Mais ce distingue pas les communes.
`2021_2026_Communes_vaudoises_et_arrondissements_Liste_des_communes_avec_districts.csv`: Liste des communes et arronsissements basée sur `2021_2026_Communes_vaudoises_et_districts_Liste_des_communes_avec_districts_2_.csv`.

## Changements

01/12/24: Ajout de graphiques des candidats par commune

