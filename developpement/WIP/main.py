"""
    CONTREPET est distribué sous les termes de la Licence Publique Générale GNU Version 3 (GNU GPL [General Public License]), CONTREPET est un logiciel libre
    Copyright Philippe Bourrée, pncefbh@gmail.com
"""

from tkinter import *
from contrepet import *


LARGEUR = 1000      # largeur de la fenêtre
HAUTEUR = 700       # hauteur de la fenêtre
TITRE = "'Contrepet - Version 1.0.0.0 Patch 0 Release 0'"
BARATIN =   "\nFélicitations! Vous avez entre les mains le meilleur programme de résolution de contrepèteries! Faut dire qu'il n'y en a pas d'autre...\n\n" \
            "Ce programme ne traite que les permutations simples (une seule permutation).\n" \
            "Dernier détail : il met entre 4 et 785 secondes pour trouver (ou pas : il n'en résout à peine que la moitié...)\n" \
            "Quelques exemples, amusez-vous à en trouver d'autres:"

BARATIN_FIN =   "Le coin du spécialiste :\t" \
                "Le programme est écrit en python 3.10.7, le code source est en accès libre sur github\t" 
ggg_bloque = False  # Passe à True si tu a été blacklisté par gg (ça dure quelques heures...)
NB_MAX_RES = 6      # Nombre de résultats à afficher si blacklistage


def afficher_ligne(ligne, retour=True, couleur=False):
    """ Affiche une ligne de texte dans la zone de résultat 
        Si couleur existe, on surligne
    """
    if retour:
        ligne = ligne  + "\n"
    if couleur:
        texte_valeur.insert(END, ligne , couleur)
    else:
        texte_valeur.insert(END, ligne)
    root.update()


def afficher_ligne_gg(nb):
    afficher_ligne(str(nb) + " appel gg\t\t", retour=False)


def afficher_resultat(tab_new_phrases, tA, tB):
    """ Affichage des résultats """
    if tab_new_phrases:
        en_tete = "\nnum".ljust(15) + "nb reponses".ljust(20) + "réponses possibles".ljust(50)
        nb = 0
        afficher_ligne(en_tete)
        for nouvelle_phrase in tab_new_phrases:
            couleur = ""
            if int(nouvelle_phrase[0]) > TOLERANCE_GG:
                couleur = "yellow"

            ligne = ("Ligne " + str(nb)).ljust(15) + str(nouvelle_phrase[0]).ljust(20) + nouvelle_phrase[1].ljust(50)
            afficher_ligne(ligne, couleur=couleur)
            nb += 1
    else:
        afficher_ligne("\nEnfer et dalmatien! Je n'ai rien trouvé!")
    # temps de réponse
    afficher_ligne("\nTemps de réponse : " + str(round(tB - tA, 2)) + " secondes" )

def raz():
    """ Remise à zéro """
    var_phrase.set("")
    texte_valeur.delete("1.0","end")


def afficher_exemple():
    """ Comme son nom l'indique, Exemples proposés à la foule en liesse: """
    exemple = "la poule qui mue\t\t\tune fine appellation\t\t\t\tvotre dent part\t\t\t\tà pied par la Chine\n" \
                "panne de micro\t\t\tlâchez-moi la patte\t\t\t\tle bras sur la chaise\t\t\t\tquelle bouille\n" \
                "boire ça vite\t\t\tla cure du foie\t\t\t\tretire ta lampe que je guette\t\t\til aime vachement ton frangin\n" \
                "une bouille incroyable\t\tlaissez nos péniches\t\t\t\t\tla berge précède le vide\t\t\t\tbrouiller l'écoute\n" \
                "ça pue dans le car\t\t\tles belles frites\t\t\t\tton entrain gène\t\t\t\tla fine ou l'épaisse\n" \
                "fou de la messe\t\t\tsalut fred\t\t\t\tla pièce du fond\t\t\t\tun tennis prévisible\n"\
                "les nouilles cuisent\t\t\tdes nouilles, encore?\t\t\t\tla canicule t'emballe\t\t\t\tcesse de chourer la batte\n"\
                "l'habile bête\t\t\ttaisez-vous en bas\t\t\t\tdes piles de boites\t\t\t\tune barrette de shit\n"\
                "le choix dans la date\t\t\tles mites de tes habits\t\t\t\tle gout du blanc\t\t\t\tune fine sans dépôt\n"\
                "tu vis aux champs?\t\t\til déplore la foule\t\t\t\telles doutent de leur foi\t\t\t\tun tennis de pro\n"\
                "compter les points\t\t\tces dames nous dérangent\t\t\t\tta peine te mine"
                
    text_exemple.insert(END, exemple)
    text_exemple.configure(state="disabled")
    

def verif_gg_tab_vis(phrase_orig, phrase_tab_phon, tab_new_phrase):
    """ Lancer la vérification du tableau par gg
        si le nombre de résultats renvoyé est supérieur à TOLERANCE_GG, la phrase est censée exister. """
    
    def renvoie_res_ggg_bloque(tab_new_phrase):
        """ Fabrication du tableau de résultats au cas ou on a été blacklisté par google """
        tab = tab_new_phrase[0:NB_MAX_RES]
        tab_retour = []
        for res in tab:
            tab_retour.append((res[1], res[0], ""))
        return tab_retour
    
    
    global ggg_bloque
    tab_retour = []
    tab_deja_fait = []
    cpt_rech_gg = 0
    cpt_rep_ok = 0
    for new_tup in tab_new_phrase:
        new_phrase = new_tup[0]
        if new_phrase in tab_deja_fait:
            continue
        if ggg_bloque:
            afficher_ligne("Gougueule t'a bloqué. Il faut attendre", couleur="red")
            return renvoie_res_ggg_bloque(tab_new_phrase)
        if ACTIVER_GG and not ggg_bloque:
            if cpt_rep_ok < NB_REPONSE_MAX_GG and cpt_rech_gg < NB_MAX_APPELS_GG:
                cpt_rech_gg += 1
                afficher_ligne_gg(cpt_rech_gg)
                tuple_phrase = gg_est_mon_ami(phrase_orig, phrase_tab_phon, new_phrase)
                if tuple_phrase[3]:
                    ggg_bloque = True
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
                        if tuple_phrase[3]:
                            ggg_bloque = True
                if int(tuple_phrase[0]) > TOLERANCE_GG:
                    cpt_rep_ok += 1
            else:
                break
        else:
            tuple_phrase = (0, new_phrase, "")
        tab_deja_fait.append(new_phrase)
        tab_retour.append(tuple_phrase)
    return tab_retour

