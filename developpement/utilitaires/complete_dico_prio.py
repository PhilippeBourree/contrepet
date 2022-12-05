
"""
on réccupère les + des anciens fichiers dico_contrepet.txt et on les met à la fin

"""


dico_plus = {}
tab_lignes = []
tab_except = []
nom_fichier_source = "dico_contrepet_plus.txt"
nom_fichier_save = "dico_contrepet.txt"
nom_fichier_sortie = "dico_contrepet2.txt"


with open(nom_fichier_source,mode = 'r' ,encoding = 'utf-8') as f :

    datas_syn = f.readlines()	
    for data in datas_syn:
        tab_data = data.split(" ")
        lon = len(tab_data)
        if lon == 3 :
        
            dico_plus[tab_data[0]] = "+"


with open(nom_fichier_save,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        data = data.strip()       
        tab_data = data.split("\t")

        if tab_data[0] in dico_plus :
            data = data + "\t+"

        tab_lignes.append(data)

# tri du tableau de ligne par ordre alphabétique
tab_lignes.sort()

# écriture du fichier
f_w = open(nom_fichier_sortie,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne+"\n")
f_w.close()



