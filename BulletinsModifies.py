import csv

_file = 'export-bulletins-PR-CHCN-20231022.csv'
_summary = 'ScrutinsParListe.csv'
_sd = "Sans dénom."
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(7,5))
fig, ax = plt.subplots()

def goodName(name):
    name2 = name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace(">","_g_").replace("<","_l_").replace("*","_times_").replace(".","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_").replace("||","_or_").replace("&&","_and_").replace("&","_").replace("|","_").replace(":","_vs_").replace("'","_").replace("#","N").replace('·','_')
    return name2

#############################################################################
class Bulletin():
    """
    Une catégorie unique de bulletin
    """
    def __init__(self,row,candidats):
#        print("Row {0}".format(row))
        self.poids = int(row[0])
        self.liste = None   # sera attribué plus tard
        self.liste_id = int(row[1][:3])
        self.complementaires = int(row[2])
        c_id = list(candidats.keys())  # les identifiants de tous les candidats
        self.suffrages = {}
        for l in range(len(c_id)):   # 
            v = int(row[3+l])        # nombre de voix du candidat l
            if int(v)>0: self.suffrages[ c_id[l] ] = v
#        print(u'Créé bulletin avec poids {0}, liste {1}, complémentaires {2}, suffrages {3}'.format(self.poids,self.liste,self.complementaires,self.suffrages[0:20]))

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

#############################################################################
class Liste():
    """
    Liste
    """
    def __init__(self,row):
        self.index = int(row[0])
        self.nom = row[1]
        self.suffrages_liste_complete = int(row[2])+int(row[3])
        self.suffrages_nom_liste_modifiee = int(row[4])
        self.suffrages_comp_liste_modifiee = int(row[5])
        self.suffrages_autres_listes = int(row[7])
        self.suffrages_sans_denom = int(row[8])
        self.suffrages = self.suffrages_liste_complete+self.suffrages_nom_liste_modifiee+self.suffrages_comp_liste_modifiee+self.suffrages_autres_listes+self.suffrages_sans_denom
        self.classe = "Liste"
        print("Nouvelle liste {0:2} {1} a {2} suffrages".format(self.index,self.nom,self.suffrages))
        
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
        self.suffrages_par_parti = {}
        self.doubles_par_parti = {}
        
    def connu(self,nom):
        """
        Liste déja existante?
        """
        return self.index == int(nom.split(' ')[0])
    
    def miseAjour(self, candidat):
        """
        Ajoute les suffrages d'un candidat
        """
#        print("Suffrages du candidat {0}: {1}".format(candidat.nom, candidat.suffrages_par_parti))
#        print("Suffrages du parti    {0}: {1}".format(self.nom, self.suffrages_par_parti))
        for k in candidat.suffrages_par_parti.keys() : self.suffrages_par_parti[k] += candidat.suffrages_par_parti[k]
        for k in candidat.doubles_par_parti.keys() : self.doubles_par_parti[k] += candidat.doubles_par_parti[k]
        # print("Liste {0} a {1} suffrages depuis {2}".format(self.nom,self.suffrages,self.suffrages_par_parti))

    def check(self):
        s = sum([v for v in self.suffrages_par_parti.values()])
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
        colors = {_sd: "black"}
        suffs = {}
        for k in self.suffrages_par_parti.keys():
            suffs[k] = self.suffrages_par_parti[k]
#            print("Pour {0} je cherche {1}".format(self.nom,k))
            for l in listes.values():
                if l.nom == k :
                    colors[k] = l.couleur
#                    print('Trouvé liste {0} couleur {1}'.format(l.nom,l.couleur))
                    break # Ne pas continuer à chercher
                elif l.parti.nom == k :
                    colors[k] = l.couleur
#                    print('Trouvé parti {0} couleur {1}'.format(l.parti.nom,l.couleur))
                    break
#                else: colors.append('black')
#        print(self.nom,self.suffrages_par_parti.keys(),colors)

        para = dict(sorted(suffs.items(), key=lambda item: item[1], reverse=True))
      
        y_pos = np.arange(len(para.values()))
        fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
        plt.barh(y_pos,para.values(),color=[colors[k] for k in list(para.keys())])
        plt.yticks(y_pos, labels=(para.keys()))
        plt.xlabel('Suffrages')
        plt.title(self.nom)
        plt.gca().invert_yaxis()
        plt.savefig("plots/Suffrages-{1}-{0}.pdf".format(goodName(self.nom),self.classe))
        plt.savefig("plots/png/Suffrages-{1}-{0}.png".format(goodName(self.nom),self.classe))
        plt.clf()

