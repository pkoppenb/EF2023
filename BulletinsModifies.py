"""
Questions auxquelles je veux répondre pour le PVL:
Nos listes:
1. Sur quelles listes faisons-nous des suffrages?
2. Quelles listes font des suffrages chez nous?
3. Quels candidats font des suffrages chez nous?

Candidats:
1. Combien de suffrages sur chaque liste? Et comparaison avec la moyenne.
2. Qui d'autre est sur ces listes?
3. Sur les listes où je suis doublé, qui est biffé?
4. Sur les listes où je suis biffé, qui est ajouté ou doublé?
5. Qui sont mes amis qui se trouvent souvent avec moi

Arrondissements pour le Grand Conseil:
1. Quels apparenetement produisent quels résultats?
2. Quelle est leur stabilité si je varie les résultats.
"""
        
#############################################################################
# main
#############################################################################
from Utilities import lisScrutin,lisBulletins,lisOFS,lisCommunes,lisArrondissements,attribueListes,_sieges,analyseBilans, correlations, goodName, analyseChi2,_elus,fixArrondissements,ajouteArrondissements,_suffragesExprimes
import sys
#############################################################################
# args
#############################################################################
import argparse
parser = argparse.ArgumentParser(description="configuration")
parser._action_groups.pop()
optional = parser.add_argument_group("optional arguments")
optional.add_argument("-v", "--Vaud", dest="Vaud", action="store_true", help="Graphiques pour Vaud")
optional.add_argument("-p", "--partis", dest="partis", action="store_true", help="Graphiques pour partis")
optional.add_argument("-l", "--listes", dest="listes", action="store_true", help="Graphiques pour listes")
optional.add_argument("-c", "--communes", dest="communes", action="store_true", help="Graphiques pour communes - ça met du temps")
optional.add_argument("-cd", "--candidats", dest="candidats", action="store_true", help="Graphiques pour candidats")
optional.add_argument("-a", "--arrondissements", dest="arrondissements", action="store_true", help="Graphiques pour arrondissements de vote (arrondissements)")
optional.add_argument("-corr", "--correlations", dest="corr", action="store_true", help="Graphiques de correlations de partis")
optional.add_argument("-g", "--grandConseil", dest="GC", action="store_true", help="Graphiques pour le Grand Conseil")
args = parser.parse_args()
#############################################################################
# lecture
#############################################################################
listes,partis = lisScrutin()
candidats,bulletins = lisBulletins(listes,partis)
attribueListes(candidats,listes)
Vaud,communes = lisOFS(partis)
lisCommunes(communes,candidats,listes)
# arrondissements
arrondissements = lisArrondissements(communes)
ajouteArrondissements(listes,partis,arrondissements,communes,candidats)
fixArrondissements(arrondissements,Vaud,partis)

pd = sum([b.poids for b in bulletins])
sf = sum([b.exprimes*b.poids for b in bulletins])
# le nombre de complémentaires ne correspond pas à ce que je trouve dans le fichier
# des bulletins modifiés. Si je l'ajoute ici ça marche.
nm = sum([p.suffrages_liste_complete+p.suffrages_comp_liste_modifiee for p in listes.values()])
total_des_suffrages = sf+nm
if total_des_suffrages!=_suffragesExprimes :
    print("Je vois {0} suffrages mais en attends {1}".format(total_des_suffrages,_suffragesExprimes))
    sys.exit()
        

print("#############################################################################")
print("### J'ai {0} listes de {1} partis et {2} candidats".format(len(listes),len(partis),len(candidats)))
print("### Il y a {0} bulletins modifiés ({1} différents) qui font {2} suffrages ({3:.1f}%)".format(pd,len(bulletins),sf,100.*sf/total_des_suffrages))
print("### Et {0:.0f} bulletins non modifiés, soit {1} suffrages ({2:.1f}%)".format(nm/_sieges,nm,100.*nm/total_des_suffrages))
print("#############################################################################")

# suffrages par candidats
for c in candidats.values():
    c.analyse(bulletins)
              
# mise à jour des suffrages par parti
for p in partis.values(): p.miseAjour(listes)

for l in listes.values(): l.check()
for p in partis.values(): p.check()

# vérification
print("##################################################################################")
# print("Listes: {0}".format( listes ))
for p in listes.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_liste.values()]))
print("##################################################################################")
# print("Partis: {0}".format( partis.keys() ))
for p in partis.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_liste.values()],p.suffrages))
print("##################################################################################")
print(args)

# graphiques pour Vaud
if args.Vaud:
    print("### VAUD ###")
    Vaud.partis(listes,normalise=False)
    Vaud.partis(partis,normalise=True)
    Vaud.candidats(candidats)
    Vaud.candidats(candidats,avecBase=True)
    Vaud.candidats(candidats,parti="Centres")

