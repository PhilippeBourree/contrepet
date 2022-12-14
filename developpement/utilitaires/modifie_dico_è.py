"""
    Modification du dictionnaire "dico_contrepet.txt"
    Si la terminaison du mot fr est "è", on vire 
"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"

i = 0

with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        if data:
            if data.startswith('##'):
                continue 
            tab_data = data.split("\t")
            mot = tab_data[0]

            if "è\t" in data :
                i += 1            
                continue

            tab_lignes.append(data)

print(str(i)+" lignes modifiées")
# écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


