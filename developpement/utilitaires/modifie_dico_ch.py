"""
    Modification du dictionnaire "dico_contrepet.txt"
    Les sons "ch" (chiant) et "k" (caca) ne sont pas différenciés en pseudo phonétique et se traduisent par "k"
    Si le français comprend "ch" on modifie la phonétique en remplaçant "k" par "K" (majuscule)
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:    
        tab_data = data.split(" ")
        if "ch" in tab_data[0] or "Ch" in tab_data[0]:
            pho = tab_data[1].replace("k","K")
            data = tab_data[0] + " " + pho
            if len(tab_data) > 2:
                data += " " + tab_data[2]
        tab_lignes.append(data)
    

#écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


