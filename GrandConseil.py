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
    "Pays d'En Haut" : 2, 
    "Vevey" : 14 }
_sieges["Vaud"] = sum(_sieges.values())
_quorum = 0.05

from itertools import combinations
from Utilities import deuxPlots, goodName

plt.figure(figsize=(7,5))
fig, ax = plt.subplots()
fontAxis = {'size'   : 7}
#############################################################################
class Apparentement():
    """
    Un apparentement de partis
    """
    def __init__(self,partis):
        if isinstance(partis,tuple): self.partis = list(partis)
        elif isinstance(partis,set): self.partis = list(partis)
        elif not isinstance(partis,list): self.partis = [partis]
        else: self.partis = partis

        # PVL first
        PVL = None
        for p in self.partis:
            if 'PVL' == p.nom: PVL = p
        if PVL:
            self.partis.remove(PVL)
            self.partis.insert(0, PVL)     
        
        # total
        self.total_par_arrondissement = { arr: sum([ p.total_par_commune[arr]*p.fudge for p in self.partis ]) for arr in list(_sieges.keys())[:-1] } 
        self.total_par_arrondissement["Vaud"] = sum([ p.suffrages*p.fudge for p in self.partis ])
        self.sieges_par_arrondissement = {} 
        # print("Apparentement de {0}".format(self))

    def __repr__(self):
        r = "[ "
        for p in self.partis: r+=p.nom+", "
        return r[:-2]+" ]"   # supprime `, ` et replace par ` ]`

    def attribueSieges(self,ns,arr):
        """
        attribue les sieges pour un arrondissement et distribue sur les partis
        """
        resultats = { p: p.total_par_commune[arr]*p.fudge for p in self.partis }
        self.sieges_par_arrondissement[arr] = GrandConseil( resultats, ns )
        
        # EDIT HERE
        
def printApps(apps):
    """
    imprime un ensemble d'apparentements
    """
    r = ""
    for a in apps: r += "{0}, ".format(a)
    return r[:-2]
        
#######################################################
def GrandConseil(resultats,nsieges,debug=False):
    """
    Algorithme du grand conseil - des plus grands restes
    """
    if 0==nsieges : return { p: 0 for p in resultats.keys() }
    if debug:  print("Je dois distribuer {0} sieges sur la base de {1}".format(nsieges,resultats))
    sieges = {}
    total = sum(resultats.values())
    quotient = total/(nsieges+0.5)
    # 1er passage
    for p,v in resultats.items():
        sieges[p] = int(nsieges*resultats[p]/total)
    second = nsieges-sum(sieges.values())
    if debug: print("Première distribution: {0}. Il reste {1} siège(s)".format(sieges,second))
    if 0==second: return sieges  # peu probable
    # plus grands restes
    restes = { p: resultats[p]-sieges[p]*quotient for p in resultats.keys() }
    restes = dict(sorted(restes.items(), key=lambda item: item[1], reverse=True))  # classement
    if debug: print("    Restes: {0}.".format(restes))
    for k in list(restes.keys())[:second]: # les n premiers prennent un siège
        sieges[k]+=1
    if debug: print("Seconde distribution: {0}".format(sieges))
    if (sum(sieges.values())!=nsieges):
        print("Oups! J'ai distribué {0} au lieu de {1} sièges".format(sieges,nsieges))
        if not debug: GrandConseil(resultats,nsieges,debug=True) # rejoue en mode debug
        sys.exit()
    return sieges
    
#############################################################################
def compareApps(l1,l2):
    r1,r2 = 1,1
    for a1 in l1: r1*=a1.total_par_arrondissement['Nyon']
    for a2 in l1: r2*=a2.total_par_arrondissement['Nyon']
    return (not r1==r2)

