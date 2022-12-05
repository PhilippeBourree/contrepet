"""
    CONTREPET est distribué sous les termes de la Licence Publique Générale GNU Version 3 (GNU GPL [General Public License]), CONTREPET est un logiciel libre
    Copyright Philippe Bourrée, pncefbh@gmail.com
"""

import requests
from bs4 import BeautifulSoup
from time import sleep, time
from random import uniform
import re
import math
import grammalecte
import grammalecte.text as txt
import itertools
from dico_mot import *
from dico_phonetik import *
from dico_prio import *
from dico_synt import *




VOYELLES_PHO = ["oi", "a", "â", "e", "é", "è", "ê", "i", "o", "ô", "u", "û", "1", "2", "Y"] # voyelles de la transcription phonétique
MOTS_PHO_APOS = ["S", "d", "j", "l", "m", "n", "k", "t"]
LIMITE = 4              # Nombre de caractères max sur lesquels on fait les substitutions
TOLERANCE_GG = 4        # Nombre de résultats au-dessus duquel on valide la phrase
ACTIVER_GG = True       # Activer la recherche gg, False pour les tests (sinon ralentissement et éventuellement blacklistage)
NB_MAX_APPELS_GG = 4    # Le nombre max d'appels à gg
NB_REPONSE_MAX_GG = 2   # Le nombre de "bonnes" réponses (supérieures à la TOLERANCE_GG)
NB_NIVEAUX_PRIO_MAX = 4 # Le nombre de notes pris en compte à partir de la priorité maximale, si "priorité de la phrase" > "prio max - NB_NIVEAUX_PRIO_MAX on prends la phrase
NB_MAX_PHRASES_PHO = 10000 # Si plus, on jette l'éponge : trop de possibilités
NB_MAX_PHRASES_FR = 2000000 # Si plus, afficher un message pour patienter
NB_MAX_PHRASES = 10000  # Le nombre maximum de phrases à traiter
TEST = True             # Activer l'affichage de données de test
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
URL_GG = "https://www.google.com/search?q="

# initialisation des dictionnaires
# dico_mot = {}       # clé : mot fr,     valeur : phonétique
# dico_phonetik = {}  # clé : phonétique, valeur : mot fr
# dico_synt = {}      # clé : mot fr,     valeur : renseignements syntaxiques
# dico_prio = {}      # clé : mot fr,     valeur : nombre indiquant la priorité, le mot est prioritaire au regard de la théorie contrepétique :
#                            mots grossiers, vulgaires, utilisé dans les contrepèteries ou à double sens... (Ex : bite, macron, enculé, fente...)

gg_bloque = False  # permet de savoir si gg nous à blacklisté


def cle_existe(dico, cle):
    """ Renvoie si la clé "cle" existe dans le dictionnaire "dico"
        (dictionnaire, clé)---> Booléen
    """
    return cle in dico
    
def contient_apos(chaine):
    """ renvoie si la chaine contient une apostrophe """
    if "'" in chaine :
        return True
    return False
    

def get_sous_chaines(chaine, lim=LIMITE):
    """ Renvoie la liste des sous chaines sans doublons de longueur maximale LIMITE d'une chaine """
    return list(set([chaine[idx: idx + N] for  N in range(lim + 1) for idx in range(0, len(chaine) - N + 1) if chaine[idx: idx + N]]))


def get_tab_phonemes(phrase_pho):
    """ Renvoie un tableau des phonèmes de la phrase phonétique
    """
    tab_phonemes = []
    for voyelle in VOYELLES_PHO:                                    # insertion des voyelles
        while voyelle in phrase_pho:
            phrase_pho = phrase_pho.replace(voyelle, " ", 1)
            tab_phonemes.append(voyelle)
    tab_phonemes += [el for el in (phrase_pho.split(" ")) if el]    # insertion des consonnes rentantes

    return sorted(tab_phonemes)


def verif_phonemes(phrase_tab_phon, tup_phrase):
    """ Vérifie que les phonèmes de la phrase de départ se retrouvent dans la phrase française
        retraduite en phonétique
        tup_phrase = (phrase phonétique, phrase fr)
    """
    tab_phrase = get_tab_phrase(tup_phrase[0])
    phrase_pho = get_phrase_pho(tab_phrase, " ")
    if phrase_tab_phon == sorted(get_tab_phonemes(phrase_pho)):
        return True
    return False


def verif_phonemes_tab(phrase_tab_phon, tab_new):
    """ Lance la vérification des phonèmes pour chaque élément d'un tableau
        Renvoie un tableau des éléments vérifiés
    """
    tab_retour = []
    for tup_phrase in tab_new:
        if verif_phonemes(phrase_tab_phon, tup_phrase):
            tab_retour.append(tup_phrase)
    return tab_retour