# graphiques pour les partis
if args.partis:
    print("### PARTIS ###")
    bilans = {}
    somme = 0.
    for p in partis.values():
        p.pourcentage = 100.*p.suffrages/total_des_suffrages
        print("Parti {0} : {1:0.1f}% ({2})".format(p.nom,p.pourcentage,p.suffrages))
        somme+= p.suffrages
        p.plotSuffrages(partis)
        para = p.parasite(partis)
        bilans[p] = p.bilan(para)
        p.candidatsParasites(candidats)
        p.communes(communes)
        p.communes(communes,pires=True)  # pires
        p.communes(communes,grandes=True)  # grandes
        p.communes(arrondissements,circonscription="Arrondissement")
        Vaud.candidats(candidats,parti=p.nom)
        Vaud.candidats(candidats,parti=p.nom,avecBase=True)

    print("Total des suffrages {0:.0f} au lieu de {1:.0f}. Différence {2}.".format(somme,total_des_suffrages,somme-total_des_suffrages))

    analyseBilans(bilans)

if args.corr:
    print("### CORRELATIONS ###")
    for p in partis.values():
        for q in partis.values():
            if p==q : continue
            correlations(p,q,communes,Vaud)
            correlations(p,q,arrondissements,Vaud,circonscription="Arrondissement")

# graphiques pour les listes
if args.listes:
    print("### LISTES ###")
    bilans = {}
    somme = 0.
    for l in listes.values():
        l.pourcentage = 100.*l.suffrages/total_des_suffrages
        print("Liste {0} : {1:0.1f}% ({2})".format(l.nom,l.pourcentage,l.suffrages))
        somme += l.suffrages
        l.communes(communes)
        l.communes(communes,pires=True)  # pires
        l.communes(arrondissements,circonscription="Arrondissement")
        l.biffageDoublage()
        l.suffragesParCandidat()
        l.plotSuffrages(listes)
        para = l.parasite(listes)
        bilans[l] = l.bilan(para)
        #    if l.parti.nom == "PVL" :
        l.candidatsParasites(candidats)

    print("Total des suffrages {0:.0f} au lieu de {1:.0f}. Différence {2}.".format(somme,total_des_suffrages,somme-total_des_suffrages))
    analyseBilans(bilans)

# graphiques pour les communes
if args.communes:
    print("### COMMUNES ###")
    chi2 = {}
    for c in communes.values():
        chi2[c] = c.chi2(Vaud)
        print("\\Commune[{0}]{{{1}}} % {2}".format(c.nom,goodName(c.nom),len(chi2)))
        c.partis(listes,normalise=False)
        c.partis(partis,normalise=True)
        c.candidats(candidats)
        c.candidats(candidats,avecBase=True)
        c.candidats(candidats,parti="PVL")
        c.candidats(candidats,parti="PVL",avecBase=True)
        c.candidats(candidats,parti="Centres")
        # if len(chi2)==25: analyseChi2(chi2)
    analyseChi2(chi2)

# graphiques pour les arrondissements
if args.arrondissements:
    print("### ARRONDISSEMENTS ###")
    for a in arrondissements.values():
        a.partis(listes,normalise=False,circonscription="Arrondissement")
        a.partis(partis,normalise=True,circonscription="Arrondissement")
        a.candidats(candidats,circonscription="Arrondissement")
        a.candidats(candidats,avecBase=True,circonscription="Arrondissement")
        a.candidats(candidats,parti="PVL",circonscription="Arrondissement")
        a.candidats(candidats,parti="PVL",avecBase=True,circonscription="Arrondissement")
        a.candidats(candidats,parti="Centres",circonscription="Arrondissement")
        # if len(chi2)==25: analyseChi2(chi2)


# graphiques pour les candidats
if args.candidats:
    print("### CANDIDATS ###")
    for c in candidats.values():
        if c.liste.parti.nom == "PVL" or c.nom in _elus:
            #        print("Candidat {0} liste {1} parti {2}".format(c.nom,c.liste.nom,c.liste.parti.nom))
            print("\\Candidat{{{0}}}{{{1}}} % {2}".format(goodName(c.nom),c.nom,c.liste.nom))
            c.communes(communes)
            c.communes(communes,False)
            c.communes(arrondissements)
            c.communes(arrondissements,False)
            c.listes(listes)
            c.amis(candidats,listes)
            c.biffage(candidats,listes, unique=False)
            c.biffage(candidats,listes, unique=True)
           
# graphiques pour le GC
from GrandConseil import apparentementsValides, distribueSieges, plotSieges
if args.GC:
    print("### Grand Conseil ###")
    partis_centre = [ partis["PVL"], partis["Centre"], partis["Libres"], partis["PEV"], partis["UDF"] ]
    apps = apparentementsValides(partis_centre)
    print("Il y a {0} apparentements possibles".format(len(apps)))
    for p in apps: print(p)
    for arr in arrondissements.keys():
        combDeSieges = []  # liste de même taille que apps
        print("## Arr. {0}".format(arr))
        for p in apps:
            combDeSieges.append(distribueSieges(arr,p,partis))
        plotSieges(arr,apps,combDeSieges,partis)
