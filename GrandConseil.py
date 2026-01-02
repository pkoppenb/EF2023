import csv
import sys
import copy
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import collections

# https://www.vd.ch/gc/depute-e-s/par-ordre-alphabetique/par-arrondissement
# ce nombre n'est pas encore fixé
_sieges = {
    "Aigle" : 8, 
    "Broye-Vully" : 8, 
    "Gros-de-Vaud" : 8, 
    "La Vallée" : 2, 
    "Yverdon" : 15, 
    "Lausanne-Ville" : 26, 
    "Romanel" : 5, 
    "Lavaux-Oron" : 12, 
    "Morges" : 16, 
    "Nyon" : 19, 
    "Ouest lausannois" : 15, 
    "Pays-d'Enhaut" : 2, 
    "Vevey" : 14 }
_quorum = 0.05

partis_centre = [ "PVL", "Centre", "PEV", "Libres", "UDF" ]

from itertools import combinations

def compareLists(l1,l2):
    if sorted(l1[0])==sorted(l2[1]) and sorted(l1[1])==sorted(l2[0]): return False
    return True

def apparentementsValides():
    """
    Construit tous les apparentemets de 5 partis
    """
    valides = [[partis_centre]]
    for a4 in list(combinations(partis_centre,4)):
        valides.append( [ list(a4), list(set(partis_centre) - set(a4)) ] )
    for a3 in list(combinations(partis_centre,3)):
        rest = list(set(partis_centre) - set(a3))
        valides.append( [ list(a3), rest ] )
        valides.append( [ list(a3), [ rest[0] ], [rest[1] ] ])
    for a2 in list(combinations(partis_centre,2)):
        rest = list(set(partis_centre) - set(a2))
        for a22 in list(combinations(rest,2)):
            test = [ list(a2), list(a22), list(set(rest) - set(a22)) ] # I am generating duplicates here. Do not append yet
            good = True
            for v in valides: good = (good and compareLists(v,test))
            if good: valides.append(test)
        valides.append( [ list(a2), [rest[0]], [rest[1]], [rest[2]] ] )
    valides.append( [ [partis_centre[0]], [partis_centre[1]], [partis_centre[2]],  [partis_centre[3]],  [partis_centre[4]] ] )
    # ordonne pour que le PVL soit toujours premier
    valides2 = []
    for v in valides:
        for k in range(len(v)):
            if 'PVL' in v[k]: v2 = [ v[k] ]
        for k in range(len(v)):
            if 'PVL' not in v[k]: v2.append( v[k] )
        valides2.append(v2)
    
    return valides2

#######################################################
def GrandConseil(resultats,nsieges):
    """
    Algorithme du grand conseil - des plus grans restes
    """
    sieges = {}
    total = sum(resultats.values())
    quotient = total/(sieges+0.5)
    # 1er passage
    for p,v in resultats.items():
        sieges[p] = int(nsieges*resultats[p]/total)
    # plus grands restes
    if sum(sieges.values())==nsieges: return sieges  # can't practically happen
    reste = { p: resultats[p]-sieges[p]*quotient for p in resultats.keys() }
    reste = dict(sorted(reste.items(), key=lambda item: item[1], reverse=True))
    for k in reste.keys():
        if reste[k]>=nsieges-sum(sieges.values()): sieges[k]+=1
    return sieges
    
#######################################################
def plotCentres(pourcentages,nsieges=None):
    """
    le graphique de toutes les combinaisons
    """
    valides = apparentementsValides()
    
    

#######################################################
apps = apparentementsValides()
print("Il a {0} apparentements possibles".format(len(apps)))
for a in apps:
    print(a)