def get_tag_synt(tab_phrase):
    """
        Renvoie l'analyse lexicale de la phrase
        Pour chaque mot, renvoie le tupple (type, genre, nombre, temps, personne)
            type = nom, verbe, ...
            genre = féminin, masculin, indéterminé
            nombre = singulier, pluriel, indéterminé
            temps = présent, infinitif, futur, ... (pour les verbes)
            personne = 1,2,3 ou indéterminé (pour les verbes, pronoms personnels sujets)
    """

    def get_temps(tab_synt):
        """ Si le verbe est conjugué, renvoie le temps """
        if 'iimp' in tab_synt:
            return 'iimp'
        elif 'simp' in tab_synt:
            return 'simp'
        elif 'cond' in tab_synt:
            return 'cond'
        elif 'ifut' in tab_synt:
            return 'ifut'
        elif 'ipre' in tab_synt:
            return 'ipre'
        elif 'ipsi' in tab_synt:
            return 'ipsi'
        return ''

    def get_pers(tab_synt):
        """ Si le verbe est conjugué, renvoie la personne """
        if '1' in tab_synt[-1] or '2' in tab_synt[-1] or '3' in tab_synt[-1]:
            return tab_synt[-1]
        return ''

    def get_nbr(tab_synt):
        """ Renvoie le nombre (singulier/pluriel) de l'expression """
        if 'pl' in tab_synt:
            return 'pl'
        elif 'sg' in tab_synt:
            return 'sg'
        return ''

    def get_genre(tab_synt):
        """ Renvoie le genre (féminin, masculin) de l'expression """
        if 'mas' in tab_synt:
            return 'mas'
        elif 'fem' in tab_synt:
            return 'fem'
        return ''

    tab_synt_retour = []
    for mot in tab_phrase:
        synt = dico_synt[mot]
        tab_synt = synt.split(" ")
        type_mot = tab_synt[0]
        genre = get_genre(tab_synt)
        nbr = get_nbr(tab_synt)
        tps = ''
        pers = ''
        if type_mot[0] == 'v':
            type_mot = 'verb'
            tps = get_temps(tab_synt)
            pers = get_pers(tab_synt)

            if 'ppas' in tab_synt:
                type_mot = 'adj'
        elif type_mot == 'nom' or type_mot == 'patr' or type_mot == 'patr' or type_mot == 'npr':
            type_mot = 'nom'
        elif type_mot == 'mg':
            type_mot = tab_synt[1]
            if type_mot == 'detpos' or type_mot == 'detdem' or type_mot == 'detind':
                type_mot = 'det'
            if 'propersuj' in tab_synt:
                pers = get_pers(tab_synt)
        tab_synt_retour.append((type_mot, genre, nbr, tps, pers))
    return tab_synt_retour


