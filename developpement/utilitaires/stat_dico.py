"""

    
"""



nom_fichier = "dico_contrepet.txt"





tab_fin = []
dico_fin = {}

with open(nom_fichier,mode = 'r' ,encoding = 'utf-8') as f :

    datas = f.readlines()
    nb = 0
    for data in datas:
        if data:
            if data.startswith('##'):
                continue
            tab_data = data.split("\t")
            # print(data)
            mot = tab_data[0]
            pho = tab_data[1]
            # if len(pho) >= 2:
                # tab_fin.append(pho[-2:])
            # if len(pho) < 3:
            # if mot[-1] == "s" and pho[-1]== "s" :
            # if "eu" in mot and "eu" in pho:
                # tab_fin.append(mot+" " + pho)
            if len(pho) == 2:
                if pho in dico_fin:
                    dico_fin[pho] += 1
                else :
                    dico_fin[pho] = 1
            
            
# tab_fin = list(set(tab_fin))
# print(sorted(tab_fin))
for el in dico_fin:
    if dico_fin[el] == 1:
        print( el)

# VOYELLES_PHO = ["a", "â", "e", "é", "è", "ê", "i", "o", "ô", "ö", "u", "û", "1", "2", "Y"]  # voyelles de la transcription phonétique
# CONSONNES_PHO_SUBS = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q" \
                    # , "r", "s", "t", "v", "w", "x", "z", "S", "K"]   

# tab_ref = VOYELLES_PHO + CONSONNES_PHO_SUBS
# tab_ref = list(set(tab_ref))
# print(sorted(tab_ref))

