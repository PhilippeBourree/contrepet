"""
    Modification du dictionnaire "dico_contrepet.txt"
    On modifie le son "oi" en "ö"
    
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        if data:
            if data.startswith('##'):
                continue
            tab_data = data.split("\t")
            if "oi" in tab_data[1]:
                if "oï" not in tab_data[0]:
                    if "oy" in tab_data[0] or "ohy" in tab_data[0]:
                        pho = tab_data[1].replace("oi", "öi")
                    else:
                        pho = tab_data[1].replace("oi", "ö")
                    data = tab_data[0] + "\t" + pho
                    if len(tab_data) > 2:
                        data += "\t" + tab_data[2]
            tab_lignes.append(data)


# écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