def verif_synt_tab(tab_new):
    """
        Vérification de chaque phrase grace au dictionnaire syntaxique
        Elimination des solutions pourries ou attribution d'un coef positif/négatif
    """

    def verif_determinants(tab_tag):
        """ Traitement des déterminants
            Si un mot est un déterminant :
                - il doit y avoir un mot après
                - le mot d'après doit s'accorder en genre et en nombre
        """
        tab_type = [tag[0] for tag in tab_tag]
        tab_genre = [tag[1] for tag in tab_tag]
        tab_nbr = [tag[2] for tag in tab_tag]
        nb_mots = len(tab_type)
        for indice in range(nb_mots):
            if tab_type[indice] == 'det':
                if nb_mots <= indice + 1:  # le mot suivant n'existe pas, on élimine
                    return False
                elif tab_genre[indice] and tab_genre[indice + 1] and tab_genre[indice] != tab_genre[
                    indice + 1]:  # le mot suivant n'a pas le même genre, on élimine
                    return False
                elif tab_nbr[indice] and tab_nbr[indice + 1] and tab_nbr[indice] != tab_nbr[
                    indice + 1]:  # le mot suivant n'a pas le même nombre, on élimine
                    return False
                elif tab_type[indice + 1] == 'verb':  # le déterminant est suivi par un verbe, on élimine
                    return False
        return True

    def verif_preposition(tab_type):
        """ Vérification de la préposition
                - il doit y avoir un mot après
                - le mot suivant une préposition doit être soit un déterminant soit un nom (ou assimilé) 
        """
        nb_mots = len(tab_type)
        tab_ok_prep = ['det', 'nom', 'patr', 'prn', 'npr', 'verb']
        for indice in range(nb_mots):
            if tab_type[indice] == 'prep':
                if nb_mots <= indice + 1:  # le mot suivant n'existe pas, on élimine
                    return False
                if tab_type[indice + 1] not in tab_ok_prep:
                    return False
        return True

    def verif_verbes(tab_tag):
        """ Vérification du verbe
            Si un mot est un verbe conjugué :
                - il ne peut pas être suivi par un verbe conjugué à un autre temps
                - il ne peut pas être suivi par un verbe conjugué à une autre personne    
        """
        tab_type = [tag[0] for tag in tab_tag]
        tab_temps = [tag[3] for tag in tab_tag]
        tab_pers = [tag[4] for tag in tab_tag]
        nb_mots = len(tab_type)
        type_avt = ''
        temps_avt = ''
        pers_avt = ''
        for indice in range(nb_mots):
            if tab_type[indice] == 'verb' and type_avt == 'verb':  # le mot suivant un verbe existe et est un verbe
                if tab_temps[indice] and temps_avt and tab_temps[indice] != temps_avt:
                    return False
                if tab_pers[indice] and pers_avt and tab_pers[indice] != pers_avt:
                    return False
            type_avt = tab_type[indice]
            temps_avt = tab_temps[indice]
            pers_avt = tab_pers[indice]
        return True

    def verif_noms(tab_type):
        """ Vérification du nom
            Si un mot est un nom :
                - il ne peut pas être suivi par un nom
        """
        nb_mots = len(tab_type)
        tab_nok_nom = ['patr', 'prn', 'npr']    # pas vraiment des noms : patronymes, prénoms, noms propres
        type_avt = ''
        for indice in range(nb_mots):
            if tab_type[
                indice] == 'nom' and type_avt == 'nom':  # le mot suivant un nom existe et est un nom, on élimine
                return False
            elif (tab_type[indice] == 'nom' and type_avt in tab_nok_nom) or (
                    type_avt in tab_nok_nom and tab_type[indice] == 'nom'):
                return False
            type_avt = tab_type[indice]
        return True

    def verif_pronom_int(tab_phrase, tab_type):
        """ Vérification s'il y a un pronom relatif
            Si un mot est un pronom relatif :
                - il doit y avoir un mot après
                - si le pronom est "qui" il doit être suivi d'un verbe
        """
        nb_mots = len(tab_type)
        for indice in range(nb_mots):
            if tab_type[indice] == 'proint':
                if nb_mots <= indice + 1:           # le mot suivant n'existe pas, on élimine
                    return False
                elif tab_phrase[indice] == 'qui':   # le pronom "qui" doit être suivi par un verbe
                    if tab_type[indice + 1] != 'verb':
                        return False
            # à compléter
        return True

    def genre_compatible(genre1, genre2):
        """ Renvoie si les genres (féminin, masculin) sont compatibles """
        if genre1 and genre2:
            if genre1 != genre2 :
                return False
        return True

    def nb_compatible(nb1, nb2):
        """ Renvoie si les nombres (singulier, pluriel) sont compatibles """
        if nb1 and nb2:
            if nb1 != nb2:
                return False
        return True

    tab_retour = []
    for tup in tab_new:
        tab_phrase = tup[0].replace("'"," ").replace("  "," ").split(" ")
        nb_mots = len(tab_phrase)
        tab_tag = get_tag_synt(tab_phrase)  # (type_mot, genre, nbr, tps, pers)
        tab_type = [tag[0] for tag in tab_tag]
        nb_verb = tab_type.count('verb')
        coef = 0

        if not "nom" in tab_type:  # pas de nom dans la phrase, on élimine
            continue
        if not verif_noms(tab_type):  # deux noms qui se suivent, on élimine
            continue
        if nb_verb >= 2:
            if not verif_verbes(tab_tag):  # deux verbes qui se suivent, on élimine sous condition
                continue
            if tab_type[0] == "verb":
                coef -= 1
        if 'det' in tab_type and not verif_determinants(tab_tag):
            continue  # anomalie déterminant, on élimine
        if 'proint' in tab_type and not verif_pronom_int(tab_phrase, tab_type):
            continue  # anomalie pronom relatif, on élimine
        if 'prep' in tab_type and not verif_preposition(tab_type):
            continue  # anomalie préposition, on élimine
        if tab_type[0] == "verb" and not (tab_tag[0][3] == "ipre" or tab_tag[0][3] == "impe"):
            continue  # la phrase commence par un verbe qui n'est pas au présent ou à l'impératif
            # TODO : vérification forme interrogative
        if tab_type[nb_mots - 1] == "cjco":  # conjonction de coordination en dernier on élimine
            continue
        if nb_verb == 0:
            coef -= 1
        elif nb_verb >= 1:
            index_verb = tab_type.index('verb')
            if index_verb > 0:
                nombre_du_verb = tab_tag[index_verb][2]
                nb_mot_avant = tab_tag[index_verb - 1][2]
                if nombre_du_verb != nb_mot_avant:  # le verbe et le mot devant le verbe n'ont pas le même nombre (sing/plur) : malus
                    coef -= 1
                else:
                    coef += 1
                type_mot_avant = tab_type[index_verb - 1]
                if type_mot_avant == 'nom' and tab_tag[index_verb][4] != '3':  # le mot d'avant est un nom et le verbe
                    coef -= 1  # n'est pas à la 3ième personne : malus
                if type_mot_avant == 'mg' and tab_tag[index_verb - 1][4]:  # le mot d'avant est peut-être un pronom personnel
                    if tab_tag[index_verb][4] != tab_tag[index_verb][4]:  # s'il a une personne, elle doit correspondre à celle du verbe
                        coef -= 1
                    else:
                        coef += 1
            if index_verb < nb_mots - 1:
                type_mot_apres = tab_tag[index_verb + 1][0]  # le verbe est suivi directement par un nom : malus
                if type_mot_apres == 'nom':
                    coef -= 1
        if tab_type.count('det'):
            index_det = tab_type.index('det')  # TODO : boucle pour traiter tous les det?
            type_mot_apres = tab_tag[index_det + 1][0]  # la phrase ayant un déterminant placé en dernier a déjà été éliminée
            if type_mot_apres == 'nom' and genre_compatible(tab_tag[index_det][2],tab_tag[index_det + 1][2]) \
                                       and nb_compatible(tab_tag[index_det][3], tab_tag[index_det + 1][3]):
                coef += 1  # le déterminant est suivi d'un nom genre et nombre compatible  : bonus
        if tab_type.count('prodem'):
            index_prodem = tab_type.index('prodem')  # TODO : boucle pour traiter tous les prodem?
            if index_prodem < nb_mots - 1:
                type_mot_apres = tab_tag[index_prodem + 1][0]
                if type_mot_apres == 'verb':
                    coef += 1
                elif type_mot_apres == 'nom' or type_mot_apres == 'det':
                    coef -= 1
        if tab_type.count('adj'):           # adjectif
            index_adj = tab_type.index('adj')
            if index_adj < nb_mots - 1:
                type_mot_apres = tab_tag[index_adj + 1][0]
                if type_mot_apres == 'nom':     # si le mot suivant est un nom, il doit s'accorder
                    if genre_compatible(tab_tag[index_adj][2],tab_tag[index_adj + 1][2]) and nb_compatible(tab_tag[index_adj][3], tab_tag[index_adj + 1][3]):
                        coef += 1
                    else :
                        coef -= 1
            if index_adj > 1 :
                type_mot_avant = tab_tag[index_adj - 1][0]
                if type_mot_avant == 'det':     # si le mot précédent est est un déterminant, il doit s'accorder
                    if genre_compatible(tab_tag[index_adj][2],tab_tag[index_adj - 1][2]) and nb_compatible(tab_tag[index_adj][3], tab_tag[index_adj - 1][3]):
                        coef += 1
                    else :
                        coef -= 1
            
        new_tup = (coef, tup[0])
        tab_retour.append(new_tup)

    return tab_retour


