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
from Utilities import goodName

plt.figure(figsize=(7,5))
fig, ax = plt.subplots()
fontAxis = {'size'   : 5}
#############################################################################
def deuxPlotsGC(nom):
    """
    Crée un pdf et un png
    """
    plt.savefig("GC-pdf/{0}.pdf".format(nom),transparent=True)
    plt.savefig("GC-png/{0}.png".format(nom),transparent=True)

#############################################################################
class Apparentement():
    """
    Un apparentement de partis
    """
    def __init__(self,partis,nom=None):
        if isinstance(partis,tuple): self.partis = list(partis)
        elif isinstance(partis,set): self.partis = list(partis)
        elif not isinstance(partis,list): self.partis = [partis]
        else: self.partis = partis
        self.nom = nom

        # PVL first
        PVL = None
        for p in self.partis:
            if 'PVL' == p.nom: PVL = p
        if PVL:
            self.partis.remove(PVL)
            self.partis.insert(0, PVL)     
        
        # total
        self.sieges_par_arrondissement = {} 
        # print("Apparentement de {0}".format(self))

    def total_par_arrondissement(self,arr):
        """
        calcule le total à chaque fois vu que p.fudge peut changer
        """
        if "Vaud"==arr : return sum([ p.suffrages*p.fudge for p in self.partis ])
        else: return sum([ p.total_par_commune[arr]*p.fudge for p in self.partis ])        

    def __repr__(self):
        if self.nom: return self.nom
        r = "[ "
        for p in self.partis: r+=p.nom+", "
        return r[:-2]+" ]"   # supprime `, ` et replace par ` ]`

    def attribueSieges(self,ns,arr):
        """
        attribue les sieges pour un arrondissement et distribue sur les partis
        """
        resultats = { p: p.total_par_commune[arr]*p.fudge for p in self.partis }
        self.sieges_par_arrondissement[arr] = GrandConseil( resultats, ns )
        #print("attribueSieges {0} arr {1}:".format(self.__repr__(),arr))
        #for p in self.partis: print("    {0}*{1}: {2}".format(p.total_par_commune[arr],p.fudge, self.sieges_par_arrondissement[arr][p]))

def compareApparentements(a1,a2):
    """
    Compare 2 apparentements
    """
    for p1 in a1.partis:
        for p2 in a2.partis:
            if p1==p2: return False
    return True
        
#############################################################################
class Scrutin():
    """
    Une système d'apparentements 
    """
    def __init__(self,apps):                    
        if isinstance(apps,list): self.apps = apps
        else: self.apps = [apps]
        for a1 in self.apps:
            for a2 in self.apps:
                if a1!=a2 and not compareApparentements(a1,a2):
                    print("Je ne peux pas créer de Scrutin avec {0} et {1}".format(a1,a2))
                    sys.exit()

    def __repr__(self):
        """
        imprime un ensemble d'apparentements
        """
        r = ""
        for a in self.apps:
#            print(a.nom)
            if a.nom!='Gauche': r += "{0}, ".format(a)  # inutile d'imprimer Gauche
