"""
    Modification du dictionnaire "dico_contrepet.txt"
    On modifie le son "ill" (le son mouillé de "couille") qui est noté tantôt "Y" tantôt "il" : on met tout à "Y"
    Attention ! Il ne faut travailler que sur les parties sélectionnées du fichier : ne pas changer Coutainville
"""


tab_lignes = []

nom_fichier = "work.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        if data:
            tab_data = data.split(" ")
            if "ill" in tab_data[0] :
                pho = tab_data[1].replace("il","Y")
                data = tab_data[0] + " " + pho
                if len(tab_data) > 2:
                    data += " " + tab_data[2]
            tab_lignes.append(data)
    

#écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