#############################################################################
def apparentementsValides(partis_centre):
    """
    Construit tous les apparentemets de 5 partis
    """
    valides = [[Apparentement(partis_centre)]]
    for a4 in list(combinations(partis_centre,4)):
        valides.append( [ Apparentement(a4), Apparentement(set(partis_centre) - set(a4)) ] )
    for a3 in list(combinations(partis_centre,3)):
        rest = list(set(partis_centre) - set(a3))
        valides.append( [ Apparentement(a3), Apparentement(rest) ] )
        valides.append( [ Apparentement(a3), Apparentement(rest[0] ), Apparentement( rest[1] ) ])
    for a2 in list(combinations(partis_centre,2)):
        rest = list(set(partis_centre) - set(a2))
        for a22 in list(combinations(rest,2)):
            test = [ Apparentement(a2), Apparentement(a22), Apparentement(set(rest) - set(a22)) ] # I am generating duplicates here. Do not append yet
            good = True
            for v in valides: good = (good and compareApps(v,test))
            if good: valides.append(test)
        valides.append( [ Apparentement(a2), Apparentement(rest[0]), Apparentement(rest[1]), Apparentement(rest[2]) ] )
    valides.append( [ Apparentement(partis_centre[0]), Apparentement(partis_centre[1]), Apparentement(partis_centre[2]),
                      Apparentement(partis_centre[3]), Apparentement(partis_centre[4]) ] )
    # ordonne pour que le PVL soit toujours premier
    valides2 = []
    for v in valides:
        v2 = []
        for k in range(len(v)):
            # print(partis_centre[0], v[k].partis)
            if partis_centre[0] in v[k].partis: v2.append( v[k] ) # PVL
        for k in range(len(v)):
            if partis_centre[0] not in v[k].partis: v2.append( v[k] )
        valides2.append(v2)

    # check
    for i in range(len(valides2)):
        for j in range(len(valides2)):
            if j<=i: continue
            if compareApps(valides2[i],valides2[j]):
                print("{0} et {1} sont identiques".format(valides2[i],valides2[j]))
                sys.exit()
        
    return valides2

#######################################################
def genereApparentements(centre,partis):
    _leCentre = Apparentement([ partis['Centre'] ])
    _CUDF = Apparentement([ partis['Centre'], partis['UDF'] ])
    gauche = Apparentement([ partis['PST/Sol.'], partis['VERT-E-S'], partis['PS'], partis['Pirates'] ])
    droite = Apparentement([ partis['UDC'], partis['PLR'] ])  # redéfinis à chaque fois
    apps = [ i for i in centre ]  # clone the thing
    if _leCentre in apps:
        apps.remove(_leCentre)
        droite.append( _leCentre[0] ) # add element
    elif _CUDF  in apps:              # ai-je besoin de reverse? 
        apps.remove(_CUDF)
        droite.append(_CUDF[0])
        droite.append(_CUDF[1])
    apps.append(droite)
    apps.append(gauche)
    return apps
    
#######################################################
def distribueSieges(arr,centres,partis,fudge=0.,debug=False):
    """
    Distribue les sièges de l'arrondissement
    """
    if debug: print("Je commence avec {0}".format(centres))
    sieges_partis = {}
    apps = genereApparentements(centres,partis)
    if debug: print("Je teste les apparentements {0}".format(apps))
    resultats = { a: a.total_par_arrondissement[arr] for a in apps }
    resultats5 = { a: resultats[a] if resultats[a]/sum(resultats.values())>=_quorum else 0 for a in apps } # quorum
    if debug: print(resultats,resultats5)
    sieges = GrandConseil(resultats5, _sieges[arr] )
    for a,s in sieges.items():
        a.attribueSieges(s,arr)  # distribue sur les partis
        if debug: print("     {0}: l'apparentement {1} fait {2} suffrages et {3} sièges".format(arr,a,a.total_par_arrondissement[arr],sieges[a]))
        for p in a.partis:
            if a.sieges_par_arrondissement[arr][p]>0 and debug: print("         {0} fait {1} siège(s) à {2}".format(p,a.sieges_par_arrondissement[arr][p],arr))
            if p in sieges_partis.keys():
                print("{0} est dans plusieurs apparentements".format(p))
                sys.exit()
            sieges_partis[p] = a.sieges_par_arrondissement[arr][p]
    return sieges_partis

