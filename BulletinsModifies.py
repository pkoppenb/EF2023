import csv

_file = 'export-bulletins-PR-CHCN-20231022.csv'
_summary = 'ScrutinsParListe.csv'
_communes = 'CHCN20231022.csv'
_partis = 'sd-t-17.02-NRW2023-parteien-appendix.csv'
_sd = "Sans dénom."
_suissesDeLetranger1 = 9999   # chez les vaudois
_suissesDeLetranger2 = 19220   # chez l'OFS
_max = 25 # numbre maximal de lignes
_sieges = 19   # 19 sieges
_moitie = int(_sieges/2.+1)   # il faut 10 pour avoir la moitié
_vaud = 7.5366869013
_elus = ['Maillard Pierre-Yves',
         'Nordmann Roger',
         'Bendahan Samuel',
         'Crottaz Brigitte',
         'Tschopp Jean',
         'Jaccoud Jessica',
         'Tuosto Brenda',
         'de Quattro Jacqueline',
         'Broulis Pascal',
         'Feller Olivier',
         'Wehrli Laurent',
         'Ruch Daniel',
         'Michaud Gigon Sophie',
         'Mahaim Raphaël',
         'Porchet Léonore',
         'Nicolet Jacques',
         'Buffat Michaël',
         'Pahud Yvan',
         'Freymond Sylvain',
         'Weber Céline',
         'Chappuis Isabelle' ]

grandesCommunes = {  # de wikipedia
    'Lausanne' : 5586, # 	Lausanne 	141 418 	41,38 	3418
    'Yverdon-les-Bains' :  	5938, # 	Jura-Nord vaudois 	29 827 	11,28 	2644
    'Montreux' :  	5886, # 	Riviera-Pays-d'Enhaut 	26 230 	33,37 	786
    'Nyon' :  	5724, # 	Nyon 	22 465 	6,79 	3309
    'Renens' :  	5591, # 	Ouest lausannois 	21 086 	2,96 	7124
    'Vevey' :  	5890, # 	Riviera-Pays-d'Enhaut 	19 738 	2,38 	8293
    'Pully' :  	5590, # 	Lavaux-Oron 	18 984 	5,85 	3245
    'Morges' :  	5642, # 	Morges 	17 529 	3,85 	4553
    'Gland' :  	5721, # 	Nyon 	13 664 	8,32 	1642
    'Écublens' :  	5635, # 	Ouest lausannois 	13 118 	5,71 	2297
    'La Tour-de-Peilz' :  	5889, # 	Riviera-Pays-d'Enhaut 	12 382 	3,24 	3822
    'Prilly' :  	5589, # 	Ouest lausannois 	12 294 	2,19 	5614
    'Blonay Saint-Légier' : 	5892, # 	Riviera-Pays-d'Enhaut 	12 117 	31,24 	388
    'Aigle' :  	5401 , #	Aigle 	10 913 	16,41 	665
    'Lutry' :  	5606, # 	Lavaux-Oron 	10 718 	8,45 	1268
    'Bussigny' :  	5624, # 	Ouest lausannois 	10 365 	4,82 	2150
    'Payerne' :  	5822, # 	Broye-Vully 	10 342 	24,19 	428
    'Épalinges' :  	5584, # 	Lausanne 	9 822 	4,57 	2149
    'Le Mont-sur-Lausanne' :  	5587, # 	Lausanne 	9 291 	9,82 	946
    'Crissier' :  	5583, # 	Ouest lausannois 	9 181 	5,51 	1666
    'Chavannes-près-Renens' :  	5627, # 	Ouest lausannois 	8 737 	1,65 	5295
    'Bex' :  	5402, # 	Aigle 	8 167 	96,56 	85
    'Ollon' :  	5409, # 	Aigle 	7 968 	59,56 	134
    'Orbe' :  	5757, # 	Jura-Nord vaudois 	7 613 	12,02 	633
    'Rolle' :  	5861, # 	Nyon 	6 322 	2,74 	2307
    'Moudon' :  	5678, # 	Broye-Vully 	6 124 	15,69 	390
    'Oron':  5805, # 	Lavaux-Oron 	6 114 	26,28 	233
    }
    

         
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
plt.figure(figsize=(7,5))
fig, ax = plt.subplots()

def goodName(name):
    name2 = name.replace("VERT'LIBÉRAUX-ENGAGÉS POUR DEMAIN","ENGAGÉS POUR DEMAIN").replace("VERT'LIBÉRAUX-JEUNES VERT'LIBÉRAUX","JEUNES VERT'LIBÉRAUX").replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace(">","_g_").replace("<","_l_").replace("*","_times_").replace(".","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_").replace("||","_or_").replace("&&","_and_").replace("&","_").replace("|","_").replace(":","_vs_").replace("'","_").replace("#","N").replace('·','_').replace('É','E').replace('à','a').replace('é','e').replace('è','e').replace('ë','e').replace('ä','a').replace('ç','c').replace('ï','i').replace('â','a').replace('ô','o').replace('ê','e').replace('ë','e').replace('__','_')
    return name2

def incrementeOuCree(dico,cle,valeur):
    if cle in dico.keys(): dico[cle] += valeur
    else: dico[cle] = valeur

def deuxPlots(nom):
    """
    Crée un pdf et un png
    """
    plt.savefig("pdf/{0}.pdf".format(nom),transparent=True)
    plt.savefig("png/{0}.png".format(nom),transparent=True)

def tableau(nom,lignes,colonnes):
    """
    Crée un tableau de données en csv
    """
    # print("tableau avec {0} et {1}".format(lignes,colonnes))
    with open("csv/{0}.csv".format(nom),"w") as f:
        # d'abord l'en-tete
        f.write(nom)
        for k in colonnes.keys(): f.write(", {0}".format(k))
        f.write("\n")
        # ensuite chaque ligne
        for i,l in enumerate(lignes):
            f.write(l)
            for k in colonnes.keys(): f.write(", {0}".format(colonnes[k][i]))
            f.write("\n")
    f.close()

#############################################################################
class Bulletin():
    """
    Une catégorie unique de bulletin
    """
    def __init__(self,row,candidats):
#        print("Row {0}".format(row))
        self.poids = int(row[0])
        self.liste = None   # sera attribué plus tard
        self.nom_liste_originale = row[1][3:]  # nom original (permet de retrouver les bulletins sans denom.)
        self.liste_id = int(row[1][:3])
        self.complementaires = int(row[2])
        c_id = list(candidats.keys())  # les identifiants de tous les candidats
        self.suffrages = {}
        for l in range(len(c_id)):   # 
            v = int(row[3+l])        # nombre de voix du candidat l
            if int(v)>0: self.suffrages[ c_id[l] ] = v
        self.exprimes = sum(self.suffrages.values()) # +self.complementaires
#        print(u'Créé bulletin avec poids {0}, liste {1}, complémentaires {2}, suffrages {3}'.format(self.poids,self.liste,self.complementaires,self.suffrages[0:20]))

    def assigneParti(self,listes,partis):
        """
        Trouve le meilleur parti pour listes sans denom.
        """
        if self.nom_liste_originale != _sd:
            self.liste = listes[self.liste_id]
            self.parti = self.liste.parti
        if (sum( self.suffrages.values())<_moitie): return # il me fait au moins 0 voix pour un partu pour ré-assigner
        _partis = {}
        for s in self.suffrages.keys():
            lln = int(s[:2])
            ll = listes[lln]   # 07.01 devient 7 et je prends la liste[7]
#            print("lln {0} ll {1} parti {2}".format(lln,ll.nom,ll.parti.nom))
            incrementeOuCree(_partis,ll.parti.nom,self.suffrages[s])
#            print(_partis)
        _partis2 = dict(sorted(_partis.items(), key=lambda item: item[1], reverse=True))
#        print(_partis2,list(_partis2.keys()))
        _best =  list(_partis2.keys())[0]
        if ( _partis2[_best]>_moitie): self.parti = partis[_best]
        else:
#            print("Le meilleur parti {0} n'a que {1} suffrages".format(_best, _partis2[_best]))
            self.parti = None

    def nombreDeSuffrages(self,numero):
        """
        Nombre de voix du candidat numero 
        """
        if numero not in self.suffrages.keys(): return 0
        else: return self.poids*self.suffrages[numero]

    def double(self,numero):
        """
        A ete double?
        """
        if numero not in self.suffrages.keys(): return False
        else: return (self.suffrages[numero]==2)

    def double_unique(self,numero):
        """
        A ete double?
        """
        if not self.double(numero): return False
        for n,s in self.suffrages.items():
            if s==2 and n!=numero : return False  # il y en a un autre doublé
        return True                               # trouvé aucun autre
        

    def pleine(self):
        """
        Liste pleine?
        """
        return self.exprimes==_sieges

