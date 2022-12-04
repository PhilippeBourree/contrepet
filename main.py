"""
    CONTREPET est distribué sous les termes de la Licence Publique Générale GNU Version 3 (GNU GPL [General Public License]), CONTREPET est un logiciel libre
    Copyright Philippe Bourrée, pncefbh@gmail.com
"""

from tkinter import *
from contrepet import *
import pkgutil

LARGEUR = 1000      # largeur de la fenêtre
HAUTEUR = 720       # hauteur de la fenêtre
TITRE = "'Contrepet - Version 1.0.0.0 Patch 0 Release 0'"
BARATIN =   "\nFélicitations! Vous avez entre les mains le meilleur programme de résolution de contrepèteries! Faut dire qu'il n'y en a pas d'autre...\n\n" \
            "Ce programme traite les permutations simples : une seule permutation et il a quelque problème avec les apostrophes : personne n'est parfait.\n" \
            "Dernier détail : il met entre 3 et 50 secondes pour trouver (ou pas : il n'en résoud à peine que la moitié...)\n" \
            "Quelques exemples, amusez-vous:"

BARATIN_FIN =   "Le coin du spécialiste :\t" \
                "Le programme est écrit en python 3.10.7, le code source est en accès libre sur github\t" \
                "Contact : pncefbh@gmail.com\n" \
                "Ce logiciel utilise Grammalecte https://grammalecte.net/"


def afficher_ligne(ligne, res=False):
    """ Affiche une ligne de texte dans la zone de résultat 
        Si res est vrai, c'est probablement une bonne réponse  : on surligne
    """
    # print("INSERT AV",texte_valeur.index(INSERT)," ",ligne)
    if res:
        texte_valeur.insert(END, ligne +"\n", "yellow")
    else:
        texte_valeur.insert(END, ligne +"\n")
    root.update()


def afficher_ligne_gg(nb):
    afficher_ligne(str(nb) + " appel gg")


def afficher_resultat(tab_new_phrases, tA, tB):
    """ Affichage des résultats """
    if tab_new_phrases:
        en_tete = "\nnum".ljust(15) + "nb reponses".ljust(20) + "réponses possibles".ljust(50)
        nb = 0
        afficher_ligne(en_tete)
        for nouvelle_phrase in tab_new_phrases:
            couleur = False
            if int(nouvelle_phrase[0]) > TOLERANCE_GG:
                couleur = True

            ligne = ("Ligne " +str(nb)).ljust(15) + str(nouvelle_phrase[0]).ljust(20) + nouvelle_phrase[1].ljust(50)
            afficher_ligne(ligne, couleur)
            nb += 1
    else:
        afficher_ligne("\nEnfer et dalmatien! Je n'ai rien trouvé!")
    
    # temps de réponse
    afficher_ligne("\nTemps de réponse : " + str(round(tB - tA, 2)) + " secondes" )


# TODO : voir yscrollcommand


def raz():
    """ Remise à zéro """
    var_phrase.set("")
    texte_valeur.delete("1.0","end")


def afficher_exemple():
    """ Comme son nom l'indique, Exemples proposés à la foule en liesse: """
    exemple = "la poule qui mue\t\t\tune fine appellation\t\t\t\tvotre dent qui part\t\t\t\tà pied par la Chine\n" \
                "panne de micro\t\t\tlâchez-moi la patte\t\t\t\tle bras sur la chaise\t\t\t\tquelle bouille\n" \
                "boire ça vite\t\t\tla cure du foie\t\t\t\tretire ta lampe que je guette\t\t\til aime vachement ton frangin\n" \
                "vite et bien\t\t\tlaissez nos péniches\t\t\t\tla berge précède le vide\t\t\t\tbrouiller l'écoute\n" \
                "ça pue dans le car\t\t\tles belles frites\t\t\t\tton entrain gène\t\t\t\tla fine ou l'épaisse\n" 
    #            J'ai du tracas jusqu'au cou      \n"
    """
        un champ de coton          
        
        glisser dans la piscine 
        le linge à sécher
        un tennis prévisible

    """

    text_exemple.insert(END, exemple)
    text_exemple.configure(state="disabled")
    

