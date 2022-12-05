"""
    Chercher les doublons du dictionnaire "dico_contrepet.txt"

"""


tab_lignes = []

nom_fichier = "dico_contrepet.txt"

with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :
    datas = f.readlines()
    ex = ""
    for data in datas:    
        tab_data = data.split("\t")
        if tab_data[0] == ex:
            print(ex) 
        ex = tab_data[0]
    


