import csv

_file = 'export-bulletins-PR-CHCN-20231022.csv'
_summary = 'ScrutinsParListe.csv'
_sd = "Sans dénom."
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(7,5))
fig, ax = plt.subplots()
_sieges = 19   # 19 sieges
_moitie = int(_sieges/2.+1)   # il faut 10 pour avoir la moitié

def goodName(name):
    name2 = name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace(">","_g_").replace("<","_l_").replace("*","_times_").replace(".","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_").replace("||","_or_").replace("&&","_and_").replace("&","_").replace("|","_").replace(":","_vs_").replace("'","_").replace("#","N").replace('·','_')
    return name2

def incrementeOuCree(dico,cle,valeur):
    if cle in dico.keys(): dico[cle] += valeur
    else: dico[cle] = valeur

def deuxPlots(nom):
    """
    Cree un pdf et un png
    """
    plt.savefig("pdf/{0}.pdf".format(nom))
    plt.savefig("png/{0}.png".format(nom))

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
        self.exprimes = sum(self.suffrages.values())
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

    def pleine(self):
        """
        Liste pleine?
        """
        return self.exprimes==_sieges

#############################################################################
class Liste():
    """
    Liste
    """
    def __init__(self,row):
        self.numero = int(row[0])
        self.nom = row[1]
        self.suffrages_liste_complete = int(row[2])+int(row[3])
        self.suffrages_nom_liste_modifiee = int(row[4])
        self.suffrages_comp_liste_modifiee = int(row[5])
        self.suffrages_autres_listes = int(row[7])
        self.suffrages_sans_denom = int(row[8])
        self.suffrages = self.suffrages_liste_complete+self.suffrages_nom_liste_modifiee+self.suffrages_comp_liste_modifiee+self.suffrages_autres_listes+self.suffrages_sans_denom
        self.classe = "Liste"
        print("Nouvelle liste {0:2} {1} a {2} suffrages".format(self.numero,self.nom,self.suffrages))
        
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
            self.nom_parti = 'Verts'
            self.alliance = 'Gauche'
            self.couleur = "forestgreen"
        elif 'VERT' in self.nom:
            self.nom_parti = 'PVL'
            self.alliance = 'PVL'
            self.couleur = "yellowgreen"
        elif 'POP' in self.nom:
            self.nom_parti = 'POP'
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
            self.nom_parti = 'EàG'
            self.alliance = 'Gauche'
            self.couleur = "firebrick"
        elif 'PEV' in self.nom:
            self.nom_parti = 'PEV'
            self.alliance = 'Centre'
            self.couleur = "gainsboro"
        else:
            print("Je ne touve pas {0}".format(self.nom))
            exit()
        self.parti = None  # lien vers parti
        self.suffrages_par_liste = {}
        self.doubles_par_liste = {}
        self.candidats = [ ]
        
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
        s = sum([v for v in self.suffrages_par_liste.values()])
        print("{0}: {1} suffrages compl {2}, mod {3}+{4}, autres {5}, s.d. {6} -> {7} =? {8}"
              .format(self.nom,
                      self.suffrages,
                      self.suffrages_liste_complete,
                      self.suffrages_nom_liste_modifiee,
                      self.suffrages_comp_liste_modifiee,
                      self.suffrages_autres_listes,
                      self.suffrages_sans_denom,
                      self.suffrages-self.suffrages_liste_complete-self.suffrages_comp_liste_modifiee,s))

    def plotSuffrages(self,listes):
        """
        Fait un plot des suffrages obtenus dans les autres partis
        """
        colors = {0: "black"}    # Liste
        colors = {_sd: "black"}  # Parti
        suffs = {}
        for k in self.suffrages_par_liste.keys():
            if k==0 or k==_sd : nom = _sd   # l'un pour Liste l'autre pour Parti
            else: nom = listes[k].nom
            suffs[nom] = self.suffrages_par_liste[k]