def verif_grammalecte_tab(tab_new):
    """ Lance la vérification grammalecte https://grammalecte.net/ pour chaque élément d'un tableau
        Renvoie un tableau des éléments vérifiés
    """

    def analyse_retour_grammalecte(retour):
        """ Analyse de la chaine de caractère résultat de l'analyse de grammalecte """
        tab_retour = retour.split("\n")
        if tab_retour[1] == "":  # pas d'erreur
            return tab_retour[0]
        return ""

    def verif_grammalecte(phrase, oGrammarChecker):
        """ Vérification de l'orthographe et de la grammaire par grammalecte https://grammalecte.net/ """
        # oGrammarChecker = grammalecte.GrammarChecker("fr")

        phrase = phrase.replace("'", "’").strip()
        # Apparently, the console transforms «’» in «'».
        # So we reverse it to avoid many useless warnings.

        for sParagraph in txt.getParagraph(phrase):
            sRes, _ = oGrammarChecker.getParagraphWithErrors(sParagraph)
            if sRes:
                return analyse_retour_grammalecte(sRes)
            else:
                return phrase  # No error found

    oGrammarChecker = grammalecte.GrammarChecker("fr")
    tab_retour = []
    for tup in tab_new:
        new_phrase = verif_grammalecte(tup[0], oGrammarChecker)
        if new_phrase:
            tab_retour.append(tup)
    return tab_retour


def classer_reponses(tab_new_phrase, tab_phrase_init):
    """ Classe les phrases en attibuant des points :
        - aux phrases contenant des mots trouvés dans le "dictionnaire prioritaire" (dictionnaire des mots usuels dans les contrepèteries)
        - aux phrases contenant des mots de la phrase initiale
    """
    tab_retour = []
    tab_inter = []
    for tup_phrase in tab_new_phrase:
        phrase = tup_phrase[1]
        prio = tup_phrase[0]
        tab_phrase = phrase.split(" ")
        if len(tab_phrase) == len(tab_phrase_init):     # même nombre de mots  : bonus (discutable)
            prio += 1
        else :
            prio -= math.fabs(len(tab_phrase) - len(tab_phrase_init)) -1
        if sorted(tab_phrase) == sorted(tab_phrase_init):   # la phrase est constituée des mêmes mots: on élimine
            continue
        nb_mots = len(tab_phrase)
        prio_exist = 0
        for i, mot in enumerate(tab_phrase):
            if cle_existe(dico_prio, mot):  # le mot existe dans le dictionnaire prioritaire : bonus
                prio += int(dico_prio[mot][1:])
            if mot in tab_phrase_init:  # le mot existe dans la phrase initiale : bonus
                prio += 1
                if len(tab_phrase_init) > i:
                    if tab_phrase_init[i] == mot:  # et à la même place : bonus!
                        prio_exist += 1
        if prio_exist >= len(tab_phrase_init) - 1:  # trop de priorité tue la priorité!
            prio_exist = 1

        tab_inter.append((phrase, prio + prio_exist))
    tab_inter = sorted(tab_inter, key=lambda bout: bout[1], reverse=True)

    if len(tab_inter) > NB_MAX_PHRASES:     # limitation arbitraire du nombre de résultat renvoyé
        tab_inter = tab_inter[:NB_MAX_PHRASES]

    bonus_max = tab_inter[0][1]  # note maximale attribuée à une des phrases
    max_prio = bonus_max - NB_NIVEAUX_PRIO_MAX      # on ne prends que les meilleures > max_prio

    return [(elem[0], elem[1]) for elem in tab_inter if elem[1] > max_prio]

def comparer_initial(phrase, tab_new_tup):
    """ compare les phonétiques du mot fr du tuple au mot initial, si c'est la même on prends l'original """
    return tab_new_tup
    tab_phrase = phrase.split(" ")
    tab_pho = []
    for mot in tab_phrase:
        mot = mot.replace("'","")
        tab_pho.append(trouver_mot_pho(dico_mot, mot))
    
    taille_init = len(tab_phrase)
    tab_retour = []
    for tup in tab_new_tup:
        phrase_fr = tup[0]
        tab_phrase_fr = phrase_fr.split(" ")
        taille = min(taille_init, len(tab_phrase_fr))
        for indice in range(taille):
            mot_pho = trouver_mot_pho(dico_mot, tab_phrase_fr[indice])
            if mot_pho == tab_pho[indice]:
                phrase_fr = phrase_fr.replace(tab_phrase_fr[indice], tab_phrase[indice])
                tup = (phrase_fr, tup[1])
        tab_retour.append(tup)
    return tab_retour


def verif_suggestion_gg(tab_new_phrase, suggestion):
    """ Si la suggestion gg est déjà parmi nos choix, c'est vraiement la bonne """
    if suggestion[1] in [el[1] for el in tab_new_phrase]:
        return True
    return False


