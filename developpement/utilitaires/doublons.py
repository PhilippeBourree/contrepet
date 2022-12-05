"""
    Modification du dictionnaire "dico_contrepet.txt"
    Tri des phrase par ordre alphabétique et suppression des doublons
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    data_av = ""
    for data in datas:
        if data != data_av:
            tab_lignes.append(data)
        data_av = data
    
#écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