#############################################################################
class Commune():
    """
    Une commune
    """
    def __init__(self,numero,nom):
        self.numero = numero
        self.nom = nom
        self.suffrages = 0
        self.suffrages_par_parti = {}

    def partis(self,partis,normalise=True):
        """
        Résultats par partis dans une commune
        """
        # if "PVL" in partis.keys() : print(self.nom, partis["PVL"].nom,
        #                                  partis["PVL"].compacts_par_commune[self.numero],partis["PVL"].autres_suffrages_par_commune[self.numero])
        if normalise: facteur = 100./self.suffrages
        else: facteur = 1.0
        if list(partis.values())[0].classe=='Liste':  what = "listes"
        else: what = "partis"
        if -1==self.numero :
            #Vaud
            compacts = { k: facteur*sum(list(partis[k].compacts_par_commune.values())) for k in partis.keys() }
            total    = { k: facteur*partis[k].suffrages for k in partis.keys() }
            autres   = { k: total[k]-compacts[k] for k in total.keys() } 
        else:
            compacts = { k: facteur*partis[k].compacts_par_commune[self.numero] for k in partis.keys() }
            autres   = { k: facteur*sum(partis[k].autres_suffrages_par_commune[self.numero].values()) for k in partis.keys() }
            total    = { k: compacts[k]+autres[k] for k in partis.keys() }
        total = dict(sorted(total.items(), key=lambda item: item[1], reverse=False))
        # print("{0}: compacts {1} autres {2} total {3}".format(self.nom, compacts, autres, total))
        
        if "listes"==what: fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        else: fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.12)
        y_pos = np.arange(len(total))
        plt.barh(y_pos,[compacts[k] for k in total.keys()],color=[ partis[k].couleur for k in total.keys()],edgecolor=[ partis[k].couleur for k in total.keys()], label='Compacts' )
        plt.barh(y_pos,[autres[k] for k in total.keys()],left=[compacts[k] for k in total.keys()],edgecolor=[ partis[k].couleur for k in total.keys()], color=['white' for k in total.keys()], label='Modifiés' )
        off = 0.01*list(total.values())[-1]
        for i, v in enumerate(list(total.values())):
            if normalise: plt.text(off+v, i - .25, "{0:.1f}%".format(v), color='black', ha='left', fontsize=9) # horizontal alignment
            else: plt.text(off+v, i - .25, str(int(v)), color='black', ha='left', fontsize=9) # horizontal alignment
        if normalise:
            plt.axvline(x = 5., color = 'b')
            plt.xlabel('Pourcentages des {0}'.format(what))
        else: plt.xlabel('Suffrages des {0}'.format(what))
        plt.title(self.nom)
        plt.xlim([0.,1.15*list(total.values())[-1]])
        plt.yticks(y_pos, labels=[partis[k].nom for k in total.keys()])
        plt.legend()
        deuxPlots("Commune-{0}-{1}s".format(goodName(self.nom),list(partis.values())[0].classe))
        plt.clf()

    def candidats(self,candidats,parti=None,avecBase=False):
        """
        Résultats par partis dans une commune
        """
        modifies = {}
        base = {}
        total = {}
        sl = 0
        for k,c in candidats.items():
            # print(candidats[k].nom,candidats[k].liste.parti.nom,self.numero,c.suffrages,c.liste.suffrages_liste_complete,Parti)
            if ((not parti) or (candidats[k].liste.parti.nom==parti) or
                (parti=="Centres" and (candidats[k].liste.parti.nom in [ "PVL", "Centre", "Libres"]))):
                if -1==self.numero: # Vaud
                    ss = c.suffrages
                    if avecBase: sl = c.liste.suffrages_liste_complete/_sieges
                    # print("Vaud {0}+{1}".format(ss,sl))
                else:
                    ss = sum(list(c.suffrages_par_commune[self.numero].values()))
                    if avecBase: sl = c.liste.compacts_par_commune[self.numero]/_sieges
                    # print("{2}: {0}+{1}".format(self.nom,ss,sl))
                if sl+ss>0:
                    modifies[k] = ss 
                    base[k] = sl
                    total[k] = sl+ss
        total = dict(sorted(total.items(), key=lambda item: item[1], reverse=False))
        # print(modifies)
        nmax = min(_max,len(list(total.values())))
        kk = list(total.keys())[-nmax:]
        vv = list(total.values())[-nmax:]
        
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        y_pos = np.arange(len(kk))
        if avecBase: plt.barh(y_pos,[base[k] for k in kk ],color='white',edgecolor=[candidats[k].liste.couleur for k in kk],height=0.75, label="Listes compactes" )
        plt.barh(y_pos,[modifies[k] for k in kk ],left=[base[k] for k in kk ],color=[candidats[k].liste.couleur for k in kk], label="Listes modifiées" )
        if len(vv)>0:
            off = +0.02*vv[-1]
            for i, v in enumerate(vv):
                plt.text(off+v, i - .25, str(int(v)), color='black', ha='left', fontsize=9) # horizontal alignment
        plt.xlabel('Suffrages des Candidats')
        if parti:
            if "Centres"==parti: plt.title("{0}: candidats des {1}".format(self.nom,parti))
            else: plt.title("{0}: candidats du {1}".format(self.nom,parti))
        else: plt.title("{0}: candidats".format(self.nom))
        if len(vv)>0: plt.xlim([0.,1.15*vv[-1]])
        plt.yticks(y_pos, labels= [candidats[k].nom for k in kk] )
        plt.legend()
        textBase = ""
        if avecBase: textBase = "-avecBase"
        if parti:
            deuxPlots("Commune-{0}-{1}-Candidats{2}".format(goodName(self.nom),goodName(parti),textBase))
        else:
            deuxPlots("Commune-{0}-Candidats{1}".format(goodName(self.nom),textBase))
        plt.clf()

    def chi2(self,Vaud):
        """
        chi2 par rapport au canton
        """
        chi2 = 0.
        # print(self.suffrages_par_parti,Vaud.suffrages_par_parti,self.suffrages,Vaud.suffrages)
        for p,v in self.suffrages_par_parti.items():
            chi2 += (100.*v/self.suffrages-100.*Vaud.suffrages_par_parti[p]/Vaud.suffrages)**2
        # print("% Le chi2 de {0} est {1:.1f}".format(self.nom,chi2))
        return chi2
        
    