#############################################################################
class Parti(Liste):
    """
    Un parti est une somme de listes
    """
    def __init__(self,nom,listes):
        self.nom = nom
        self.nom_parti = nom
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
        self.suffrages_par_parti = {}
        self.doubles_par_parti = {}
        self.classe = "Parti"
        print("Nouveau parti {0} contenant {1} listes".format(self.nom_parti,len(self.listes)))

    def miseAjour(self,listes):
        """
        Mise à jour des suffrages du parti

        Je pourrais probablement simplifier maintenant que ce sont des dictionnaires
        """
        for l in listes.values():  # je boucle sur les listes
            if l.nom_parti != self.nom : continue    # je ne garde que les listes du parti
            for k in l.suffrages_par_parti.keys():  # je boucle encore sur les listes
                if k==_sd: pi = k  # sans dénomination
                else:   # je cherche le parti de k
                    for ll in listes.values():
                        if ll.nom==k : pi = ll.nom_parti
                if pi in self.suffrages_par_parti.keys():
                    print(u"{0} Trouvé {1} - j'ajoute {2}".format(self.nom,pi,l.suffrages_par_parti[k]))
                    self.suffrages_par_parti[pi] += l.suffrages_par_parti[k]
                    self.doubles_par_parti[pi] += l.doubles_par_parti[k]
                else:
                    print(u"{0} Nouveau {1} - je crée avec {2}".format(self.nom,pi,l.suffrages_par_parti[k]))
                    self.suffrages_par_parti[pi] = l.suffrages_par_parti[k]
                    self.doubles_par_parti[pi] = l.doubles_par_parti[k]
                
        # print("Le parti {0} a des suffrages de {1}".format(self.nom,self.suffrages_par_parti))

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
        # print(u'Crée candidat {0} liste {1:2}, place {2:2}: {3}'.format(self.index,self.liste_id,self.place,self.nom))
        self.pvl = None
        self.suffrages_par_parti = {}
        self.doubles_par_parti = {}
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
                if b.liste: bn = b.liste.nom
                else: bn = _sd
                if bn in self.suffrages_par_parti.keys():
                    self.suffrages_par_parti[bn] += nS
                    if b.double(self.numero): self.doubles_par_parti[bn] += b.poids
                else:
                    self.suffrages_par_parti[bn] = nS
                    self.doubles_par_parti[bn] = 0   # create
                    if b.double(self.numero): self.doubles_par_parti[bn] = b.poids
                self.suffrages += b.suffrages[self.numero]*b.poids
                    
#        print("Candidat {0} a {1} suffrages dans {2}".format(self.nom,self.suffrages,self.suffrages_par_parti))

        self.liste.miseAjour(self)

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
                if b.liste_id>0: b.liste = listes[b.liste_id]
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
            if c.liste_id == l.index: c.liste = l
        # print("Candidat {0} est du parti {1}".format(c.nom,c.liste.nom_parti))
                
#############################################################################
def redistribue(listes,bulletins):
    """
    Redistribue les scrutins sans dénomination qui sont en fait des listes modifiées
    Assigne aussi les listes aux bulletins
    """
    print("Listes {0}".format([[n,l.nom] for n,l in zip(listes.keys(),listes.values())]))
    
    for b in bulletins:
        if b.liste_id == 0:   
            for s in b.suffrages.keys():
                print("Suffrage pour candidat {0}".format(s))
    exit()
    