def format_nb(nb):
    nb = round(nb, 4)
    return str('{:,}'.format(nb).replace(',', ' '))

def chercher_contrepet(phrase):
    """ Le Coeur de la Bête """
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
    nb_mots_pho = len(phrase_pho_esp.split(" "))
    phrase_tab_phon = get_tab_phonemes(phrase_pho_esp)
    afficher_ligne("Temps".ljust(esp2) + "Action".ljust(esp1))
    
    print(phrase_pho)
    print(phrase_tab_phon)
    
    t1 = time()
    afficher_ligne(format_nb(t1 - t0).ljust(esp2) + "analyse".ljust(esp1))
    
    tab_subst = get_sous_chaines(phrase_pho)
    nb2 = len(tab_subst)
    t2 = time()
    afficher_ligne(format_nb(t2 - t1).ljust(esp2) + (format_nb(nb2)+" sous chaines de substitution trouvées").ljust(esp3) )

    tab_chaines = get_chaines_substituees(phrase_pho, tab_subst)
    nb3 = len(tab_chaines)
    t3 = time()
    afficher_ligne(format_nb(t3 - t2).ljust(esp2) + (format_nb(nb3) + " chaines substituées trouvées").ljust(esp3))     

    tup_toutes_phrases = tab_phrases = get_toutes_phrases(tab_chaines, nb_mots_pho)
    tab_phrases = tup_toutes_phrases[0]
    nb_phrases_possible = tup_toutes_phrases[1]
    nb4 = len(tab_phrases)
    msg = format_nb(nb4) + " phrases phonétiques possibles"
    if nb_phrases_possible != nb4:
        msg = str(nb_phrases_possible) + " phrases phonétiques possibles, c'est trop : on en garde "+ format_nb(nb4)
    t4 = time()
    afficher_ligne(format_nb(t4 - t3).ljust(esp2) + msg.ljust(esp3))
  
    tab_new_tup = get_tup_phrases(tab_phrase_init, tab_phrases)
    if tab_new_tup:
        nb5 = len(tab_new_tup)
        t5 = time()
        afficher_ligne(format_nb(t5 - t4).ljust(esp2) + (format_nb(nb5) + " phrases françaises correspondantes").ljust(esp3))
    else:
        return []

    if nb5 > NB_MAX_PHRASES_FR:
        afficher_ligne("".ljust(esp2) + (format_nb(nb5) + " possibilités, c'est beaucoup : patience...").ljust(esp3), couleur="green")

    tab_new_tup = verif_synt_tab(tab_new_tup)
    if tab_new_tup:
        nb6 = len(tab_new_tup)
        t6 = time()
        afficher_ligne(format_nb(t6 - t5).ljust(esp2) + "Vérification syntaxique: ".ljust(esp1) +
            (format_nb(nb5 - nb6) + " solutions éliminées").ljust(esp4)  + (format_nb(nb6) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_tup = classer_reponses(tab_new_tup, tab_phrase_init)
    if tab_new_tup:
        nb7 = len(tab_new_tup)
        t7 = time()
        afficher_ligne(format_nb(t7 - t6).ljust(esp2) + "Sélection et classement: ".ljust(esp1) +
            (format_nb(nb6 - nb7) + " solutions éliminées").ljust(esp4)  + (format_nb(nb7) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_tup = verif_grammalecte_tab(tab_new_tup)
    if tab_new_tup:
        nb8 = len(tab_new_tup)
        t8 = time()
        afficher_ligne(format_nb(t8 - t7).ljust(esp2) + "Vérification Grammalecte: ".ljust(esp1) +
            (format_nb(nb7 - nb8) + " solutions éliminées").ljust(esp4)  + (format_nb(nb8) + " solutions restantes").ljust(esp4))
    else:
        return []

    tab_new_phrase = verif_gg_tab_vis(phrase, phrase_tab_phon, tab_new_tup)
    tab_new_phrase.sort(reverse=True)
    nb9 = len(tab_new_phrase)
    t9 = time()
    afficher_ligne("\n" + format_nb(t9 - t8).ljust(esp2) + "Vérification gg: ".ljust(esp1) + 
        (format_nb(nb8 - nb9) + " solutions éliminées").ljust(esp4)  + (str(nb9) + " solutions restantes").ljust(esp4))

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
#root.iconbitmap('C:\\Users\\pncef\\Bureau\\contrepet\\contrepet.ico')
root.geometry(str(LARGEUR)+"x"+str(HAUTEUR))
root.title(TITRE)
initialiser_dictionnaires() ####


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
texte_valeur.tag_config("red", background="red")
texte_valeur.tag_config("green", background="green", foreground="white")

label_baratin_fin = Label(root, text=BARATIN_FIN,justify = LEFT)
label_baratin_fin.grid(row=5, column=0, columnspan=5, ipadx =20)

root.bind('<Return>', fct_touche_entree)

root.mainloop()



