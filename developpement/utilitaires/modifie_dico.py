"""
    Modification du dictionnaire "dico_contrepet.txt"
    Les sons "ill" (brouille, couillon, ceux avec le son mouillé "ye", pas ville par exemple) 
    sont traduit tantôt par "il" tantôt pa "Y" ==> tout transformer en "Y" 
    Attention travailler par morceaux de "dico_contrepet.txt" plein d'exceptions
"""


tab_lignes = []

nom_fichier = "work.txt"



with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()

    for data in datas:    
        tab_data = data.split(" ")
        if "ill" in tab_data[0] 
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


