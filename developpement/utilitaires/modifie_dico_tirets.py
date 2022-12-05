"""
    Modification du dictionnaire "dico_contrepet.txt"
    Virer tous les mots à tirets
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        if data:
            tab_data = data.split(" ")
            if "-" in tab_data[0] :
                continue
            tab_lignes.append(data)
    

#écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