def verif_gg_tab_vis(phrase_orig, phrase_tab_phon, tab_new_phrase):
    """ Lancer la vérification du tableau par gg
        si le nombre de résultats renvoyé est supérieur à TOLERANCE_GG, la phrase est censée exister. """

    tab_retour = []
    tab_deja_fait = []
    cpt_rech_gg = 0
    cpt_rep_ok = 0
    for new_tup in tab_new_phrase:
        # print("gg_bloqueA::",gg_bloque)
        new_phrase = new_tup[0]
        if new_phrase in tab_deja_fait:
            continue
        if ACTIVER_GG and not gg_bloque:
            if cpt_rep_ok < NB_REPONSE_MAX_GG and cpt_rech_gg < NB_MAX_APPELS_GG:
                cpt_rech_gg += 1
                afficher_ligne_gg(cpt_rech_gg)
                tuple_phrase = gg_est_mon_ami(phrase_orig, phrase_tab_phon, new_phrase)
                if tuple_phrase[2]:  # gg a fait une suggestion
                    suggestion_existe = verif_suggestion_gg(tab_new_phrase, tuple_phrase)
                    if tuple_phrase[0] == 666 and suggestion_existe:
                        return [tuple_phrase]  # c'est la bonne ! on renvoie

                    if not suggestion_existe and tuple_phrase[1]:  # la phrase est une suggestion gg n'existant pas encore dans la liste
                        # tab_retour.append(tuple_phrase)                             # on stocke le résultats
                        tab_deja_fait.append(tuple_phrase[1])
                        cpt_rech_gg += 1
                        afficher_ligne_gg(cpt_rech_gg)
                        cpt_rech_gg += 1
                        tuple_phrase = gg_est_mon_ami(phrase_orig, phrase_tab_phon, tuple_phrase[1])  # on relance la recherche avec la suggestion
                if int(tuple_phrase[0]) > TOLERANCE_GG:
                    cpt_rep_ok += 1
            else:
                break
        else:
            tuple_phrase = (0, new_phrase, "")
        tab_deja_fait.append(new_phrase)
        tab_retour.append(tuple_phrase)
    return tab_retour