#############################################################################
def lisScrutin():
    """
    Résumé du canton par liste
    https://www.elections.vd.ch/votelec/app21/index.html?id=CHCN20231022#v=listsCandidats&m=moreDetails&r=listSuffOrigin
    """
    listes = {}
    partis = {}
    noms_des_listes = [_sd]  # mettre sans dénomination en premier

    with open(_summary) as f:
        ff = csv.reader(f)
        nL = 0  # ligne
        for row in ff:
            nL += 1
            if nL>=4 and not "Total" in row[0]:  
                l=Liste(row)
                listes[l.index] = l
                noms_des_listes.append(row[1])

    # mettre à jour la liste des listes
    for l in listes.values():
        for nl in noms_des_listes:
            l.suffrages_par_parti[nl] = 0
            l.doubles_par_parti[nl] = 0
            

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
        if not l.nom == nom :
            para[l] = l.suffrages_par_parti[nom]
    y_pos = np.arange(len(para.values()))
    fig.subplots_adjust(top=0.93,right=0.97,bottom=0.12,left=0.25)
    para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))
    plt.barh(y_pos,para.values(),color = [l.couleur for l in para.keys()])
    plt.yticks(y_pos, labels=[ l.nom for l in para.keys()])
    plt.xlabel('Suffrages obtenus chez {0}'.format(nom))
    plt.title("Parasitage de {0}".format(nom))
    plt.gca().invert_yaxis()
    plt.savefig("plots/Parasite-{0}.pdf".format(goodName(nom)))
    plt.savefig("plots/png/Parasite-{0}.png".format(goodName(nom)))
    plt.clf()
    
#############################################################################
def candidatsParasites(nomParti,candidats,partis=None):
    """
    Candidats parasites sur les listes PVL

    Si nomParti est un parti, il fait donner partis
    """
    para = {}
    listes = []
    if partis:
        for p in partis.values():
            if nomParti==p.nom : listes = [ l.nom for l in p.listes ]
    else:
        listes = [ nomParti ]

    for c in candidats.values():
        if c.liste.nom in listes : continue
        para[c] = 0
        for l in listes:
            if l in c.suffrages_par_parti.keys():
                para[c] += c.suffrages_par_parti[l]
    para = dict(sorted(para.items(), key=lambda item: item[1], reverse=True))
    nn = 25
    kk = list(para.keys())[:nn]
    vv = list(para.values())[:nn]
    y_pos = np.arange(len(kk))
    plt.barh(y_pos,vv,color=[ c.liste.couleur for c in kk ] )
    plt.gca().invert_yaxis()
    plt.yticks(y_pos, labels=[k.nom for k in kk])
    plt.xlabel('Suffrages obtenus chez {0}'.format(nomParti))
    plt.title("Candidats parasites de {0}".format(nomParti))
    plt.savefig("plots/CandidatsParasite-{0}.pdf".format(goodName(nomParti)))
    plt.savefig("plots/png/CandidatsParasite-{0}.png".format(goodName(nomParti)))
    plt.clf()
    
            
        

#############################################################################
# main
#############################################################################
listes,partis = lisScrutin()
candidats,bulletins = lisBulletins(listes)
attribueListes(candidats,listes)

print("J'ai {0} listes de {1} partis et {2} candidats pour {3} bulletins différents".format(len(listes),len(partis),len(candidats),len(bulletins)))

# redistribue les listes sans dénomination qui sont en fait des listes de parti modifées.
# redistribue(listes,bulletins)

# suffrages par candidats
for c in candidats.values():
    c.analyse(bulletins)
              
# mise à jour des suffrages par parti
for p in partis.values(): p.miseAjour(listes)

for l in listes.values(): l.check()
for p in partis.values(): p.check()

# vérification
print("##################################################################################")
print(partis)
print("Listes: {0}".format( [ k for k in listes[12].suffrages_par_parti.keys()] ))
for p in listes.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_parti.values()]))
print("##################################################################################")
print("Partis: {0}".format( partis.keys() ))
for p in partis.values(): print("{0} a {1} suffrages dont {2} mod. de {3}".format(p.nom,p.suffrages,p.suffrages-p.suffrages_liste_complete-p.suffrages_comp_liste_modifiee,[v for v in p.suffrages_par_parti.values()],p.suffrages))
print("##################################################################################")

# plots
for p in partis.values():
    p.plotSuffrages(listes)
    parasite(p.nom,partis)
    candidatsParasites(p.nom,candidats,partis)
for l in listes.values():
    l.plotSuffrages(listes)
    parasite(l.nom,listes)
    if l.parti.nom == "PVL" : candidatsParasites(l.nom,candidats)


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
"""