#############################################################################
class Liste():
    """
    Liste
    """
    def __init__(self,row):
        self.numero = int(row[0])
        self.nom = row[1]
        self.nomCourt = self.nom.replace("VERT'LIBÉRAUX-ENGAGÉS POUR DEMAIN","ENGAGÉS POUR DEMAIN").replace("VERT'LIBÉRAUX-JEUNES VERT'LIBÉRAUX","JEUNES VERT'LIBÉRAUX")
        self.suffrages_liste_complete = int(row[2])+int(row[3])
        self.suffrages_nom_liste_modifiee = int(row[4])
        self.suffrages_comp_liste_modifiee = int(row[5])
        self.suffrages_autres_listes = int(row[7])
        self.suffrages_sans_denom = int(row[8])
        self.suffrages = self.suffrages_liste_complete+self.suffrages_nom_liste_modifiee+self.suffrages_comp_liste_modifiee+self.suffrages_autres_listes+self.suffrages_sans_denom
        print("{0} reçoit {1}+{2}+{3}+{4}+{5} = {6} suffrages".format(self.nom,self.suffrages_liste_complete,self.suffrages_nom_liste_modifiee,self.suffrages_comp_liste_modifiee,self.suffrages_autres_listes,self.suffrages_sans_denom,self.suffrages))
        self.classe = "Liste"
        self.parti = None  # lien vers parti
        self.suffrages_par_liste = {}
        self.doubles_par_liste = {}
        self.candidats = [ ]
        self.compacts_par_commune = {}           # structure: {commune_id : suffrages }
        self.autres_suffrages_par_commune = {}   # structure: {commune_id : { liste: suffrages}}
        self.total_par_commune = {}              # structure: {commune_id : suffrages }
        # print("Nouvelle liste {0:2} {1} a {2} suffrages".format(self.numero,self.nom,self.suffrages))
        self.pourcentage = 0
        
        if 'Sans' in self.nom:
            self.nom_parti = None
            self.alliance = None
            self.couleur = "black"
        elif 'UDC' in self.nom:
            self.nom_parti = 'UDC'
            self.alliance = 'Droite'
            self.couleur = "darkgreen"
        elif 'SV' in self.nom:
            self.nom_parti = 'PS'
            self.alliance = 'Gauche'
            self.couleur = "red"
        elif 'LR' in self.nom:
            self.nom_parti = 'PLR'
            self.alliance = 'Droite'
            self.couleur = "royalblue"
        elif 'Vert' in self.nom or 'JVVD' in self.nom:
            self.nom_parti = 'VERT-E-S'
            self.alliance = 'Gauche'
            self.couleur = "forestgreen"
        elif 'VERT' in self.nom:
            self.nom_parti = 'PVL'
            self.alliance = 'PVL'
            self.couleur = "yellowgreen"
        elif 'POP' in self.nom:
            self.nom_parti = 'PST/Sol.'
            self.alliance = 'Gauche'
            self.couleur = "maroon"
        elif 'Libres' in self.nom:
            self.nom_parti = 'Libres'
            self.alliance = 'Centre'
            self.couleur = "gold"
        elif 'PPVD' in self.nom:
            self.nom_parti = 'Pirates'
            self.alliance = 'Gauche'
            self.couleur = "khaki"
        elif 'Centre' in self.nom:
            self.nom_parti = 'Centre'
            self.alliance = 'Centre'
            self.couleur = "orange"
        elif 'UDF' in self.nom:
            self.nom_parti = 'UDF'
            self.alliance = 'UDF'
            self.couleur = "gray"
        elif u'EàG' in self.nom:
            self.nom_parti = 'PST/Sol.'
            self.alliance = 'Gauche'
            self.couleur = "maroon"
        elif 'PEV' in self.nom:
            self.nom_parti = 'PEV'
            self.alliance = 'Centre'
            self.couleur = "gainsboro"
        else:
            print("Je ne touve pas {0}".format(self.nom))
            exit()
        
    def connu(self,nom):
        """
        Liste déja existante?
        """
        return self.numero == int(nom.split(' ')[0])
    
    def miseAjour(self, candidat):
        """
        Ajoute les suffrages d'un candidat
        """
#        print("Suffrages du candidat {0}: {1}".format(candidat.nom, candidat.suffrages_par_liste))
#        print("Suffrages du parti    {0}: {1}".format(self.nom, self.suffrages_par_liste))
        self.candidats.append(candidat) # liste des candidats
        # print("{0} {1} suffrages par liste {2}".format(self.classe, self.nom, self.suffrages_par_liste))
        for k in candidat.suffrages_par_liste.keys() :
            self.suffrages_par_liste[k] += candidat.suffrages_par_liste[k]
        for k in candidat.doubles_par_liste.keys() : self.doubles_par_liste[k] += candidat.doubles_par_liste[k]
        # print("Liste {0} a {1} suffrages depuis {2}".format(self.nom,self.suffrages,self.suffrages_par_liste))

    def check(self):
        # print("Check avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(self.autres_suffrages_par_commune[5938][0],0,5938,self.nom))
        s = sum([v for v in self.suffrages_par_liste.values()])
        print("{0} {1}: suffrages: {2}, complète: {3}, modifiée: {4}+{5}, autres listes: {6}, s.d. {7} -> {8} =? {9}"
              .format(self.classe,
                      self.nom,
                      self.suffrages,
                      self.suffrages_liste_complete,
                      self.suffrages_nom_liste_modifiee,
                      self.suffrages_comp_liste_modifiee,
                      self.suffrages_autres_listes,
                      self.suffrages_sans_denom,
                      self.suffrages-self.suffrages_liste_complete-self.suffrages_comp_liste_modifiee,s))
        s1 = sum(list(self.compacts_par_commune.values()))
        s2 = sum([ sum(s.values()) for s in self.autres_suffrages_par_commune.values() ]) # boucle sur autres listes
        s4 = sum(list(self.total_par_commune.values()))
        print("{0} {1}: Somme des suffrages par commune {2} + autres {3}, total {4}".format(self.classe,self.nom,s1,s2,s4))
        if not s==s2 :
            print("{0} {1}: Somme des suffrages par commune {2} + autres {3}, total {4}".format(self.classe,self.nom,s1,s2,s4))
            exit()
        """    
        if self.classe == "Parti" :
            s3 = sum(list(self.total_par_commune.values()))
            print("{0} {1}: Somme des suffrages par commune {2} + autres {3}, parti: {4}".format(self.classe,self.nom,s1,s2,s3))
        else: 
            print("{0} {1}: Somme des suffrages par commune {2} + autres {3}".format(self.classe,self.nom,s1,s2))
        """

    def plotSuffrages(self,listes):
        """
        Fait un plot des suffrages obtenus par origine
        """
        _ll = 'Liste complète'
        colors = {0: "black",    # Liste
                  _sd: "black",  # Parti
                  _ll: self.couleur}  
        suffs = { _ll: self.suffrages_liste_complete}
        for k in self.suffrages_par_liste.keys():
            if k==0 or k==_sd : nom = _sd   # l'un pour Liste l'autre pour Parti
            elif listes[k].nom==self.nom: # C'est ma liste
                nom = 'Liste modifiée'
            else: nom = listes[k].nom
            suffs[nom] = self.suffrages_par_liste[k]
