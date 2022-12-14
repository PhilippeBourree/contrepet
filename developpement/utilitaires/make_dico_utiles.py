"""
    Fabrication des 5 dictionnaires pythons à partir de "dico_contrepet.txt"
"""
dico = "dico_contrepet.txt"

dico_mot = {}       # clé : mot fr,     valeur : phonétique
dico_phonetik = {}  # clé : phonétique, valeur : mot fr
dico_synt = {}      # clé : mot fr,     valeur : renseignements syntaxiques
dico_prio = {}      # clé : mot fr,     valeur : nombre indiquant la priorité, le mot est prioritaire au regard de la théorie contrepétique :
                          # mots grossiers, vulgaires, utilisé dans les contrepèteries ou à double sens... (Ex : bite, macron, enculé, fente...)
dico_prio_pho = {}  # clé : mot pho,    valeur : 1, liste des mots prioritaires en phonétique
                          

def cle_existe(dico, cle):
    """ Renvoie si la clé "cle" existe dans le dictionnaire "dico"
        (dictionnaire, clé)---> Booléen
    """
    return cle in dico

def initialiser_dictionnaires():
    """ Fabrication des dictionnaires """
    global dico_mot
    global dico_phonetik
    global dico_prio
    global dico_prio_pho

    with open(dico, mode='r', encoding='utf-8') as f:
        datas = f.readlines()

    for data in datas:
        if data.startswith('##'):
            continue
        tab_data = data.split("\t")
        lon = len(tab_data)
        mot = tab_data[0].strip().lower()
        pho = tab_data[1].strip()
        synt = eval(tab_data[2].strip())
        dico_mot[mot] = pho
        if not cle_existe(dico_phonetik,
                          pho):  # une phonétique ne correspond pas qu'à un mot, on met le mot dans un tableau
            dico_phonetik[pho] = []
        dico_phonetik[pho].append(mot)
        dico_synt[mot] = synt[0]  # TODO : ne pas prendre que le premier...
        if lon == 4:
            dico_prio[mot] = tab_data[3].replace("\n","")
            dico_prio_pho[pho] = 1

def make_dicos_files():
    """ Écriture des fichiers stockant les dicos"""
    global dico_mot
    global dico_phonetik
    global dico_prio
    global dico_prio_pho
    
    fichier_dico_mot = "dico_mot.py"
    fichier_dico_phonetik = "dico_phonetik.py"
    fichier_dico_prio = "dico_prio.py"
    fichier_dico_synt = "dico_synt.py"
    fichier_dico_prio_pho = "dico_prio_pho.py"

    
    f_w = open(fichier_dico_mot,mode = 'w' ,encoding = 'utf-8')
    f_w.write("dico_mot = ")
    f_w.write(str(dico_mot))
    f_w.close()
    f_w = open(fichier_dico_phonetik,mode = 'w' ,encoding = 'utf-8')
    f_w.write("dico_phonetik = ")
    f_w.write(str(dico_phonetik))
    f_w.close()
    f_w = open(fichier_dico_prio,mode = 'w' ,encoding = 'utf-8')
    f_w.write("dico_prio = ")
    f_w.write(str(dico_prio))
    f_w.close()
    f_w = open(fichier_dico_synt,mode = 'w' ,encoding = 'utf-8')
    f_w.write("dico_synt = ")
    f_w.write(str(dico_synt))
    f_w.close()
    f_w = open(fichier_dico_prio_pho,mode = 'w' ,encoding = 'utf-8')
    f_w.write("dico_prio_pho = ")
    f_w.write(str(dico_prio_pho))
    f_w.close()
    #### TODO : essayer avec tous les dicos dans 1 fichier?
    #### TODO : essayer pickle : https://wiki.python.org/moin/UsingPickle   
    ####                         https://docs.python.org/fr/3/library/pickle.html?highlight=getattr
    ####                voir si on peut importer les fichiers pickle à la compil (.pickle)
    #### TODO : essayer shelves :  
    #### TODO essayer Cython : https://bioinfo-fr.net/cython-votre-programme-python-mais-100x-plus-vite

initialiser_dictionnaires()
make_dicos_files()