#        print(r[:-2])
        return r[:-2]

    def partis(self):
        """
        Les partis impliqués
        """
        p = []
        for a in self.apps: p.extend(a.partis)
        return p
        
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
def apparentementsValides(partis):
    """
    Toutes les hypothèses d'apparentements possibles

    Les apparentements de PEV, UDF, Libres sont sous le quorum et donc ignorés.
    """
    # Autour du PVL
    optionsPVL = [
        Apparentement([ partis['PVL'] ]), 
        Apparentement([ partis['PVL'], partis['Libres'] ]), 
        Apparentement([ partis['PVL'], partis['Libres'],  partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['Libres'],  partis['PEV']]), 
        Apparentement([ partis['PVL'], partis['Libres'],  partis['PEV'], partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['PEV']]), 
        Apparentement([ partis['PVL'], partis['PEV'], partis['UDF']]), 
        #
    ]
    optionsPVLCentre = [
        Apparentement([ partis['PVL'], partis['Centre'] ]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['Libres'] ]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['Libres'],  partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['Libres'],  partis['PEV']]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['Libres'],  partis['PEV'], partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['UDF']]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['PEV']]), 
        Apparentement([ partis['PVL'], partis['Centre'], partis['PEV'], partis['UDF']])
    ]
    # Autour du centre
    optionsCentre = [
        Apparentement([ partis['Centre'] ]), 
        Apparentement([ partis['Centre'], partis['Libres'] ]), 
        Apparentement([ partis['Centre'], partis['Libres'],  partis['UDF']]), 
        Apparentement([ partis['Centre'], partis['Libres'],  partis['PEV']]), 
        Apparentement([ partis['Centre'], partis['Libres'],  partis['PEV'], partis['UDF']]), 
        Apparentement([ partis['Centre'], partis['UDF']]), 
        Apparentement([ partis['Centre'], partis['PEV']]), 
        Apparentement([ partis['Centre'], partis['PEV'], partis['UDF']])
    ]
    # La Gauche
    laGauche = [
        Apparentement([partis['PST/Sol.'], partis['VERT-E-S'], partis['PS'], partis['Pirates'] ], nom='Gauche'), # Gauche
    ]
    lesPetits = [
        Apparentement([ partis['Libres'],  partis['PEV'], partis['UDF'] ]), # Les petits
    ]
    # La Droite
    optionsDroite = [
        Apparentement([ partis['UDC'], partis['PLR'] ]), # Droite
        Apparentement([ partis['UDC'], partis['PLR'], partis['Centre'] ]), # Droite
        Apparentement([ partis['UDC'], partis['PLR'], partis['UDF'] ]), # Droite
        Apparentement([ partis['UDC'], partis['PLR'], partis['Centre'], partis['UDF']]), # Droite
    ]
    return optionsPVL, optionsPVLCentre, optionsCentre, laGauche, optionsDroite, lesPetits
    
#######################################################
def genereScrutins(partis):
    """
    La combinatoire des scrutins
    """
    scrutins = []
    optionsPVL, optionsPVLCentre, optionsCentre, laGauche, optionsDroite, lesPetits = apparentementsValides(partis)
    g = laGauche[0] # pas besoin de boucler
    # options PVL sans le centre
    for p in optionsPVL:
        for c in optionsCentre: # Centre à part
            if not compareApparentements(p,c): continue  # overlap
            for d in optionsDroite:
                if not compareApparentements(p,d): continue  # overlap
                if not compareApparentements(c,d): continue  # overlap
                scrutins.append(Scrutin([p,c,d,g]))          # c'est valable
                # print("Nouveau Scrutin valable {0}".format(scrutins[-1]))
        for d in optionsDroite: # options avec le centre dans la droite
            if not partis['Centre'] in d.partis: continue
            if not compareApparentements(p,d): continue  # overlap
            scrutins.append(Scrutin([p,d,g]))          # c'est valable
            # print("Nouveau Scrutin valable {0}".format(scrutins[-1]))
            
    # maintenant les option PVL-centre
    for pc in optionsPVLCentre: # PVL avec Centre
        for d in optionsDroite:
            if not compareApparentements(pc,d): continue  # overlap
            scrutins.append(Scrutin([pc,d,g]))          # c'est valable
            # print("Nouveau Scrutin valable {0}".format(scrutins[-1]))

    # si les petits ne sont dans aucun scrutin, je les ajoute
    x = lesPetits[0]
    for s in scrutins:
        if len(set(s.partis()).intersection(set(x.partis)))==0:
            print("{0} ne contient aucun petit. Je les ajoute.".format(s))
            s.apps.append(x)
            print("    J'obtiens {0}".format(s))
            
    for s in scrutins: print("{0}\\\\[1pt]".format(s))
    scrutins.reverse()
    return scrutins
    
#######################################################
def distribueSieges(arr,scrutin,partis,fudge=0.,debug=False):
    """
    Distribue les sièges de l'arrondissement
    """
    debug = False
    sieges_partis = {}
    if debug: print("Je teste les apparentements {0}".format(scrutin))
    resultats = { a: a.total_par_arrondissement(arr) for a in scrutin.apps }
    resultats5 = { a: resultats[a] if resultats[a]/sum(resultats.values())>=_quorum else 0 for a in scrutin.apps } # quorum
    if debug: print(resultats,resultats5)
    sieges = GrandConseil(resultats5, _sieges[arr] )
    for a,s in sieges.items():
        a.attribueSieges(s,arr)  # distribue sur les partis
        if debug: print("     {0}: l'apparentement {1} fait {2} suffrages et {3} sièges".format(arr,a,a.total_par_arrondissement(arr),sieges[a]))
        for p in a.partis:
            if a.sieges_par_arrondissement[arr][p]>0 and debug: print("         {0} fait {1} siège(s) à {2}".format(p,a.sieges_par_arrondissement[arr][p],arr))
            if p in sieges_partis.keys():
                print("{0} est dans plusieurs apparentements".format(p))
                sys.exit()
            sieges_partis[p] = a.sieges_par_arrondissement[arr][p]
    for p in partis.values():
        if p not in sieges_partis.keys(): sieges_partis[p] = 0 # si les petits partis ne sont pas dans un apparementement ils n'ont pas de siege
    return sieges_partis