#            print("Pour {0} je cherche {1}".format(self.nom,k))
            if k!=_sd and k!=0 : colors[nom] = listes[k].couleur

        suffs = dict(sorted(suffs.items(), key=lambda item: item[1], reverse=True))

        y_pos = np.arange(len(suffs.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        plt.barh(y_pos,suffs.values(),color=[colors[k] for k in list(suffs.keys())])
        plt.yticks(y_pos, labels=(suffs.keys()))
        plt.xlabel('Suffrages')
        plt.title(self.nom)
        plt.xscale('log')
        plt.xlim([1,10*suffs[_ll]])
        for i, v in enumerate(suffs.values()):
            plt.text(1.02*v, i + .25, str(v), color='blue', fontsize=9)
        plt.gca().invert_yaxis()
        deuxPlots("{0}-Suffrages-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
        plt.xscale('linear')

        fig.subplots_adjust(top=0.90,right=0.90,bottom=0.03,left=0.03)
        plt.title(self.nom)
        explode = [0]*len(suffs)
        explode[0] = 0.1
        _, _, autotexts= plt.pie(suffs.values(),explode=explode,labels=(suffs.keys()),colors=[colors[k] for k in list(suffs.keys())], autopct='%1.1f%%')
        # https://stackoverflow.com/questions/27898830/python-how-to-change-autopct-text-color-to-be-white-in-a-pie-chart
        if self.couleur!='grey':
            for autotext in autotexts:  autotext.set_color('grey')
        deuxPlots("{0}-Suffrages-Camembert-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
        plt.xscale('linear')

    def biffageDoublage(self):
        """
        Analyse le biffage
        """
        doubles = {}
        for c in self.candidats: doubles[c.nom] = c.doubles
        doubles = dict(sorted(doubles.items(), key=lambda item: item[1], reverse=True))
        biffes = {}
        for c in self.candidats: biffes[c.nom] = c.biffes
        biffes_uniques = {}
        for c in self.candidats: biffes_uniques[c.nom] = sum(c.biffe_pour_qui_unique.values())
        doubles_uniques = {}
        for c in self.candidats: doubles_uniques[c.nom] = c.doubles_uniques
       
        y_pos = np.arange(len(doubles.values()))
        width = 0.4
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        # this is ordered
        plt.barh(y_pos-width/2,doubles.values(),width,color='green',label='Doublage',alpha=1)
        # these ones are not ordered
        plt.barh(y_pos-width/2,[ doubles_uniques[n] for n in doubles.keys()] ,width,color='salmon',label='Doublage Unique',alpha=1)
        plt.barh(y_pos+width/2,[ biffes[n] for n in doubles.keys()] ,width,color='red',label='Biffage',alpha=1)
        plt.barh(y_pos+width/2,[ biffes_uniques[n] for n in doubles.keys()] ,width,color='black',label='Biffage Unique',alpha=1)
        plt.yticks(y_pos, labels=(doubles.keys()))
        plt.xlabel('Doublages et biffages')
        plt.title("Doublages et biffages des candidats {0}".format(self.nom))
        plt.legend()
        plt.gca().invert_yaxis()
        deuxPlots("{0}-DoublagesBiffages-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()

        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.12)
        plt.title("Doublages et biffages des candidats {0}".format(self.nom))
        offx = 0.01*list(doubles.values())[0]
        offy = 0.01*list(biffes.values())[0]
        plt.plot([d-offx for d in doubles.values()], [ biffes[n]-offy for n in doubles.keys()], 'o', color=self.parti.couleur)
        for k,v in doubles.items(): plt.text(v,biffes[k],k)
        plt.xlabel('Doublages')
        plt.ylabel('Biffages')
        
        deuxPlots("{0}-DoublagesBiffages-Scatter-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
       

    def suffragesParCandidat(self):
        """
        Graphique des suffrages par candidat
        """
        sorted_cands = {  }
        for c in self.candidats : sorted_cands[c] = c.suffrages
        sorted_cands = dict(sorted(sorted_cands.items(), key=lambda item: item[1], reverse=False))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        y_pos = np.arange(len(self.candidats))

        # les biffés je les mets à gauche
        biffes = [ -c.biffes for c in sorted_cands.keys() ]
        plt.barh(y_pos,biffes,color='red',label='Biffés')

        # biffés uniques
        uniques = [ -sum(c.biffe_pour_qui_unique.values()) for c in sorted_cands.keys() ]
        plt.barh(y_pos,uniques,color='black',label='Biffés uniques')
        
        # listes complètes
        base = [ self.suffrages_liste_complete/_sieges for c in sorted_cands.keys() ]
        plt.barh(y_pos,base,color='cyan',label='Listes complètes')
        
        # puis je mets les doublés au dessus de la base
        doubles = [ c.doubles for c in sorted_cands.keys() ]
        plt.barh(y_pos,doubles,left=base,color='green',label='Doublés')
        sums = [ int(b+d) for d,b in zip(base,doubles) ]
        
        # par dessus les doublés uniques
        doubles_uniques = [ c.doubles_uniques for c in sorted_cands.keys() ]
        plt.barh(y_pos,doubles_uniques,left=base,color='salmon',label='Doublés uniques')
        
        # les autres de fait contiennent les biffages
        suffs =  [ c.suffrages-c.doubles for c in sorted_cands.keys() ]  
        plt.barh(y_pos,suffs,left=sums,color='blue',label='Complémentaires')
        sums = [ int(b+d) for d,b in zip(sums,suffs) ]

        # on remet les biffes
        # plt.barh(y_pos,[-b for b in biffes],left=sums,color='white',edgecolor='red',height=0.75)
         
        plt.xlabel('Suffrages')
        plt.title("Candidats de {0}".format(self.nom))
        plt.yticks(y_pos, labels=[c.nom for c in sorted_cands.keys()])
        off = 0.1*base[0]
        for i, v in enumerate(sums):
#            plt.text(-off+v, i - .25, str(v), color='white', ha='right', fontsize=9) # horizontal alignment
            plt.text(off, i - .25, str(v), color='black', ha='left', fontsize=9) # horizontal alignment
        plt.legend(loc="lower right")
        deuxPlots("{0}-Suffrages-Par-Candidat-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
        
    def candidatsParasites(self,candidats):
        """
        Candidats parasites sur les listes PVL
        """
        para = {}
        listes = []
        if self.classe == "Parti":
            listes = [ l.numero for l in p.listes ]
        else:
            listes = [ self.numero ]
            #    print("Je cherche les parasites de {0} Listes: {1}".format(self.nom,listes))
        for c in candidats.values():
            if c.liste.numero in listes : continue
            para[c] = 0
            for l in listes:
                if l in c.suffrages_par_liste.keys():
                    para[c] += c.suffrages_par_liste[l]
        #    print("Trouvé {0} parasites".format(len(para)))
        para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))
        nn = _max
        kk = list(para.keys())[:nn]
        vv = list(para.values())[:nn]
        y_pos = np.arange(len(kk))
        plt.barh(y_pos,vv,color=[ c.liste.couleur for c in kk ] )
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels=[k.nom for k in kk])
        plt.xlabel('Suffrages obtenus chez {0}'.format(self.nom))
        plt.title("Candidats parasites de {0}".format(self.nom))
        deuxPlots("{0}-CandidatsParasite-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
        
    def parasite(self,listes):
        """
        qui parasite la liste ?
        """
        para = {}
        idx = self.numero
        if self.classe == "Parti": idx = self.nom # on indexe les partis par nom
        for l in listes.values():   # peut être un numero ou un nom
            if not (l.nom == self.nom):
                # print("Parasitage de {2} - Parti {0} suffrages_par_liste {1}".format(l.nom,l.suffrages_par_liste,idx))
                para[l] = l.suffrages_par_liste[idx]
                # print("Parasitage de {0} par {1} : {2} suffrages".format(self.nom,l.nom,para[l]))
        para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))

        y_pos = np.arange(len(para.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        plt.barh(y_pos,para.values(),color = [l.couleur for l in para.keys()])
        plt.yticks(y_pos, labels=[ l.nom for l in para.keys()])
        plt.title("Parasitage de {0}".format(self.nom))
        plt.xlabel('Suffrages obtenus chez {0}'.format(self.nom))
        plt.gca().invert_yaxis()
        deuxPlots("{0}-Parasite-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()
        return para

    def bilan(self,para):
        """
        Le bilan du plus et du moins
        """
        diff = {}
        plus = {}
        for l in para.keys():
            if self.classe == "Liste": plus[l] = self.suffrages_par_liste[l.numero]  # suffrage de cette liste chez d'autres
            else : plus[l] = self.suffrages_par_liste[l.nom]
            diff[l] = plus[l]-para[l]
            # print("{0} a {1} voix chez {2} et en perd {3}: diff = {4}".format(self.nom,plus[l],l.nom,para[l],diff[l]))
        # on met dans l'ordre
        diff = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))  #
        diff[self] = sum(diff.values())  # bilan total
        plus[self] = 0
        para[self] = 0
        # plot
        y_pos = np.arange(len(diff.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        plt.barh(y_pos,[ plus[l] for l in diff.keys()], edgecolor = [l.couleur for l in diff.keys()], color=['white' for l in diff.keys()])
        plt.barh(y_pos,[ -para[l] for l in diff.keys()], edgecolor = [l.couleur for l in diff.keys()], color=['white' for l in diff.keys()])
        plt.barh(y_pos,diff.values(), color = [l.couleur for l in diff.keys()])
        plt.xlabel("Suffrages sur d'autres listes moins les suffrages perdus")
        plt.title("Bilan de {0}".format(self.nom))
        ticks = [ l.nom for l in list(diff.keys())[:-1]]
        ticks.append("Total")
        plt.yticks(y_pos, labels=ticks)
        plt.gca().invert_yaxis()
        plt.vlines(x = 0., ymin = plt.gca().get_ylim()[0], ymax = plt.gca().get_ylim()[1],colors = 'grey',linewidth=1)
        deuxPlots("{0}-Bilan-{1}".format(self.classe,goodName(self.nom)))
        plus[self] = sum(plus.values())
        para[self] = sum(para.values())
        tableau("{0}-Bilan-{1}".format(self.classe,goodName(self.nom)),ticks,
                { "gagnés" : [ plus[l] for l in diff.keys()],
                  "perdus" : [ -para[l] for l in diff.keys()],
                  "bilan" : list(diff.values()) })
        plt.clf()

        return diff
        

    def communes(self,communes,pires=False,absolu=False,grandes=False):
        """
        Meilleures et pires communes de la liste

        Attention: je n'ai pas le détail des suffrages non-nominatifs par liste
        """
        pourcents = {}
        quoi = "Meilleures"
        if pires: quoi = "Pires"
        elif grandes : quoi = "Grandes"
        if len(self.total_par_commune)<1: return # pas pour pirates et libres
        if grandes:
            for k in list(grandesCommunes.values())[::-1] :
                pourcents[k] = 100.*self.total_par_commune[k]/communes[k].suffrages
                # print(" Grandes {0} {1} : {2} ".format(k,communes[k],pourcents[k]))
        elif not absolu:
            for c in communes.keys(): pourcents[c] = 100.*self.total_par_commune[c]/communes[c].suffrages
            pourcents = dict(sorted(pourcents.items(), key=lambda item: item[1], reverse=pires))
            # print("{0} parti {1} total {2} pourcents {3}".format(self.nom,self.total_par_commune[5650],communes[5650].suffrages,pourcents[5650])) # Vaux sur Morges
        else:
            pourcents = dict(sorted(self.total_par_commune.items(), key=lambda item: item[1], reverse=pires))
        if not grandes:
            top25 = list(pourcents.keys())[-_max:]
            pc25 = list(pourcents.values())[-_max:]
            noms = [communes[c].nom for c in top25]
        else:
            top25 = list(pourcents.keys())
            pc25 = list(pourcents.values())
            noms = [communes[c].nom for c in top25]
            top25.insert(0,0)
            pc25.insert(0,self.pourcentage)
            noms.insert(0,"Canton de Vaud")
            
        # print(pourcents,top25,pc25)
        y_pos = np.arange(len(top25))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        plt.barh(y_pos,pc25,color=self.couleur)
        if absolu:  plt.xlabel('Suffrages dans la commune')
        else: plt.xlabel('Pourcentage dans la commune')
        plt.title("{1}: {0} communes".format(quoi,self.nom))
        plt.yticks(y_pos, labels=noms)
        if grandes: plt.axvline(x = self.pourcentage, color = 'b')
        if absolu and not pires and not grandes:
            if communes[top25[-1]].nom=='Lausanne' and 1.5*pc25[-2]<pc25[-1]: plt.xlim(0,1.5*pc25[-2]) # couper Lausanne
            deuxPlots("{0}-{1}-Suffrages-{2}-Communes".format(self.classe,goodName(self.nom),quoi))
        else: deuxPlots("{0}-{1}-{2}-Communes".format(self.classe,goodName(self.nom),quoi))
        plt.clf()
        
        
#############################################################################
class Parti(Liste):
    """
    Un parti est une somme de listes
    """
    def __init__(self,nom,listes):
        self.nom = nom
        self.nomCourt = nom
        self.nom_parti = nom
        self.numero = None # pour que ça existe
        self.suffrages_liste_complete = 0
        self.suffrages_nom_liste_modifiee = 0
        self.suffrages_comp_liste_modifiee = 0
        self.suffrages_autres_listes = 0
        self.suffrages_sans_denom = 0
        self.suffrages = 0
        self.listes = []
        self.compacts_par_commune = {}
        self.autres_suffrages_par_commune = {}
        self.total_par_commune = {}
        for l in listes.values():
            if l.nom_parti==nom:
                l.parti = self
                self.suffrages_liste_complete += l.suffrages_liste_complete
                self.suffrages_nom_liste_modifiee += l.suffrages_nom_liste_modifiee
                self.suffrages_comp_liste_modifiee += l.suffrages_comp_liste_modifiee
                self.suffrages += l.suffrages
                self.listes.append(l)
                self.couleur = l.couleur
                self.alliance = l.alliance
        self.suffrages_par_liste = {}
        self.doubles_par_liste = {}
        self.classe = "Parti"
        print("Nouveau parti {0} contenant {1} listes".format(self.nom_parti,len(self.listes)))

    def miseAjour(self,listes):
        """
        Mise à jour des suffrages du parti
        """
#        print("J'entre dans la miseAjour avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(listes[1].autres_suffrages_par_commune[5938][0],0,5938,listes[1].nom))
        for l in self.listes:  # je boucle sur les listes
            for k in l.suffrages_par_liste.keys():   # je boucle encore sur les listes
                if k==0: pi = _sd  # sans dénomination
                else: pi = listes[k].nom_parti
                if pi in self.suffrages_par_liste.keys():   # les partis sont indexés par nom
                    # print(u"{0} Trouvé {1} - j'ajoute {2}".format(self.nom,pi,l.suffrages_par_liste[k]))
                    self.suffrages_par_liste[pi] += l.suffrages_par_liste[k]
                    self.doubles_par_liste[pi] += l.doubles_par_liste[k]
                else:
                    # print(u"{0} Nouveau {1} - je crée avec {2}".format(self.nom,pi,l.suffrages_par_liste[k]))
                    self.suffrages_par_liste[pi] = l.suffrages_par_liste[k]
                    self.doubles_par_liste[pi] = l.doubles_par_liste[k]
                #print("Boucle 1 de miseAjour avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(listes[1].autres_suffrages_par_commune[5938][0],0,5938,listes[1].nom))

            for c in l.compacts_par_commune.keys():
#                print("Parti {0} Boucle 2 liste {1} commune {2}".format(self.nom,l.nom,c))
                if c not in self.compacts_par_commune.keys() :  # create first list
                    self.compacts_par_commune[c] = l.compacts_par_commune[c]
                    # Intéressant: ça ne copie pas le dictionnaire, ça crée un pointeur vers celui de la liste.
                    # self.autres_suffrages_par_commune[c] = l.autres_suffrages_par_commune[c]
                    # Il faut créer les éléments du dictionnaire un par un
                    self.autres_suffrages_par_commune[c] = {}
                    for k in l.autres_suffrages_par_commune[c].keys():
                        self.autres_suffrages_par_commune[c][k]=l.autres_suffrages_par_commune[c][k]
                    # print("      Boucle 2 je crée compacts {0} et autres {1}".format(l.compacts_par_commune[c],l.autres_suffrages_par_commune[c]))
                else:
                    self.compacts_par_commune[c] += l.compacts_par_commune[c]
                    for k in self.autres_suffrages_par_commune[c].keys():
                        self.autres_suffrages_par_commune[c][k]+=l.autres_suffrages_par_commune[c][k]
#                        print("{0}: J'ajoute {1}: {2} pour donner {3} pour commune {4} et bulletin {5}".format(self.nom,l.nom,l.autres_suffrages_par_commune[c][k],self.autres_suffrages_par_commune[c][k],c,k))

                    # print("      Boucle 2 incrémente compacts {0} et autres {1}".format(l.compacts_par_commune[c],l.autres_suffrages_par_commune[c]))
#                print("Boucle 2 de miseAjour avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(listes[1].autres_suffrages_par_commune[5938][0],0,5938,listes[1].nom))
                if listes[1].autres_suffrages_par_commune[5938][0]>116: exit()

                
#        print("Le parti {0} a des suffrages de {1}".format(self.nom,self.suffrages_par_liste))
#        print("Je sors de la miseAjour avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(listes[1].autres_suffrages_par_commune[5938][0],0,5938,listes[1].nom))
        

#############################################################################
class Candidat():
    """
    Un candidat
    """
    def __init__(self,nom):
#        print("Nom {0}".format(nom))
        self.numero = nom.split(' ')[0]   # string (to be sortable)
        self.liste_id = int(self.numero.split('.')[0])
        self.liste = None
        self.place = int(self.numero.split('.')[1])
        nn = nom.split(' ')[1:]
        self.nom = ""
        for n in nn[:-1]:
            self.nom+=n+" "
        self.nom+=nn[-1]
        # print(u'Crée candidat {0} liste {1:2}, place {2:2}: {3}'.format(self.numero,self.liste_id,self.place,self.nom))
        self.pvl = None
        self.suffrages_par_liste = {}
        self.doubles_par_liste = {}
        self.suffrages_par_commune = {}
        self.biffes = 0
        self.doubles = 0
        self.doubles_uniques = 0
        self.biffe_pour_qui = {}
        self.biffe_pour_qui_unique = {}
        self.ajoutes_aussi = {}
        self.suffrages = 0
        self.classe = "Candidat"

    def analyse(self,bulletins):
        """
        Analyse le résultat du candidat
        """
        for b in bulletins:
            # print("b.suffrages[{0}] = {1}".format(self.numero,b.suffrages[self.numero]))
            nS = b.nombreDeSuffrages(self.numero)
            if nS>0:                                              # le candidat a des suffrages
                if b.liste: bn = b.liste.numero                   # numero de la liste
                else: bn = 0
                if bn in self.suffrages_par_liste.keys():
                    self.suffrages_par_liste[bn] += nS
                    if b.double(self.numero):
                        self.doubles_par_liste[bn] += b.poids
                else:                                             # je rajoute une liste qui donne des voix
                    self.suffrages_par_liste[bn] = nS
                    self.doubles_par_liste[bn] = 0                # create
                    if b.double(self.numero): self.doubles_par_liste[bn] = b.poids
                self.suffrages += b.suffrages[self.numero]*b.poids
                if b.double_unique(self.numero):
                    self.doubles_uniques += b.poids
                ### amis
                if b.double(self.numero) or b.liste != self.liste:  # ajout sur une autre liste ou doubles
                    #LN = ""
                    #if b.liste : LN = b.liste.nom
                    for c,v in b.suffrages.items():
                        if c==self.numero: continue               # c'est le candidat
                        # d'abord les doublages quand le candidat a été doublé
                        if b.double(self.numero) and  v==2 :      # doublage des deux
                            incrementeOuCree(self.ajoutes_aussi,c, b.poids) # une fois poids
                            #if self.numero=='12.02': print("Le candidat {0} a été doublé et {1} aussi sur un bulletin {3} {2}".format(self.nom,c,b.suffrages,LN))
                        # ensuite sur les autres listes, les doublages ou les autres candidats ajoutés
                        elif (v==2) or (not b.liste) or (not c[:2] == b.liste.numero):
                            incrementeOuCree(self.ajoutes_aussi,c, b.poids) # une fois poids
                            #if self.numero=='12.02': print("Le candidat {0} a été ajouté et {1} aussi sur un bulletin {3} {2}".format(self.nom,c,b.suffrages,LN))
                        #elif self.numero=='12.02': print("Je ne fais rien pour {1} avec un bulletin {3} {2}".format(self.nom,c,b.suffrages,LN))
                
            elif b.liste == self.liste:
                # print("Le candidat {0} a été biffé d'un bulletin avec {1} voix pour {2}".format(self.nom,b.exprimes,b.suffrages.keys()))
                self.biffes += 1
                # "biffe pour qui" sont les candidats doubles ou venant d'ailleurs
                candUnique = []
                for c,v in b.suffrages.items():
                    liste = int(c[:2])
                    # print("{0} liste {1} versus ma liste {2}".format(self.nom,liste,self.liste.numero))
                    if v==2 or liste!=self.liste.numero:
#                        if self.numero=='12.02': print("Le candidat {0} a été biffé et {1} a recu {2} voix".format(self.nom,c,v))
                        incrementeOuCree(self.biffe_pour_qui,c, b.poids) # un
                        if b.pleine(): candUnique.append(c)
                if len(candUnique)==1:
                    incrementeOuCree(self.biffe_pour_qui_unique,candUnique[0],b.poids) # un seul
                    # if self.numero=='12.02': print("Le candidat {1} a été biffé d'une liste {2}, et {3} a recu {4} voix sur un bulletin {5}".format(self.numero,self.nom,b.nom_liste_originale,c,v,b.suffrages))
                    
#        print("Candidat {0} a {1} suffrages dans {2}".format(self.nom,self.suffrages,self.suffrages_par_liste))

#        print("Le candidat {0} a des suffrages de {1}".format(self.nom, self.suffrages_par_liste))
        self.doubles = sum(self.doubles_par_liste.values())
        self.liste.miseAjour(self)

    def biffage(self,candidats,listes,unique=True):
        """
        Analyse le biffage
        Unique veut dire que je suis le seul biffé
        """
        if unique:
            biff = dict(sorted(self.biffe_pour_qui_unique.items(), key=lambda item: item[1], reverse=True))  # unique
        else:
            biff = dict(sorted(self.biffe_pour_qui.items(), key=lambda item: item[1], reverse=True))
        nn = _max
        kk = list(biff.keys())[:nn]
        vv = list(biff.values())[:nn]
        cc = [ listes[int(k[0:2])].couleur for k in kk ]  # k est genre "07.16" qui donne listes[7].
        if not unique:
            vU = []
            for k in kk:
                if k in self.biffe_pour_qui_unique.keys(): vU.append(self.biffe_pour_qui_unique[k])
                else: vU.append(0)
            vD = [ a-b for  (a,b) in zip(vv,vU)]  # differece

        y_pos = np.arange(len(kk))
        
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels=[candidats[k].nom for k in kk])
        plt.xlabel('Biffages de {0}'.format(self.nom))
        if unique:
            plt.barh(y_pos,vv,color=cc )
            plt.title("Biffages de seulement {0} en faveur de ...".format(self.nom))
            deuxPlots("{0}-Biffage-Unique-{1}".format(self.classe,goodName(self.nom)))
        else:
            plt.barh(y_pos,vU,color='black', label="Uniques" )
            plt.barh(y_pos,vD,left=vU,color=cc, label="Autres" )
            plt.legend(loc="lower right")
            plt.title("Biffages de {0} en faveur de ...".format(self.nom))
            deuxPlots("{0}-Biffage-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()

    def amis(self,candidats,listes):
        """
        Meilleurs amis
        """
        amis = dict(sorted(self.ajoutes_aussi.items(), key=lambda item: item[1], reverse=True))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        nn = _max
        kk = list(amis.keys())[:nn]
        vv = list(amis.values())[:nn]
        cc = [ listes[int(k[0:2])].couleur for k in kk ]  # k est genre "07.16" qui donne listes[7]. 
        y_pos = np.arange(len(kk))
        plt.barh(y_pos,vv,color=cc )
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels=[candidats[k].nom for k in kk])
        plt.xlabel('Amis de {0}'.format(self.nom))
        plt.title("Candidats ajoutés en même temps que {0}".format(self.nom))
        deuxPlots("{0}-Amis-{1}".format(self.classe,goodName(self.nom)))
        plt.clf()

    def listes(self,listes):
        """
        suffrages du candidat par listes
        """
        s_listes = dict(sorted(self.suffrages_par_liste.items(), key=lambda item: item[1], reverse=True))
        # print("s_listes {0} listes {1}".format(s_listes,listes))
        cols = []
        labels = []
        for n in s_listes.keys():
            if n == 0 :
                labels.append(_sd)
                cols.append("black")
            else:
                cols.append(listes[n].couleur)
                labels.append(listes[n].nom)
        s_listes[ "Liste complète"] = int(self.liste.suffrages_liste_complete/_sieges)
        labels.append( "Liste complète")
        cols.append(self.liste.couleur)
        y_pos = np.arange(len(s_listes))
        plt.barh(y_pos,s_listes.values(),color=cols )
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels = labels)
        plt.xlabel('Suffrages de {0}'.format(self.nom))
        plt.title("Suffrages de {0} par liste".format(self.nom))
        plt.xscale('log')
        for i, v in enumerate(s_listes.values()):
            plt.text(1.02*v, i + .25, str(v), color='blue', fontsize=9)
        deuxPlots("Candidat-Suffrages-{0}".format(goodName(self.nom)))
        plt.clf()
        plt.xscale('linear')
        
    def communes(self,communes,relatif=True):
        """
        Meilleures communes du candidat relatif à la liste
        """
        cand = {}
        parti = {}
        
        for k in self.suffrages_par_commune.keys():
            if relatif:
                if (self.liste.total_par_commune[k]>0): cand[k] = _sieges*1.0*sum(list(self.suffrages_par_commune[k].values()))/self.liste.total_par_commune[k]
            else:
                cand[k] = 100.*(_sieges*sum(list(self.suffrages_par_commune[k].values()))+self.liste.compacts_par_commune[k])/communes[k].suffrages
                # if k==5726: print("{0} suffrages {1}+{4} / {2} = {3}".format(self.nom, sum(list(self.suffrages_par_commune[k].values())),communes[k].suffrages,cand[k],self.liste.compacts_par_commune[k]))
                    
        cand = dict(sorted(cand.items(), key=lambda item: item[1], reverse=False))
        if not relatif: # parti dans le même ordre
            for k in cand.keys():
                parti[k] = 100.*self.liste.total_par_commune[k]/communes[k].suffrages

        tt = list(cand.keys())[-_max:]
        top25 = [ communes[c].nom for c in tt ]
        pc25 = list(cand.values())[-_max:]
        pa25 = list(parti.values())[-_max:]
        top25.append("Canton de Vaud")
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
        y_pos = np.arange(len(top25))
        plt.yticks(y_pos, labels=top25)
        if relatif:
            pc25.append(1.0*_sieges*self.suffrages/self.liste.suffrages)
            plt.barh(y_pos,pc25,color=self.liste.parti.couleur)
            plt.xlabel('Suffrages relatif à la liste')
            plt.title("{0}: relatif à la liste".format(self.nom))
            deuxPlots("Candidat-{0}-Communes-relatif-a-la-liste".format(goodName(self.nom)))
        else:
            pc25.append(_sieges*_vaud*self.suffrages/self.liste.suffrages)
            pa25.append(_vaud)
            width = 0.4
            plt.barh(y_pos+width/2,pc25,width,color='Black',label=self.nom)
            plt.barh(y_pos-width/2,pa25,width,color=self.liste.parti.couleur,label=self.liste.nomCourt)
            plt.xlabel('Pourcents (pondérés par sièges)')
            plt.title("{0}: meilleures communes".format(self.nom))
            plt.legend(loc="lower right")
            deuxPlots("Candidat-{0}-Communes".format(goodName(self.nom)))

        plt.clf()
            

#############################################################################
def lisBulletins(listes):
    """
    Lis le gros fichier de tous les Bulletins
    """
    candidats = {}
    bulletins = []
    with open(_file) as f:
        ff = csv.reader(f)
        head = True
        for row in ff:
            if head:
                for n in row[3:-1]:
                    c = Candidat(n)
                    candidats[c.numero] = c
                head = False
            else:
                try:
                    a = int(row[0]) # marche pas sur la dernière ligne
                except:
                    # print("Fin du fichier")
                    break
                b = Bulletin(row,candidats)
                b.assigneParti(listes,partis)
#                print("Bulletin de poids {0}".format(b.poids))
                bulletins.append(b)

    f.close()

    return candidats,bulletins
    
#############################################################################
def attribueListes(candidats,listes):
    """
    ajoute la liste aux candidats
    """
    for c in candidats.values():
        for l in listes.values():
            if c.liste_id == l.numero: c.liste = l
        # print("Candidat {0} est du parti {1}".format(c.nom,c.liste.nom_parti))
                
#############################################################################
def lisScrutin():
    """
    Résumé du canton par liste
    https://www.elections.vd.ch/votelec/app21/index.html?id=CHCN20231022#v=listsCandidats&m=moreDetails&r=listSuffOrigin
    """
    listes = {}
    partis = {}
    noms_des_listes = [_sd]  # mettre sans dénomination en premier
    print("Je lis le scrutin")

    with open(_summary) as f:
        ff = csv.reader(f)
        nL = 0  # ligne
        for row in ff:
            nL += 1
            if nL>=4 and not "Total" in row[0]:  
                l=Liste(row)
                listes[l.numero] = l

    # mettre à jour la liste des listes
    for l in listes.values():
        l.suffrages_par_liste[0] = 0
        l.doubles_par_liste[0] = 0
        for nl in listes.keys():
            l.suffrages_par_liste[nl] = 0
            l.doubles_par_liste[nl] = 0

    noms_des_partis = {}
    for l in listes.values():
        if l.nom_parti not in noms_des_partis.keys():
            noms_des_partis[l.nom_parti] = [l]
        else:
            noms_des_partis[l.nom_parti].append(l)

    for k in noms_des_partis.keys():
        partis[k] = Parti(k,listes)
            
    return listes,partis
                
#############################################################################
def lisCommunes(communes,candidats,listes):
    """
    Lis le fichier vaudois des communes et candidats
    """
    with open(_communes) as f:
        ff = csv.reader(f)
        nL = 0  # ligne
        for row in ff:
            nL += 1
#            print("Ligne {0}: {1}".format(nL,row))
            if nL==3:
                nom_listes = [ r for r in row[9:] ]
                # print("Les listes sont {0}".format(nom_listes))
                ListKeys = []   # liste qui mappe l'ordre dans ce fichier avec l'ordre des numéros de listes
                for n in nom_listes:
                    for l in listes.values():
                        if n==l.nom : ListKeys.append(l.numero)
                ListKeys.append(0)  # sd
                print("Les listes dans l'ordre du fichier sont {0}".format([ listes[lk].nom for lk in ListKeys[:-1] ]))
                    
            elif nL>=4:
                # commune
                num = int(row[0])
                nom = row[1]
                cand_id = row[2]
                la_liste = listes[ int(cand_id[:2]) ]
                # 3 : nom de la liste
                cand_nom = row[4]+" "+row[5]
                non_mod = int(row[6])  # par liste
                mod = int(row[7])
                tot = int(row[8])
                parListe = [ int(r) for r in row[9:] ]

                if num not in communes.keys():
                    if num==_suissesDeLetranger1: num = _suissesDeLetranger2
                    else:
                        print("Je ne trouve pas la commune {0} {1}".format(num,nom))
                        exit()
                if num not in la_liste.compacts_par_commune:   # je dois les ajouter 1 à 1 parce que des listes, comme les jeunes du centre ont certains candidats doublés et pas d'autres.
                    la_liste.compacts_par_commune[num] = non_mod
                else:
                    la_liste.compacts_par_commune[num] += non_mod
                
                if num not in la_liste.autres_suffrages_par_commune.keys(): la_liste.autres_suffrages_par_commune[num] = {}
                # communes[num].suffrages += tot # incrémente le total de suffrages

                # liste des voix venant d'autres listes. Le dernier est s.d.
                candidats[cand_id].suffrages_par_commune[num] = { ListKeys[i]: parListe[i] for i in range(len(parListe))}
                
                for k in candidats[cand_id].suffrages_par_commune[num].keys():    # je boucle sur les listes 
                    if k in la_liste.autres_suffrages_par_commune[num].keys():    
                        la_liste.autres_suffrages_par_commune[num][k] += candidats[cand_id].suffrages_par_commune[num][k]
                    else:
                        la_liste.autres_suffrages_par_commune[num][k] = candidats[cand_id].suffrages_par_commune[num][k]
                    # if la_liste.numero==1 and num==5938: print("Commune {6} {0} liste {1} candidat {2} suff. de la liste {3}: j'ajoute {4} pour avoir {5}".format(nom,la_liste.nom,cand_id,k,candidats[cand_id].suffrages_par_commune[num][k],la_liste.autres_suffrages_par_commune[num][k],num))
                # if num==5726: print("Ajouté {0} à {1} dans {2}: autres_suffrages_par_commune {3} somme {4}".format(cand_id,la_liste.nom,nom,la_liste.autres_suffrages_par_commune[num],sum(list(la_liste.autres_suffrages_par_commune[num].values()))))

                # print("Commune {0} {1} : Candidat {2} {3} a {4}+{5} suffrages de {6}".format(num,nom,cand_id,cand_nom,non_mod,mod,candidats[cand_id].suffrages_par_commune[num]))
                
                la_liste.total_par_commune[num] = la_liste.compacts_par_commune[num] + sum(list(la_liste.autres_suffrages_par_commune[num].values()))

#    print("Je sors de la lecture avec {0} suffrages pour la liste {1} sur des bulletins {2} pour {3}".format(listes[1].autres_suffrages_par_commune[5938][0],0,5938,listes[1].nom))
    return 

#############################################################################
def lisOFS(partis):
    """
    Lis le fichier suisse des communes et partis
    """
    communes = {}
    Vaud = Commune(-1,"Canton de Vaud")
    with open(_partis) as f:
        ff = csv.reader(f,delimiter=';')
        nL = 0  # ligne
        for row in ff:
            nL += 1
 #           if row[0]=='Gemeinde' and row[4]=='Vaud':
            if row[4]=='Vaud':
                # print(row)
                nom = row[2]
                if row[5]:
                    num = int(row[5])
               	    if num not in communes.keys():
                        c = Commune(num,nom)
                        communes[num] = c
                else: c = Vaud
                parti = row[9]
                if row[12]=='': suffrages = 0
                else: suffrages = int(row[12])
                c.suffrages_par_parti[parti] = suffrages
                if c!=Vaud and parti in partis.keys():
                    partis[parti].total_par_commune[num] = suffrages
                    # print("Ajouté commune {0} parti {1} suffrages {2}".format(nom,parti,suffrages))
                elif 0==suffrages:  # ne participe pas
                    pass # do nothing
                elif 'Autres' == parti:
                    pass

    for c in communes.values(): c.suffrages = sum(list(c.suffrages_par_parti.values()))
    Vaud.suffrages = sum(list(Vaud.suffrages_par_parti.values()))
                                          
    # print('Vaux sur Morges {0} de {1}'.format(communes[5650].suffrages , communes[5650].suffrages_par_parti))
    return Vaud, communes
#############################################################################
def analyseBilans(bilans):
    """
    Matrice des bilans
    """
    what = "Partis"
    if list(bilans.keys())[0].classe=='Liste':  what = "Listes"
    partis = [ p.nom for p in bilans.keys() ]
    npartis = len(partis)
    xy_pos = np.arange(npartis)  # sera utilisé pour x et y
    ordreDesPartis = {}
    for i in xy_pos: ordreDesPartis[i] = list(bilans.keys())[i]
    theX = []
    theY = []
    theVal =  []
    colour = []
    # print("Bilans",bilans)
    # print("ordreDesPartis",ordreDesPartis)
    for y in xy_pos:
        for x in xy_pos:
            theX.append(x)
            theY.append(y)
            # print("bilans[ ordreDesPartis[x] ]",bilans[ ordreDesPartis[x] ])
            b = bilans[ ordreDesPartis[y] ][ ordreDesPartis[x] ]
            theVal.append( abs(b)/20. )
            # colour.append(b)
            if b>0: colour.append('green')
            else: colour.append('red')
            # print("Bilans {0} à {1} : {2}".format( ordreDesPartis[x].nom, ordreDesPartis[y].nom, b))

    ll = 0.15
    if  what == "Listes": ll = 0.25
    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.25,left=ll)               
    plt.scatter(theX, theY, s=theVal, c=colour, alpha=0.5)
    plt.title("Bilans des {0}".format(what))
    plt.yticks(xy_pos, labels=[p.nomCourt for p in ordreDesPartis.values()])
    plt.xticks(xy_pos, labels=[p.nomCourt for p in ordreDesPartis.values()],rotation=90)
#    plt.colorbar() # pas utile
    deuxPlots("Bilans-des-{0}".format(what))
    plt.clf()

#############################################################################
def analyseChi2(chi2):
    """
    Analyse le chi2 des communes
    """
    best = min(chi2, key=chi2.get)
    worst = max(chi2, key=chi2.get)
    print("La commune la plus typique est {0} (chi2={1:.1f}) et la moins {2} (chi2={3:.1f})".format(best.nom,chi2[best],worst.nom,chi2[worst]))
    
    chi2s = dict(sorted(chi2.items(), key=lambda item: item[1], reverse=True))
    top25 = list(chi2s.keys())[-_max:]
    pc25 = list(chi2s.values())[-_max:]
    y_pos = np.arange(len(top25))
    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.30)
    plt.barh(y_pos,pc25,color="green")
    plt.title("Communes qui votent comme le Canton")
    plt.yticks(y_pos, labels=[c.nom for c in top25])
    plt.xlabel('$\chi^2$')
    deuxPlots("Communes-Typiques")
    plt.clf()


def correlations(p1,p2,communes,Vaud):
    """
    correlations de deux partis par commune
    """
    if len(p1.total_par_commune)==0 or len(p2.total_par_commune)==0: return
    pourcents1 = [ 100.*p1.total_par_commune[c]/communes[c].suffrages for c in communes.keys() ]
    pourcents2 = [ 100.*p2.total_par_commune[c]/communes[c].suffrages for c in communes.keys() ]
#    bulletins = [ 10*(np.log(communes[c].suffrages)/np.log(2.)-9) for c in communes.keys() ]
    bulletins = [ communes[c].suffrages/_sieges/40 for c in communes.keys() ]
    vaud1 = [ 100.*p1.suffrages/Vaud.suffrages ]
    vaud2 = [ 100.*p2.suffrages/Vaud.suffrages ]
    t = [ b/max(bulletins) for b in bulletins ]
#    print(min(bulletins),max(bulletins))
#    weights = [ communes[c].suffrages/_sieges for c in communes.keys() ]
#    c, b, a = np.polyfit(pourcents1, pourcents2, w=weights,deg=2)
#    c, b, a = np.polyfit(pourcents1, pourcents2, deg=2)
    b, a = np.polyfit(pourcents1, pourcents2, deg=1)

    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.08)
    plt.scatter(vaud1,vaud2,s=[1000],c='g',alpha=0.2)
    plt.annotate("Canton",(vaud1[0],vaud2[0]),c='g')

    plt.title("{0} et {1} par commune".format(p1.nom,p2.nom))
    xseq = np.linspace(0, 1.05*max(pourcents1), num=100)
    
    # plt.axvline(x = vaud1[0], color = p1.couleur )
    # plt.axhline(y = vaud2[0], color = p2.couleur )
    # quorum
    if max(pourcents1)>2.5: plt.axvline(x = 5., color = "cyan" )
    if max(pourcents2)>2.5: plt.axhline(y = 5., color = "cyan" )
    