#            print("Pour {0} je cherche {1}".format(self.nom,k))
            if k!=_sd and k!=0 : colors[nom] = listes[k].couleur

        suffs = dict(sorted(suffs.items(), key=lambda item: item[1], reverse=True))

        y_pos = np.arange(len(suffs.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        plt.barh(y_pos,suffs.values(),color=[colors[k] for k in list(suffs.keys())])
        plt.yticks(y_pos, labels=(suffs.keys()))
        plt.xlabel('Suffrages')
        plt.title(self.nom)
        plt.gca().invert_yaxis()
        deuxPlots("Suffrages-{1}-{0}".format(goodName(self.nom),self.classe))
        plt.clf()

    def biffage(self):
        """
        Analyse le biffage
        """
        biffs = {}
        for c in self.candidats:
            biffs[c.nom] = c.biffes
        biffs = dict(sorted(biffs.items(), key=lambda item: item[1], reverse=False))
        y_pos = np.arange(len(biffs.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        plt.barh(y_pos,biffs.values(),color=self.couleur)
        plt.yticks(y_pos, labels=(biffs.keys()))
        plt.xlabel('Biffages')
        plt.title(self.nom)
        plt.gca().invert_yaxis()
        deuxPlots("Biffages-{0}".format(goodName(self.nom)))
        plt.clf()

    def suffragesParCandidat(self):
        """
        Graphique des suffrages par candidat
        """
        sorted_cands = {  }
        for c in self.candidats : sorted_cands[c] = c.suffrages
        sorted_cands = dict(sorted(sorted_cands.items(), key=lambda item: item[1], reverse=False))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        y_pos = np.arange(len(self.candidats))
        base = [ self.suffrages_liste_complete/_sieges for c in sorted_cands.keys() ]
        plt.barh(y_pos,base,color='green',label='Listes complètes')
        doubles = [ c.doubles for c in sorted_cands.keys() ]
        plt.barh(y_pos,doubles,left=base,color='blue',label='doublés')
        sums = [ b+d for d,b in zip(base,doubles) ]
        suffs =  [ c.suffrages-c.doubles for c in sorted_cands.keys() ]
        plt.barh(y_pos,suffs,left=sums,color='red',label='autres suffrages')
        
        plt.xlabel('Suffrages')
        plt.title(self.nom)
        plt.yticks(y_pos, labels=[c.nom for c in sorted_cands.keys()])
        plt.legend()
        deuxPlots("SuffragesParCanddidat-{0}".format(goodName(self.nom)))
        plt.clf()
        


#############################################################################
class Parti(Liste):
    """
    Un parti est une somme de listes
    """
    def __init__(self,nom,listes):
        self.nom = nom
        self.nom_parti = nom
        self.numero = None # pour que ça existe
        self.suffrages_liste_complete = 0
        self.suffrages_nom_liste_modifiee = 0
        self.suffrages_comp_liste_modifiee = 0
        self.suffrages_autres_listes = 0
        self.suffrages_sans_denom = 0
        self.suffrages = 0
        self.listes = []
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

        Je pourrais probablement simplifier maintenant que ce sont des dictionnaires
        """
        for l in listes.values():  # je boucle sur les listes
            if l.nom_parti != self.nom : continue    # je ne garde que les listes du parti
            for k in l.suffrages_par_liste.keys():  # je boucle encore sur les listes
                if k==0: pi = _sd  # sans dénomination
                else: pi = listes[k].nom_parti
                if k in self.suffrages_par_liste.keys():   # les partis sont indexés par parti
                    print(u"{0} Trouvé {1} - j'ajoute {2}".format(self.nom,pi,l.suffrages_par_liste[k]))
                    self.suffrages_par_liste[pi] += l.suffrages_par_liste[k]
                    self.doubles_par_liste[pi] += l.doubles_par_liste[k]
                else:
                    print(u"{0} Nouveau {1} - je crée avec {2}".format(self.nom,pi,l.suffrages_par_liste[k]))
                    self.suffrages_par_liste[pi] = l.suffrages_par_liste[k]
                    self.doubles_par_liste[pi] = l.doubles_par_liste[k]
                
        # print("Le parti {0} a des suffrages de {1}".format(self.nom,self.suffrages_par_liste))

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
        self.biffes = 0
        self.doubles = 0
        self.biffe_pour_qui = {}
        self.biffe_pour_qui_unique = {}
        self.ajoutes_aussi = {}
        self.suffrages = 0
        self.classe = "Candidat"

    def est_pvl(self):
        """
        Est-ce un PVL?
        """
        if self.pvl is None:   # calcule une seule fois
            self.pvl = ('PVL' == self.liste.parti )
        return self.pvl

    def analyse(self,bulletins):
        """
        Analyse le résultat du candidat
        """
        for b in bulletins:
            # print("b.suffrages[{0}] = {1}".format(self.numero,b.suffrages[self.numero]))
            nS = b.nombreDeSuffrages(self.numero)
            if nS>0:
                if b.liste: bn = b.liste.numero
                else: bn = 0
                if bn in self.suffrages_par_liste.keys():
                    self.suffrages_par_liste[bn] += nS
                    if b.double(self.numero): self.doubles_par_liste[bn] += b.poids
                else:
                    self.suffrages_par_liste[bn] = nS
                    self.doubles_par_liste[bn] = 0   # create
                    if b.double(self.numero): self.doubles_par_liste[bn] = b.poids
                self.suffrages += b.suffrages[self.numero]*b.poids
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
            biff = dict(sorted(self.biffe_pour_qui_unique.items(), key=lambda item: item[1], reverse=True))
        else:
            biff = dict(sorted(self.biffe_pour_qui.items(), key=lambda item: item[1], reverse=True))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        nn = 25
        kk = list(biff.keys())[:nn]
        vv = list(biff.values())[:nn]
        cc = [ listes[int(k[0:2])].couleur for k in kk ]  # k est genre "07.16" qui donne listes[7]. 
        y_pos = np.arange(len(kk))
        plt.barh(y_pos,vv,color=cc )
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels=[candidats[k].nom for k in kk])
        plt.xlabel('Biffages de {0}'.format(self.nom))
        if unique:
            plt.title("Biffages de seulement {0} en faveur de ...".format(self.nom))
            deuxPlots("Biffage-Unique-{0}".format(goodName(self.nom)))
        else:
            plt.title("Biffages de {0} en faveur de ...".format(self.nom))
            deuxPlots("Biffage-{0}".format(goodName(self.nom)))
        plt.clf()

    def amis(self,candidats,listes):
        """
        Meilleurs amis
        """
        amis = dict(sorted(self.ajoutes_aussi.items(), key=lambda item: item[1], reverse=True))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        nn = 25
        kk = list(amis.keys())[:nn]
        vv = list(amis.values())[:nn]
        cc = [ listes[int(k[0:2])].couleur for k in kk ]  # k est genre "07.16" qui donne listes[7]. 
        y_pos = np.arange(len(kk))
        plt.barh(y_pos,vv,color=cc )
        plt.gca().invert_yaxis()
        plt.yticks(y_pos, labels=[candidats[k].nom for k in kk])
        plt.xlabel('Amis de {0}'.format(self.nom))
        plt.title("Candidats ajoutés en même temps que {0}".format(self.nom))
        deuxPlots("Amis-{0}".format(goodName(self.nom)))
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
            plt.text(1.02*v, i + .25, str(v), color='blue', fontweight='bold')
        deuxPlots("Suffrages-Candidat-{0}".format(goodName(self.nom)))
        plt.clf()
        plt.xscale('linear')
        
        

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
                    print("Fin du fichier")
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
def parasite(nom,listes):
    """
    qui parasite la liste nom ?
    """
    para = {}
    for l in listes.values():
        if not (l.nom == nom) and not ( l.numero == nom):
            para[l] = l.suffrages_par_liste[nom]
    y_pos = np.arange(len(para.values()))
    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
    para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))
    plt.barh(y_pos,para.values(),color = [l.couleur for l in para.keys()])
    plt.yticks(y_pos, labels=[ l.nom for l in para.keys()])
    if type(nom) is int: nom = listes[nom].nom  # hacky
    plt.xlabel('Suffrages obtenus chez {0}'.format(nom))
    plt.title("Parasitage de {0}".format(nom))
    plt.gca().invert_yaxis()
    deuxPlots("Parasite-{0}".format(goodName(nom)))
    plt.clf()
    
#############################################################################
def candidatsParasites(liste,candidats):
    """
    Candidats parasites sur les listes PVL

    Si nomParti est un parti, il fait donner partis
    """
    para = {}
    listes = []
    if liste.classe == "Parti":
        listes = [ l.numero for l in p.listes ]
    else:
        listes = [ liste.numero ]
#    print("Je cherche les parasites de {0} Listes: {1}".format(liste.nom,listes))
    for c in candidats.values():
        if c.liste.numero in listes : continue
        para[c] = 0
        for l in listes:
            if l in c.suffrages_par_liste.keys():
                para[c] += c.suffrages_par_liste[l]
#    print("Trouvé {0} parasites".format(len(para)))
    para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))
    nn = 25
    kk = list(para.keys())[:nn]
    vv = list(para.values())[:nn]
    y_pos = np.arange(len(kk))
    plt.barh(y_pos,vv,color=[ c.liste.couleur for c in kk ] )
    plt.gca().invert_yaxis()
    plt.yticks(y_pos, labels=[k.nom for k in kk])
    plt.xlabel('Suffrages obtenus chez {0}'.format(liste.nom))
    plt.title("Candidats parasites de {0}".format(liste.nom))
    deuxPlots("CandidatsParasite-{0}".format(goodName(liste.nom)))
    plt.clf()
        
       

#############################################################################
# main
#############################################################################
listes,partis = lisScrutin()
candidats,bulletins = lisBulletins(listes)
attribueListes(candidats,listes)

print("J'ai {0} listes de {1} partis et {2} candidats pour {3} bulletins différents".format(len(listes),len(partis),len(candidats),len(bulletins)))

# suffrages par candidats
for c in candidats.values():
    c.analyse(bulletins)
              
# mise à jour des suffrages par parti
for p in partis.values(): p.miseAjour(listes)

for l in listes.values(): l.check()
for p in partis.values(): p.check()

# vérification
print("##################################################################################")
print("Listes: {0}".format( listes ))
print("Listes: {0}".format( [ k for k in listes[12].suffrages_par_liste.keys()] ))
for p in listes.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_liste.values()]))
print("##################################################################################")
# print("Partis: {0}".format( partis.keys() ))
for p in partis.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_liste.values()],p.suffrages))
print("##################################################################################")

# graphiques pour les listes
for l in listes.values():
    l.suffragesParCandidat()
    l.plotSuffrages(listes)
    parasite(l.numero,listes)
    if l.parti.nom == "PVL" : candidatsParasites(l,candidats)
    l.biffage()

# graphiques pour les partis
for p in partis.values():
    p.plotSuffrages(partis)
    parasite(p.nom,partis)
    candidatsParasites(p,candidats)

# graphiques pour les candidats
for c in candidats.values():
    print("Candidat {0} liste {1} parti {2}".format(c.nom,c.liste.nom,c.liste.parti.nom))
    if c.liste.parti.nom == "PVL":
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


