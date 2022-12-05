"""
    fabrication du dictionnaire "dico_contrepet.txt" à partir du fichier "lexique-grammalecte-fr-v7.0.txt"
    https://grammalecte.net/
    2 colonnes : mot et phonétique
"""


tab_lignes = []


nom_fichier_entree = "lexique-grammalecte-fr-v7.0.txt"
nom_fichier_sortie = "dico_contrepet.txt"

with open(nom_fichier_entree,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()		# !!! bonne pratique : le close() est fait automatiquement à la fin du with
    for data in datas:    
        tab_data = data.split("\t")
        # élimination des enregistrements contenant des lettres pourries
        flag = True
        mot = tab_data[2]
        
        lettres_pourries = '₀₁₂₃₄₅₆₇₈₉0123456789$(*,.:?Δαεηικμνξπυφχ‰€ℓØ¿ᵉˢΩω'

        for car in lettres_pourries:
                if car in mot:
                    flag = False
                    continue
                    
        if flag :
            if len(tab_data) < 6:
                continue
            mot = mot.replace("œ","oe")         # pour faciliter le tri et les traitements ultérieurs
            mot = mot.replace("Œ","OE")
            #æ
            phonetique = tab_data[5]   #.replace("2","eu")   # pour faciliter la recherche de contrepèteries
            if phonetique.strip():
                ligne = mot+" "+phonetique
                tab_lignes.append(ligne)


# tri du tableau de ligne par ordre alphabétique
tab_lignes.sort()

# écriture du fichier
f_w = open(nom_fichier_sortie,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne+"\n")
f_w.close()


