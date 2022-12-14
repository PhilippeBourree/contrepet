"""
    Modification du dictionnaire "dico_contrepet.txt"
    Si la terminaison du mot fr est "oute", "outent" ou "outes" la terminaison du mot pho doit être ût 
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
            if ("oute\t" in data or "outes\t" in data or"outent\t" in data ) and "û\t" in data:
                data = data.replace("û\t", "ût\t")
                i += 1
            tab_lignes.append(data)

print(str(i)+" lignes modifiées")
# écriture du fichier
f_w = open(nom_fichier,mode = 'w' ,encoding = 'utf-8')
for ligne in tab_lignes :
    f_w.write(ligne)
f_w.close()