####################################################
def plotSieges(arr,combDeSieges,partis,maxx=None,fudge=None,fudgeParti="PVL"):
    """
    graphique des sièges

    arr: arrondissement de vote
    scrutins: apparentements considérés (liste)
    combDeSieges [ {parti: siege,...}, {}...] : combinaisons de sièges par parti. Liste de même taille que scrutins.
    partis: tous les partis
    """
    # redistribue les sieges par parti
    siegesParParti = {}
    # print(combDeSieges)
    for p in partis.values(): siegesParParti[p] = [ c[p] for c in combDeSieges.values() ]
    # print("Arrondissement {0} - PVL: {1}".format(arr,siegesParParti[partis['PVL']]))

    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.34)
    y_pos = np.arange(len(combDeSieges.keys())+2)

    base = [0]*len(combDeSieges.keys()) # sieges
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
    for i in range(len(combDeSieges.keys())):
        if siegesParParti[pvl][i]>0:
             plt.text(siegesParParti[pvl][i]-0.3, i - .45, str(siegesParParti[pvl][i]), color='blue', fontsize=fontAxis['size'], horizontalalignment='right')
    if "Vaud"==arr:
        plt.text(pvl.suffrages*pvl.fudge/facteur/2, len(combDeSieges.keys())+1 - .45,
                 "{0:.1f}%".format(100*pvl.suffrages*pvl.fudge/sum([ p.suffrages*p.fudge for p in partis.values()])), color='blue', fontsize=fontAxis['size'],
                 horizontalalignment='center')
    else:  plt.text(pvl.total_par_commune[arr]*pvl.fudge/facteur/2, len(combDeSieges.keys())+1 - .45,
                    "{0:.1f}%".format(100*pvl.total_par_commune[arr]*pvl.fudge/sum([ p.total_par_commune[arr]*p.fudge for p in partis.values()])), color='blue',
                    fontsize=fontAxis['size'], horizontalalignment='center')
    
    labels = [s for s in combDeSieges.keys()]
    labels.extend(["", "Suffrages"])  # garde les 2 derniers pour les suffrages
    plt.yticks(y_pos, labels=labels, fontsize = fontAxis['size'])
    plt.ylabel('Apparentements')
    plt.xlabel('Sièges'.format(arr))
    if not fudge: ff = ""
    elif fudge>0: ff = " - {1} à +{0}%".format(fudge,fudgeParti)
    else: ff = " - {1} à {0}%".format(fudge,fudgeParti)
    if "Vaud"==arr : plt.title("Canton de {0}{1}".format(arr,ff))
    else : plt.title("Arrondissement de {0}{1}".format(arr,ff))
    if not maxx: plt.legend(loc="lower right")
    if maxx: plt.xlim(0,maxx)

    if fudge:
        if "PVL"==fudgeParti : ff = "fudge{0}".format(fudge)
        else: ff = "fudge{0}-{1}".format(fudge,fudgeParti)
        if maxx: deuxPlotsGC("Apparentements-{0}-{1}-max{2}".format(goodName(arr),ff,maxx))
        else: deuxPlotsGC("Apparentements-{0}-{1}".format(goodName(arr),ff))
    else:
        if maxx: deuxPlotsGC("Apparentements-{0}-max{1}".format(goodName(arr),maxx))
        else: deuxPlotsGC("Apparentements-{0}".format(goodName(arr)))
        
    plt.clf()

#######################################################################################
def graphiquesGC(partis,scrutins,arrondissements,fudge=0,fudgeParti="PVL"):
    """
    Les graphiques du GC
    """
