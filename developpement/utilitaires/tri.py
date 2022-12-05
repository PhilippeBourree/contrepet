"""
    Modification du dictionnaire "dico_contrepet.txt"
    Tri des phrase par ordre alphabétique
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :
    datas = f.readlines()
    for data in datas:
        if data:        # suppression des lignes vides
            tab_lignes.append(data)
    
# tri du tableau de ligne par ordre alphabétique
tab_lignes.sort()

#écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


