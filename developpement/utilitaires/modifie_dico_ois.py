"""
    Modification du dictionnaire "dico_contrepet.txt"
    Si la terminaison du mot fr est "ois" la terminaison du mot pho doit être ö (son oi)
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
            if "ois\t" in data and "ös\t" in data:
                data = data.replace("ös\t", "ö\t")
            tab_lignes.append(data)


# écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