def gg_est_mon_ami(phrase_orig, phrase_tab_phon, phrase):
    """ la phrase trouvée est vérifiée par une recherche sur google """
    global gg_bloque
    if ACTIVER_GG and not gg_bloque:
        sleep(uniform(1, 2))        # on laisse un temps entre deux appels sinon google y bloque...
        url = URL_GG + '"' + phrase + '"'
        result = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(result.content, 'html.parser')
        total_results_text = "0"
        if soup.find("div", {"id": "result-stats"}):
            total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True,
                                                                               recursive=False)  # this will give you the outer text which is like 'About 1,410,000,000 results'
        else:
            gg_bloque = True
        nb_res = int(''.join([num for num in total_results_text if
                              num.isdigit()]))  # now will clean it up and remove all the characters that are not a number .
        # traitement de la suggestion gg, si gg suggère, on prends.
        suggestion_gg = ""
        if soup.find_all("span", string="Essayez avec cette orthographe :"):
            suggestion_gg = eval(
                soup.find("span", string="Essayez avec cette orthographe :").find_next_sibling().get_text())
        elif soup.find_all("span", string="Résultats pour"):
            suggestion_gg = eval(soup.find("span", string="Résultats pour").find_next_sibling().get_text())
        if suggestion_gg and suggestion_gg != phrase_orig and verif_phonemes(phrase_tab_phon, (
        suggestion_gg, "")):  # on vérifie que tous les phonèmes sont là dans la suggestion:
            if nb_res != 0:
                return 666, suggestion_gg, "mg"
            else:
                return 1, suggestion_gg, "mg"
        return (nb_res, phrase, "")
    else:  # pour tests, évite les lenteurs et le blacklistage ou si gg_bloque
        print("ACTIVER_GG",ACTIVER_GG,"gg_bloque",gg_bloque)
        return (0, phrase, "")


def verif_gg_tab(phrase_orig, phrase_tab_phon, tab_new_phrase):
    """ Lancer la vérification du tableau par gg
        si le nombre de résultats renvoyé est supérieur à TOLERANCE_GG, la phrase est supposée exister.
        Limitation du nombre et de la fréquence des recherches : gg is watching you...
    """
    tab_retour = []
    tab_deja_fait = []
    cpt_rech_gg = 0
    cpt_rep_ok = 0
    for new_tup in tab_new_phrase:
        new_phrase = new_tup[0]
        if new_phrase in tab_deja_fait:
            continue
        if ACTIVER_GG and not gg_bloque:
            if cpt_rep_ok < NB_REPONSE_MAX_GG and cpt_rech_gg < NB_MAX_APPELS_GG:
                print(cpt_rech_gg + 1, "appel ggg")
                tuple_phrase = gg_est_mon_ami(phrase_orig, phrase_tab_phon, new_phrase)
                if tuple_phrase[2]:  # gg a fait une suggestion
                    suggestion_existe = verif_suggestion_gg(tab_new_phrase, tuple_phrase)
                    if tuple_phrase[0] == 666 and suggestion_existe:
                        return [tuple_phrase]  # c'est la bonne ! on renvoie

                    if not suggestion_existe and tuple_phrase[
                        1]:  # la phrase est une suggestion gg n'existant pas encore dans la liste
                        # tab_retour.append(tuple_phrase)                             # on stocke le résultats
                        tab_deja_fait.append(tuple_phrase[1])
                        print(cpt_rech_gg + 1, "appel ggg")
                        cpt_rech_gg += 1
                        tuple_phrase = gg_est_mon_ami(phrase_orig, phrase_tab_phon, tuple_phrase[1])  # on relance la recherche avec la suggestion
                if int(tuple_phrase[0]) > TOLERANCE_GG:
                    cpt_rep_ok += 1
                cpt_rech_gg += 1
            else:
                break
        else:
            tuple_phrase = (0, new_phrase, "")
        tab_deja_fait.append(new_phrase)
        tab_retour.append(tuple_phrase)
    return tab_retour


def get_tab_phrase(phrase):
    """ Renvoie un tableau des mots de la phrase fr """
    phrase = phrase.replace("'", " ")
    return phrase.split(" ")


def trouver_mot_pho(dico_mot, mot):
    """ Renvoie le mot phonétique correspondant à un mot fr. 
        Renvoie le mot fr original si aucun mot trouvé """
    if mot in dico_mot.keys():
        return dico_mot[mot]
    return mot


def get_phrase_pho(tab_phrase, sep=""):
    """ Renvoie la phrase en phonétique. Les mots sont séparés par "sep", par défaut concaténés """
    tab_pho = []
    for mot in tab_phrase:
        tab_pho.append(trouver_mot_pho(dico_mot, mot))
    return sep.join(tab_pho)


def get_chaines_substituees(chaine, tab_subst):
    """ Renvoie un tableau des chaines phonétiques après substitution"""

    def chaines_includes(chaine, sous):
        """ Renvoie True si toutes les lettres de "sous" sont présentes dans "chaine" """
        for car in sous:
            if car not in chaine:
                return False
        return True

    def verif_subst(subst_1, subst_2):
        """ Vérifie que les chaines de substitution sont compatibles. Cas foireux :
                - les chaines sont les mêmes
                - les chaines sont incluses l'une dans l'autre
        """
        return subst_1 != subst_2 and not chaines_includes(subst_2, subst_1) and not chaines_includes(subst_1, subst_2)

    def intervertir_dans_chaine(chaine, subst_1, subst_2):
        """ Inverse deux sous chaines (subst_1 et subst_2) présentes dans une chaine """
        if chaine.find(subst_1) > chaine.find(subst_2):
            chaine = chaine.replace(subst_1, subst_2, 1)
            chaine = chaine.replace(subst_2, subst_1, 1)
        else:
            chaine = chaine.replace(subst_2, subst_1, 1)
            chaine = chaine.replace(subst_1, subst_2, 1)
        return chaine

    tab_retour = []
    for index_subst_1 in range(len(tab_subst)):
        subst_1 = tab_subst[index_subst_1]
        for index_subst_2 in range(index_subst_1, len(tab_subst)):
            subst_2 = tab_subst[index_subst_2]
            if verif_subst(subst_1, subst_2):
                chaine_res = intervertir_dans_chaine(chaine, subst_1, subst_2)

                if chaine_res != chaine:
                    tab_retour.append(chaine_res)
    tab_retour = list(set(tab_retour))  # suppression des doublons
    return tab_retour