#    plt.plot(xseq, [a + b * x + c *x**2 for x in xseq] , color="silver", lw=1)
    plt.plot(xseq, [a + b * x for x in xseq] , color="silver", lw=1)
    sc = plt.scatter(pourcents1,pourcents2,s=bulletins,alpha=0.5,c=t,
                     norm=matplotlib.colors.LogNorm(), cmap='cool')
#    plt.colorbar(sc, label="Taille")
    plt.xlabel("Poucentage du parti {0}".format(p1.nom))
    plt.ylabel("Poucentage du parti {0}".format(p2.nom))
    plt.xlim(0,1.05*min(max(pourcents1),2*vaud1[0]))
    plt.ylim(0,1.05*min(max(pourcents2),2*vaud2[0]))
    for n in list(grandesCommunes.keys())[:10]:
        c=grandesCommunes[n]
        plt.annotate(n, (100.*p1.total_par_commune[c]/communes[c].suffrages,
                         100.*p2.total_par_commune[c]/communes[c].suffrages))
    deuxPlots("Correlation-{0}-{1}".format(goodName(p1.nom),goodName(p2.nom)))
    plt.clf()

    """
    Plus grosses communes selon quorum centre PVL
    """
    QuatreCas = {"++":None, "+-":None, "--": None, "-+": None}
    if "PVL"==p1.nom and "Centre"==p2.nom:
        for c in communes.keys():
            res = ""
            if p1.total_par_commune[c]/communes[c].suffrages > 0.05:
                res = "+"
            else: res = "-"
            if p2.total_par_commune[c]/communes[c].suffrages > 0.05:
                res += "+"
            else: res += "-"
            if (not QuatreCas[res]) or (communes[c].suffrages>communes[QuatreCas[res]].suffrages):
                QuatreCas[res] = c
        for r,c in QuatreCas.items():
            print("Plus grosse commune {0} : {1} avec {2:.1f}% et {3:.1f}%".format(r,communes[c].nom,
                                                                                   100.*p1.total_par_commune[c]/communes[c].suffrages,
                                                                                   100.*p2.total_par_commune[c]/communes[c].suffrages))
    
    