####################################################
def plotSieges(arr,apps,combDeSieges,partis,maxx=None,fudge=None):
    """
    graphique des sièges

    arr: arrondissement de vote
    apps: apparentements considérés (liste)
    combDeSieges [ {parti: siege,...}, {}...] : combinaisons de sièges par parti. Liste de même taille que apps.
    partis: tous les partis
    """
    # redistribue les sieges par parti
    siegesParParti = {}
    for p in partis.values(): siegesParParti[p] = [ c[p] for c in combDeSieges ]
    # print("Arrondissement {0} - PVL: {1}".format(arr,siegesParParti[partis['PVL']]))

    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.40)
    y_pos = np.arange(len(apps)+2)

    base = [0]*len(apps) # sieges
    base_s = 0 # suffrages
    nsieges = sum([ siegesParParti[p][0] for p in partis.values() ] )
    if "Vaud"==arr: facteur = sum([ p.suffrages*p.fudge for p in partis.values()])/nsieges
    else: facteur = sum([ p.total_par_commune[arr]*p.fudge for p in partis.values()])/nsieges
    for p in siegesParParti.keys():  # boucle sur le parti
        if maxx and p.apparentement not in ["Centre","PVL"]: continue
        # print(len(y_pos[:-2]),len(siegesParParti[p]),len(base))
        plt.barh(y_pos[:-2],siegesParParti[p],color=p.couleur,left=base)  # garde les 2 derniers pour les suffrages
        if "Vaud"==arr : plt.barh(y_pos[-1], p.suffrages*p.fudge/facteur, color=p.couleur,left=base_s,label=p.nom)
        else: plt.barh(y_pos[-1], p.total_par_commune[arr]*p.fudge/facteur, color=p.couleur,left=base_s,label=p.nom)
        base = [ b+s for b,s in zip(base,siegesParParti[p]) ]
        if "Vaud"==arr: base_s += p.suffrages*p.fudge/facteur
        else: base_s += p.total_par_commune[arr]*p.fudge/facteur

    #texte
    pvl = partis["PVL"]
    for i in range(len(apps)):
        if siegesParParti[pvl][i]>0:
             plt.text(siegesParParti[pvl][i]-0.3, i - .45, str(siegesParParti[pvl][i]), color='blue', fontsize=7, horizontalalignment='right')
    if "Vaud"==arr:
        plt.text(pvl.suffrages*pvl.fudge/facteur/2, len(apps)+1 - .45,
                             "{0:.1f}%".format(100*pvl.suffrages*pvl.fudge/sum([ p.suffrages*p.fudge for p in partis.values()])), color='blue', fontsize=7, horizontalalignment='center')
    else:  plt.text(pvl.total_par_commune[arr]*pvl.fudge/facteur/2, len(apps)+1 - .45,
                             "{0:.1f}%".format(100*pvl.total_par_commune[arr]*pvl.fudge/sum([ p.total_par_commune[arr]*p.fudge for p in partis.values()])), color='blue', fontsize=7, horizontalalignment='center')
    
    labels = [printApps(a) for a in apps]
    labels.extend(["", "Suffrages"])  # garde les 2 derniers pour les suffrages
    plt.yticks(y_pos, labels=labels, fontsize = fontAxis['size'])
    plt.ylabel('Apparentements')
    plt.xlabel('Sièges'.format(arr))
    if not fudge: ff = ""
    elif fudge>0: ff = " - PVL à +{0}%".format(fudge)
    else: ff = " - PVL à {0}%".format(fudge)
    if "Vaud"==arr : plt.title("Canton de {0}{1}".format(arr,ff))
    else : plt.title("Arrondissement de {0}{1}".format(arr,ff))
    if not maxx: plt.legend(loc="lower right")
    if maxx: plt.xlim(0,maxx)

    if fudge:
        if maxx: deuxPlots("Apparentements-{0}-fudge{1}-max{2}".format(goodName(arr),fudge,maxx))
        else: deuxPlots("Apparentements-{0}-fudge{1}".format(goodName(arr),fudge))
    else:
        if maxx: deuxPlots("Apparentements-{0}-max{1}".format(goodName(arr),maxx))
        else: deuxPlots("Apparentements-{0}".format(goodName(arr)))
        
    plt.clf()

#############################
def graphiquesGC(partis,arrondissements,fudge=None):
    """
    Les graphiques du GC
    """
    partis_centre = [ partis["PVL"], partis["Centre"], partis["Libres"], partis["PEV"], partis["UDF"] ]
    apps = apparentementsValides(partis_centre)
    print("Il y a {0} apparentements possibles".format(len(apps)))
#    for p in apps: print(p)
    totalSieges = [{} for a in apps]
    # print("totalSieges est {0}".format(totalSieges))
    for arr in arrondissements.keys():
        combDeSieges = []  # liste de même taille que apps
        if not fudge: print("## Arr. {0}".format(arr))
        for p in apps:
            combDeSieges.append(distribueSieges(arr,p,partis))
        plotSieges(arr,apps,combDeSieges,partis,fudge=fudge)
        # somme
        for i in range(len(combDeSieges)):
            for p,s in combDeSieges[i].items():
                if p in totalSieges[i].keys(): totalSieges[i][p]+=s
                else: totalSieges[i][p]=s
    # print("### Total {0} ###".format(totalSieges))
    plotSieges("Vaud",apps,totalSieges,partis,maxx=None,fudge=fudge)
    plotSieges("Vaud",apps,totalSieges,partis,maxx=25,fudge=fudge)
