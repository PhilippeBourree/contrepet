
"""
Le but est de rajouter une colonne dans le fichier de départ. 
Cette colonne - tirée du dictionnaire grammalecte - contrient des renseignements syntaxiques séparés par des espaces.


1/ remplacer espace par tab dans mon fichier
2/ ajouter renseignements après pho séparé par tab


"""


dico_syn = {}
tab_lignes = []
tab_except = []
nom_fichier_entree = "dico_contrepet - Copie.txt"
nom_fichier_sortie = "dico_contrepet.txt"
nom_fichier_source = "lexique-grammalecte-fr-v7.0.txt"
nom_fichier_erreur = "dico_erreurs.txt"

with open(nom_fichier_source,mode = 'r' ,encoding = 'utf-8') as f :

    datas_syn = f.readlines()	
    for data in datas_syn:
        tab_data = data.split("\t")
        
        mot = tab_data[2]       # le mot fr
        mot = mot.replace("œ","oe")     # pour faciliter le tri et les traitements ultérieurs
        mot = mot.replace("Œ","OE")
        synt = tab_data[4]      # les infos syntaxiques

        if not mot in dico_syn :        # les infos syntaxiques peuvent ne pas être unique
            dico_syn[mot] = []
        dico_syn[mot].append(synt)


with open(nom_fichier_entree,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:    
        tab_data = data.split(" ")

        if not tab_data[0] in dico_syn :
            tab_except.append(data)
        else :
            tab_ligne = []
            tab_ligne.append(tab_data[0])
            pho = tab_data[1].strip()    
            tab_ligne.append(pho)
            synt = "[" + ",".join(dico_syn[tab_data[0]]) + "]"
            tab_ligne.append(synt)
            ligne  = "\t".join(tab_ligne)
            tab_lignes.append(ligne)

    
# tri du tableau de ligne par ordre alphabétique
tab_lignes.sort()

# écriture du fichier
f_w = open(nom_fichier_sortie,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne+"\n")
f_w.close()

# écriture du fichier des erreurs pour traitement ultérieur
f_w = open(nom_fichier_erreur,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_except :
    f_w.write(ligne)
f_w.close()