def get_toutes_phrases(tab_chaines):
    """ Renvoie un tableau de toutes les phrases phonétiques possibles d'un tableau de chaines """

    def commence_voyelle(mot):
        """ Renvoie si un mot phonétique commence par une voyelle """
        if not mot:
            return False
        return mot[0] in VOYELLES_PHO

    def verif_phrases(phrase):
        """ Éliminer un max de phrases incorrectes
            # Le dernier mot ne doit pas avoir d'apostrophe
            # Le mot suivant un mot à apostrophe doit commencer par une voyelle
        """
        tab_phrase = phrase.strip().split(" ")
        indexes = [ind for ind, el in enumerate(tab_phrase) if el in MOTS_PHO_APOS]
        if indexes:
            if indexes[-1] == len(tab_phrase) - 1:
                return False
            for ind in indexes:
                mot_suivant = tab_phrase[ind + 1]
                if not commence_voyelle(mot_suivant):
                    return False           
        return True

    def chercher_phrases(chaine):
        """ Renvoie un tableau de toutes les phrases phonétiques possibles d'une chaine """
        tabs = []
        stack = []
        stack.append((chaine[:], ''))
        while stack:
            array, st_res = stack.pop()
            for indice in range(len(array)):
                deb = array[0:indice + 1]
                if cle_existe(dico_phonetik, deb):
                    my_res = st_res + deb + " "
                    reste_chaine = array[indice + 1:]
                    if reste_chaine:
                        stack.append((reste_chaine[:], my_res))
                    else:
                        if verif_phrases(my_res):
                            tabs.append(my_res.strip())
        return tabs

    tab_mots = []
    for chaine_res in tab_chaines:
        tab_res = chercher_phrases(chaine_res)
        tab_mots = tab_mots + tab_res
    tab_mots = list(set(tab_mots))  # suppression des doublons
    return tab_mots


def verif_phonemes_pho(tab_phrases, phrase_tab_phon_esp):
    """ Vérifie que tous les phonèmes de la phrase phonétique de départ
        se retrouvent dans la phrase phonétique transformée """
    tab_retour = []

    for phrase_pho in tab_phrases:
        tab_pho = get_tab_phonemes(phrase_pho)
        if phrase_tab_phon_esp == tab_pho:
            tab_retour.append(phrase_pho)
    return tab_retour


def get_tup_phrases(tab_phrase_init, tab_phrases):
    """ Renvoie un tableau de tupples (phrase_pho, phrase_fr) """
    
    def possible_apos(mot_pho):
        """ Le premier caractère du mot peut-il être suivi d'une apostrophe? """
        if mot_pho[0] in MOTS_PHO_APOS:
            return True
        return False

    def get_mots_possibles(dico_phonetik, mot_pho):
        """ Renvoie une sélection des mots fr correspondants à un mot phonétique """
        tab_mot_pho = []
        if cle_existe(dico_phonetik, mot_pho):
            tab_mot_pho += dico_phonetik[mot_pho]

        if possible_apos(mot_pho) and not contient_apos(mot_pho):          # si le premier caractère est possiblement suivi d'un apostrophe, on regarde si la suite existe
            char = mot_pho[0]
            suite = mot_pho[1:]
            if cle_existe(dico_phonetik, suite):
                tab_suite = dico_phonetik[suite]
                if tab_suite:
                    tab_w = []
                    tab_w.append(dico_phonetik[char])
                    tab_w.append(tab_suite)
                    liste_w = list(map("'".join, (list(itertools.product(*tab_w)))))
                    tab_mot_pho += [elt for elt in liste_w if "''" not in elt]
        return tab_mot_pho
        
    def get_mots_fr(dico_phonetik, mot_pho, tab_phrase_init):
        """ Si un des mots trouvé existe dans la phrase d'origine,
            on le prend. C'est un mot qui n'a pas été modifié
            Pas la peine de prendre en compte toutes les homophonies """
        tab_mots_fr = get_mots_possibles(dico_phonetik, mot_pho)
        for mot_init in tab_phrase_init:
            if mot_init in tab_mots_fr:
                return [mot_init]
        return tab_mots_fr

    def get_tupple_phrase(phrase_pho, tab_res_fr):
        """ Renvoie un tableau de tous les tupple possibles (phrase_pho, phrase_fr) """
        tab_retour = []
        map_list = map(' '.join, (list(itertools.product(*tab_res_fr))))

        for phrase_fr in map_list:
            phrase_fr = phrase_fr.replace("' ","'") 
            tab_retour.append((phrase_fr, phrase_pho))
        return tab_retour

    tab_tupple_retour = []
    for phrase_pho in tab_phrases:
        tab_pho = phrase_pho.split(" ")
        tab_res_fr = []
        for mot_pho in tab_pho:
            tab_mots_fr = get_mots_fr(dico_phonetik, mot_pho, tab_phrase_init)
            tab_res_fr.append(tab_mots_fr)

        tab_tupple_retour += get_tupple_phrase(phrase_pho, tab_res_fr)
    tab_tupple_retour = list(set(tab_tupple_retour))  # suppression des doublons
    return tab_tupple_retour