def chercher_contrepet(phrase):
    """ Le coeur de la bête """
    texte_valeur.delete("1.0","end")        # effacer la zone d'affichage
    
    esp1 = 28
    esp2 = 9
    esp3 = 20
    esp4 = 30
    
    t0 = time()
    # analyse & transformation de la phrase
    apos = contient_apos(phrase)
    tab_phrase_init = get_tab_phrase(phrase)
    phrase_pho = get_phrase_pho(tab_phrase_init)
    phrase_pho_esp = get_phrase_pho(tab_phrase_init, " ")
    phrase_tab_phon = get_tab_phonemes(phrase_pho_esp)
    print("phrase_pho>>>", phrase_pho)
    print("phrase_tab_phon>>>", phrase_tab_phon)
    afficher_ligne("Temps".ljust(esp2) + "Action".ljust(esp1))
    print("l:", cle_existe(dico_phonetik, "l"))

    t1 = time()
    afficher_ligne(str(round(t1 - t0)).ljust(esp2) + "analyse".ljust(esp1))
    
    tab_subst = get_sous_chaines(phrase_pho)
    nb2 = len(tab_subst)
    t2 = time()
    afficher_ligne(str(round(t2 - t1, 4)).ljust(esp2) + (str(nb2)+" sous chaines de substitution trouvées").ljust(esp3) )

    # print(tab_subst) 


    tab_chaines = get_chaines_substituees(phrase_pho, tab_subst)
    nb3 = len(tab_chaines)
    t3 = time()
    afficher_ligne(str(round(t3 - t2, 4)).ljust(esp2) + (str(nb3) + " chaines substituées trouvées").ljust(esp3))     
          
    # print(tab_chaines)   
      
          
    tab_phrases = get_toutes_phrases(tab_chaines)
    nb4 = len(tab_phrases)
    t4 = time()
    afficher_ligne(str(round(t4 - t3, 4)).ljust(esp2) + (str(nb4) + " phrases phonétiques possibles").ljust(esp3))
    if nb4 > NB_MAX_PHRASES_PHO:
        afficher_ligne("Trop de possibilités, on arrête tout...")
        return []
        
    # print(tab_phrases)    

    tab_phrases = verif_phonemes_pho(tab_phrases, phrase_tab_phon)
    if tab_phrases:
        nb5 = len(tab_phrases)
        t5 = time()
        afficher_ligne(str(round(t5 - t4, 4)).ljust(esp2) + "Vérification phonétique: ".ljust(esp1) +
            (str(nb4 - nb5) + " solutions éliminées").ljust(esp4)  + (str(nb5) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_tup = get_tup_phrases(tab_phrase_init, tab_phrases)
    if tab_new_tup:
        nb6 = len(tab_new_tup)
        t6 = time()
        afficher_ligne(str(round(t6 - t5, 4)).ljust(esp2) + (str(nb6) + " phrases françaises correspondantes").ljust(esp3))
    else:
        return []
        
    # print(tab_new_tup)    
        
        
    if nb6 > NB_MAX_PHRASES_FR:
        afficher_ligne("".ljust(esp2) + (str(nb6) + " >> Beaucoup de possibilités : patience...").ljust(esp3))

    tab_new_tup = verif_phonemes_tab(phrase_tab_phon, tab_new_tup)
    if tab_new_tup:
        nb7 = len(tab_new_tup)
        t7 = time()
        afficher_ligne(str(round(t7 - t6, 4)).ljust(esp2) + "Vérification phonétique fr: ".ljust(esp1) +
              (str(nb6 - nb7) + " solutions éliminées").ljust(esp4)  + (str(nb7) + " solutions restantes").ljust(esp4))
    else:
        return []
        
    # print(tab_new_tup)   
        

    tab_new_tup = verif_synt_tab(tab_new_tup)
    if tab_new_tup:
        nb8 = len(tab_new_tup)
        t8 = time()
        afficher_ligne(str(round(t8 - t7, 4)).ljust(esp2) + "Vérification syntaxique: ".ljust(esp1) +
            (str(nb7 - nb8) + " solutions éliminées").ljust(esp4)  + (str(nb8) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_tup = classer_reponses(tab_new_tup, tab_phrase_init)
    if tab_new_tup:
        nb9 = len(tab_new_tup)
        t9 = time()
        afficher_ligne(str(round(t9 - t8, 4)).ljust(esp2) + "Classement des réponses: ".ljust(esp1) +
            (str(nb8 - nb9) + " solutions éliminées").ljust(esp4)  + (str(nb9) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_tup = verif_grammalecte_tab(tab_new_tup)
    if tab_new_tup:
        nb10 = len(tab_new_tup)
        t10 = time()
        afficher_ligne(str(round(t10 - t9, 4)).ljust(esp2) + "Vérification Grammalecte: ".ljust(esp1) +
            (str(nb9 - nb10) + " solutions éliminées").ljust(esp4)  + (str(nb10) + " solutions restantes").ljust(esp4))
    else:
        return []
        
    tab_new_tup = comparer_initial(phrase, tab_new_tup)
    if tab_new_tup:
        nb11 = len(tab_new_tup)
        t11 = time()
        afficher_ligne(str(round(t11 - t10, 4)).ljust(esp2) + "Comparaison avec départ: ".ljust(esp1) +
            (str(nb10 - nb11) + " solutions éliminées").ljust(esp4)  + (str(nb11) + " solutions restantes").ljust(esp4))
    else:
        return []   
        

    tab_new_phrase = verif_gg_tab_vis(phrase, phrase_tab_phon, tab_new_tup)
    tab_new_phrase.sort(reverse=True)
    nb12 = len(tab_new_phrase)
    t12 = time()
    afficher_ligne(str(round(t12 - t11, 4)).ljust(esp2) + "Vérification gg: ".ljust(esp1) + 
        (str(nb11 - nb12) + " solutions éliminées").ljust(esp4)  + (str(nb12) + " solutions restantes").ljust(esp4))

    # print(tab_new_phrase)

    return tab_new_phrase


def chercher():
    """ Lancer la recherche """ 
    phrase = input_phrase.get()
    
    if phrase:
        tA = time()
        phrase = traiter_saisie(phrase)
        tab_new_phrases = chercher_contrepet(phrase)
        # root.update()
        tB = time()
        afficher_resultat(tab_new_phrases, tA, tB)

def fct_touche_entree(event):
    """ La touche entrée déclenche la recherche """ 
    chercher()


 
# Programme principal
root = Tk()

# root.iconbitmap('.\\contrepet.ico')
root.geometry(str(LARGEUR)+"x"+str(HAUTEUR))
root.title(TITRE)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=6)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=10)
root.rowconfigure(4, weight=1)

var_phrase = StringVar(root,value='')

label_titre = Label(root, text="CONTREPET",justify = CENTER)
label_titre.grid(row=0, column=0, columnspan=5)

label_baratin = Label(root, text=BARATIN,justify = LEFT)
label_baratin.grid(row=1, column=0, columnspan=5, ipadx =20)

text_exemple = Text(root, height=1, borderwidth=0)
text_exemple.grid(row=2, column=0, columnspan=5,pady=(0,5), padx =20, sticky="nsew")
afficher_exemple() 

label_phrase = Label(root, text="Entrer le texte:")
label_phrase.grid(row=3, column=0)
input_phrase = Entry(root, width=30, textvariable=var_phrase)
input_phrase.grid(row=3, column=1, sticky="nsew")

bouton_chercher = Button(root, text="Chercher", command=chercher)
bouton_chercher.grid(row=3, column=2)

bouton_raz = Button(root, text="Effacer", command=raz)
bouton_raz.grid(row=3, column=3)

bouton_quitter = Button(root, text="Quitter", command=root.destroy)
bouton_quitter.grid(row=3, column=4)


label_res = Label(root, text="Resultat")
label_res.grid(row=4, column=0 ,pady=10)

texte_valeur = Text(root)
texte_valeur.grid(row=4, column=1, columnspan=4 ,pady=10, padx =(0, 20), sticky="nsew")
texte_valeur.tag_config("yellow", background="yellow")

label_baratin_fin = Label(root, text=BARATIN_FIN,justify = LEFT)
label_baratin_fin.grid(row=5, column=0, columnspan=5, ipadx =20)


root.bind('<Return>', fct_touche_entree)
# pb.start()

root.mainloop()