#############################################################################
# main
#############################################################################
listes,partis = lisScrutin()
candidats,bulletins = lisBulletins(listes)
Vaud,communes = lisOFS(partis)
lisCommunes(communes,candidats,listes)
attribueListes(candidats,listes)
pd = sum([b.poids for b in bulletins])
sf = sum([b.exprimes*b.poids for b in bulletins])
# le nombre de complémentaires ne correspond pas à ce que je trouve dans le fichier
# des bulletins modifiés. Si je l'ajoute ici ça marche.
nm = sum([p.suffrages_liste_complete+p.suffrages_comp_liste_modifiee for p in listes.values()])
total_des_suffrages = sf+nm

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

# graphiques pour Vaud
Vaud.partis(listes,normalise=False)
Vaud.partis(partis,normalise=True)
Vaud.candidats(candidats)
Vaud.candidats(candidats,avecBase=True)
Vaud.candidats(candidats,parti="Centres")

# graphiques pour les partis
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
    p.communes(communes,True)  # pires
    p.communes(communes,False,True) # absolu
    p.communes(communes,True,True)  # pires, absolu
    p.communes(communes,grandes=True)  # pires, absolu
    Vaud.candidats(candidats,parti=p.nom)
    Vaud.candidats(candidats,parti=p.nom,avecBase=True)