def get_new_phrases(phrase):                #### virer en graphique
    """ Le coeur de la bête """
    esp1 = 32
    esp2 = 9
    esp3 = 20
    esp4 = 5
    esp5 = 20
    esp6 = 5

    if TEST:
        t0 = time()
    # analyse & transformation de la phrase
    
    apos = contient_apos(phrase)
    tab_phrase_init = get_tab_phrase(phrase)
    phrase_pho = get_phrase_pho(tab_phrase_init)
    phrase_pho_esp = get_phrase_pho(tab_phrase_init, " ")
    phrase_tab_phon = get_tab_phonemes(phrase_pho_esp)

    print("phrase_tab_phon>>>", phrase_tab_phon)

    if TEST:
        t1 = time()
        print("temps analyse de la phrase: ".rjust(esp1), str(round(t1 - t0)).ljust(esp2), "\n")

    tab_subst = get_sous_chaines(phrase_pho)
    if TEST:
        nb2 = len(tab_subst)
        t2 = time()
        print("temps get_sous_chaines: ".rjust(esp1), str(round(t2 - t1, 4)).ljust(esp2),
              "Nombres de sous chaines de substitution: ".rjust(esp3), str(nb2).ljust(esp4), "\n")

    tab_chaines = get_chaines_substituees(phrase_pho, tab_subst)
    if TEST:
        nb3 = len(tab_chaines)
        t3 = time()
        print("temps get_chaines_substituees: ".rjust(esp1), str(round(t3 - t2, 4)).ljust(esp2),
              "Nombres de chaines substituées: ".rjust(esp3), str(nb3).ljust(esp4), "\n")

    tab_phrases = get_toutes_phrases(tab_chaines)
    if TEST:
        nb4 = len(tab_phrases)
        t4 = time()
        print("temps get_toutes_phrases: ".rjust(esp1), str(round(t4 - t3, 4)).ljust(esp2),
              "Nombres de phrases phonétiques: ".rjust(esp3), str(nb4).ljust(esp4), "\n")

    tab_phrases = verif_phonemes_pho(tab_phrases, phrase_tab_phon)
    if TEST:
        nb5 = len(tab_phrases)
        t5 = time()
        print("temps verif_phonemes_pho: ".rjust(esp1), str(round(t5 - t4, 4)).ljust(esp2),
              "Nombres de phrases phonétiques: ".rjust(esp3), str(nb5).ljust(esp4), "\n")

    tab_new_tup = get_tup_phrases(tab_phrase_init, tab_phrases)
    if TEST:
        nb6 = len(tab_new_tup)
        t6 = time()
        print("temps get_tup_phrases: ".rjust(esp1), str(round(t6 - t5, 4)).ljust(esp2),
              "Nombre de phrases françaises correspondantes: ".rjust(esp3), str(nb6).ljust(esp4), "\n")

    tab_new_tup = verif_phonemes_tab(phrase_tab_phon, tab_new_tup)
    if TEST:
        nb7 = len(tab_new_tup)
        t7 = time()
        print("temps verif_phonemes_tab: ".rjust(esp1), str(round(t7 - t6, 4)).ljust(esp2),
              "Solutions éliminées: ".rjust(esp5), str(nb6 - nb7).ljust(esp6), "Solutions restantes: ".rjust(esp5),
              str(nb7).ljust(esp6), "\n")

    tab_new_tup = verif_synt_tab(tab_new_tup)
    if TEST:
        nb8 = len(tab_new_tup)
        t8 = time()
        print("temps verif_synt_tab: ".rjust(esp1), str(round(t8 - t7, 4)).ljust(esp2),
              "Solutions éliminées: ".rjust(esp5), str(nb7 - nb8).ljust(esp6), "Solutions restantes: ".rjust(esp5),
              str(nb8).ljust(esp6), "\n")

    tab_new_tup = classer_reponses(tab_new_tup, tab_phrase_init)
    if TEST:
        nb9 = len(tab_new_tup)
        t9 = time()
        print("temps classer_reponses: ".rjust(esp1), str(round(t9 - t8, 4)).ljust(esp2),
              "Solutions éliminées: ".rjust(esp5), str(nb8 - nb9).ljust(esp6), "Solutions restantes: ".rjust(esp5),
              str(nb9).ljust(esp6), "\n")

    # print(tab_new_tup)

    tab_new_tup = verif_grammalecte_tab(tab_new_tup)
    if TEST:
        nb10 = len(tab_new_tup)
        t10 = time()
        print("temps verif_grammalecte_tab: ".rjust(esp1), str(round(t10 - t9, 4)).ljust(esp2),
              "Solutions éliminées: ".rjust(esp5), str(nb9 - nb10).ljust(esp6), "Solutions restantes: ".rjust(esp5),
              str(nb10).ljust(esp6), "\n")

    print(tab_new_tup)

    tab_new_phrase = verif_gg_tab(phrase, phrase_tab_phon, tab_new_tup)
    tab_new_phrase.sort(reverse=True)
    if TEST:
        nb11 = len(tab_new_phrase)
        t11 = time()
        print("temps verif_gg_tab: ".rjust(esp1), str(round(t11 - t10, 4)).ljust(esp2),
              "Solutions éliminées : ".rjust(esp5), str(nb10 - nb11).ljust(esp6), "Solutions restantes : ".rjust(esp5),
              str(nb11).ljust(esp6), "\n")

    # print(tab_new_phrase)

    return tab_new_phrase