#    for p in scrutins: print(p)
    totalSieges = {a : {} for a in scrutins}
    # print("totalSieges est {0}".format(totalSieges))
    pvl = {}
    for arr in arrondissements.keys():
        combDeSieges = {s : distribueSieges(arr,s,partis) for s in scrutins}  #
        pvl[arr] = { s : combDeSieges[s][partis['PVL']] for s in scrutins} # pour la table
        plotSieges(arr,combDeSieges,partis,fudge=fudge,fudgeParti=fudgeParti)
        # somme
        for i in combDeSieges.keys():
            for p,s in combDeSieges[i].items():
                if p in totalSieges[i].keys(): totalSieges[i][p]+=s
                else: totalSieges[i][p]=s
    # print("### Total {0} ###".format(totalSieges))
    plotSieges("Vaud",totalSieges,partis,maxx=None,fudge=fudge,fudgeParti=fudgeParti)
    plotSieges("Vaud",totalSieges,partis,maxx=25,fudge=fudge,fudgeParti=fudgeParti)
    grandeTable(pvl,totalSieges,partis,fudge=fudge,fudgeParti=fudgeParti)
    
    return totalSieges

#############################centre

def plotVariations(s,pvl,centre,score,partis,nom="PVL",tiers=None):
    """
    Variation avec le score du PVL 
    """
    # print("input",s,parti)
    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.10)
    pvls = dict(sorted(pvl.items(), key=lambda item: item[0]))
    plt.plot([ score*(100+v) for v in pvls.keys()],   pvls.values(),'o-',color=partis['PVL'].couleur,label='PVL',linewidth=2)
    centres = dict(sorted(centre.items(), key=lambda item: item[0]))
    plt.plot([ score*(100+v) for v in centres.keys()], centres.values(),'.-',color=partis['Centre'].couleur,label='Centre') 
    if tiers:
        tierss = dict(sorted(tiers.items(), key=lambda item: item[0]))
        plt.plot([ score*(100+v) for v in tierss.keys()], tiers.values(),'s-',color=partis[nom].couleur,label=nom)  # normaliser à 100-score?

    plt.axvline(x = 100*score, color = partis[nom].couleur) # barre 
    plt.ylabel('Sièges')
    plt.xlabel('Résultat du {0} [%]'.format(nom))
    plt.title('{0}'.format(s))
    plt.legend(loc="upper left")
    plt.ylim(0,17)
    deuxPlotsGC("Apparentements-{1}-Sieges-{0}".format(goodName(s.__repr__()),nom))
    plt.clf()
    
#############################
def pasZero(v):
    """
    N'imprime pas les 0
    """
    if 0==v: return ""
    else: return str(v)
#############################
def grandeTable(pvl,totalSieges,partis,fudge=0,fudgeParti="PVL"):
    """
    La grande table de tout
    """
    debug = False and 0==fudge
    if debug: print("Grande table")
    ordre = [ partis['PVL'], partis['Centre'], partis['UDC'], partis['PLR'], partis['PS'], partis['VERT-E-S'], partis['PST/Sol.'] ]
    if partis[fudgeParti] not in ordre: ordre.append(partis[fudgeParti])
    bonsArr = list(pvl.keys())
    bonsArr.remove('La Vallée')   # toujours 0
    bonsArr.remove("Pays d'En Haut")
#    print(bonsArr)
    import codecs
    ff = "-{0}-{1}".format(fudge,fudgeParti)
    with codecs.open("tables/grandeTable{0}.tex".format(ff),'w',"ISO-8859-1") as f:
        f.write("\\begin{tabular}{l|ccccccccccc|r||")
        f.write('r'*len(ordre))
        f.write("}\n \\toprule\n")
        f.write(" & \\multicolumn{12}{c||}{Sièges du PVL} & \\multicolumn{6}{c}{Autres partis} \\\\ \n")
        thehead = "Hypothèse "
        for a in bonsArr: thehead +=" & \\rotatebox{90}{"+a+"}"
        for p in ordre : thehead +=" & \\rotatebox{90}{"+p.nom+"}"
        thehead+="\\\\ \\midrule"
        if debug: print(thehead)
        f.write(thehead+" \n")
        f.write("Résultats EC 2022 & 1 &  & 1 & 2 & 1 & 2 & 3 & 1 &  & 1 &  & 10 &  & 21 & 50 & 32 & 25 & 7 \\\\") # plus un libre qui siège avec nous
        f.write("\\midrule \n")
        for s,resultat in reversed(totalSieges.items()):  # inverse pour avoir le même ordre que dans les plots
            theline = "{}"+" {0} ".format(s)
            for a in bonsArr: theline += "& {0} ".format(pasZero(pvl[a][s]))
            for p in ordre: theline += "& {0} ".format(pasZero(resultat[p]))
            theline += "\\\\"
            if debug: print(theline)
            f.write(theline+" \n")
        f.write("\\bottomrule\\end{tabular}\n")
        f.close()