print("Total des suffrages {0:.0f} au lieu de {1:.0f}. Différence {2}.".format(somme,total_des_suffrages,somme-total_des_suffrages))

analyseBilans(bilans)

for p in partis.values():
    for q in partis.values():
        if p==q : continue
        correlations(p,q,communes,Vaud)


# graphiques pour les listes
bilans = {}
somme = 0.
for l in listes.values():
    l.pourcentage = 100.*l.suffrages/total_des_suffrages
    print("Liste {0} : {1:0.1f}% ({2})".format(l.nom,l.pourcentage,l.suffrages))
    somme += l.suffrages
    l.communes(communes)
    l.communes(communes,True)  # pires
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


# graphiques pour les candidats
for c in candidats.values():
    if c.liste.parti.nom == "PVL" or c.nom in _elus:
#        print("Candidat {0} liste {1} parti {2}".format(c.nom,c.liste.nom,c.liste.parti.nom))
        print("\\Candidat{{{0}}}{{{1}}} % {2}".format(goodName(c.nom),c.nom,c.liste.nom))
        c.communes(communes)
        c.communes(communes,False)
        c.listes(listes)
        c.amis(candidats,listes)
        c.biffage(candidats,listes, unique=False)
        c.biffage(candidats,listes, unique=True)
           
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
"""