def afficher_resultats(phrase, tab_new_phrases):               #### virer en graphique
    """ Affichage """
    res_imprimes = []
    print("\n******Solutions pour ",phrase)
    nb = 1
    print("num".ljust(8), "nb réponses".ljust(20), "réponses possibles".ljust(150))
    for nouvelle_phrase in tab_new_phrases:
        if nouvelle_phrase[1] not in res_imprimes:
            print(str(nb).ljust(8), str(nouvelle_phrase[0]).ljust(20), nouvelle_phrase[1].ljust(25),
                  nouvelle_phrase[2].ljust(3))
            nb += 1
            res_imprimes.append(nouvelle_phrase[1])
    if not tab_new_phrases:
        print("Enfer et dalmatien! Je n'ai rien trouvé!")


def traiter_saisie(phrase):
    """ Modifie la phrase de saisie :
        Minuscule et enlève la ponctuation
    """
    phrase = phrase.lower().strip().replace("’", "'").replace("-", " ")
    return re.sub(r'[.,"?:!;]', '', phrase)


def demander_texte():                      #### virer en graphique
    """ Saisie de la phrase """
    # Exemples proposés à la foule en liesse
    esp = 30
    print("La poule qui mue".ljust(esp), "glisser dans la piscine".ljust(esp), "Un champ de coton".ljust(esp))
    print("panne de micro".ljust(esp), "Laisser le pain chaud".ljust(esp), "Le bras sur la chaise".ljust(esp))
    print("boire ça vite".ljust(esp), "La cure du foie".ljust(esp), "Quelle bouille".ljust(esp))
    print("Vite et bien".ljust(esp), "Laissez nos péniches".ljust(esp), "La berge précède le vide".ljust(esp))
    print("ça pue dans le car".ljust(esp), "Le linge à sécher".ljust(esp), "Ton entrain gène".ljust(esp))
    print("à pied par la Chine".ljust(esp), "Retire ta lampe que je guette".ljust(esp), "un tennis prévisible".ljust(esp))
    print("brouiller l'écoute".ljust(esp), "la fine ou l'épaisse".ljust(esp), "J'ai du tracas jusqu'au cou".ljust(esp))

    print("")

    # saisie de la phrase :
    return traiter_saisie(input("Entrez la phrase : "))


def lancer_le_bousin():                                #### virer en graphique
    """ Programme principal """
    initialiser_dictionnaires()

    phrase = demander_texte()
    tA = time()
    tab_new_phrases = get_new_phrases(phrase)
    afficher_resultats(phrase, tab_new_phrases)
    tB = time()
    print("\nTemps de réponse : ", str(round(tB - tA, 4)), "secondes")

def lancer_le_test():                             #### virer en graphique
    TEST = False
    ctps = [ "La poule qui mue"
            ,"glisser dans la piscine"
            ,"Un champ de coton"
            ,"panne de micro"
            ,"Laisser le pain chaud"
            ,"Le bras sur la chaise"
            ,"boire ça vite"
            ,"La cure du foie"
            ,"Quelle bouille"
            ,"Vite et bien"
            ,"Laissez nos péniches"
            ,"La berge précède le vide"
            ,"ça pue dans le car"
            ,"Le linge à sécher"
            ,"Ton entrain gène"
            ,"à pied par la Chine"
            ,"Retire ta lampe que je guette"
            ,"un tennis prévisible"
            ,"brouiller l'écoute"
            ,"la fine ou l'épaisse"
            ,"J'ai du tracas jusqu'au cou"
            ,"Votre père a l'air mutin"
        ]
    for phrase in ctps:
        tab_new_phrases = get_new_phrases(phrase)
        afficher_resultats(phrase, tab_new_phrases)


# TODO :
# TODO : Liaisons : traiter les doubles consonnes (un-navet)
# TODO : Apostrophe : ça plante!
# TODO : Réalisation .exe
# TODO : Modifier la vérification phonétique : séparer la phrase pho par voyelles 
#           de façon à pouvoir identifier les consonnes doublées correspondant à un phonème "bl" "tr" : ???? fait foirer certaines...
#           (faire de même après transfo : - sur pho - sur fr (?) 
# TODO ? virer les mots à tirets du dictionnaire?

"""
La poule qui mue                        1   ok      5.8487 secondes
glisser dans la piscine             1       nok     111.782 secondes
Un champ de coton                   1       nok     7.3826 secondes
panne de micro                          1   ok      5.2629 secondes
Laisser le pain chaud               1       nok     20.0871 secondes
Le bras sur la chaise                 1     ~nok    7.6783 secondes
boire ça vite                       1       nok     8.4563 secondes
La cure du foie                         1   ok      6.1198 secondes
Quelle bouille                        1     ~nok    7.5733 secondes
Vite et bien                            1   ok      5.5751 secondes
Laissez nos péniches                    1   ok      6.03 secondes
La berge précède le vide                1   ok      13.6383 secondes
ça pue dans le car                      1   ok      8.7929 secondes
Le linge à sécher                   1       nok     10.6175 secondes
Ton entrain gène                        1   ok     8.3526 secondes
à pied par la Chine                     1   ok      10.1754 secondes
Retire ta lampe que je guette           1   ok      8.443 secondes
un tennis prévisible                1       nok     9.8443 secondes         impossible : phonème p et tr <--> pr et t 
brouiller l'écoute                      1   ok      9.191 secondes
la fine ou l'épaisse                    1   ok      12.3474 secondes
J'ai du tracas jusqu'au cou         1       nok     8.5641 secondes
folle de la messe                       1   ok      8.0385 secondes
                                    8 2 11
"""


# lancer_le_bousin()
# lancer_le_test()
# initialiser_dictionnaires()
# make_dicos_files()