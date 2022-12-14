"""
    CONTREPET est distribué sous les termes de la Licence Publique Générale GNU Version 3 (GNU GPL [General Public License]), CONTREPET est un logiciel libre
    Copyright Philippe Bourrée, pncefbh@gmail.com
"""

from requests import get
from bs4 import BeautifulSoup
from time import sleep, time
from random import uniform
from re import sub, finditer
from math import fabs
import grammalecte
import grammalecte.text as txt
from itertools import product
from dico_mot import *
from dico_phonetik import *
from dico_prio import *
from dico_synt import *
from dico_prio_pho import *


# toutes les terminaisons phonétiques de 2 lettres existantes dans le dictionnaire
TERMINAISONS = ['1K', '1S', '1a', '1b', '1d', '1f', '1g', '1j', '1k', '1m', '1p', '1r', '1t', '1z', '1ç', '2S', '2Y', '2b', '2d', '2f'    \
                , '2j', '2k', '2l', '2m', '2n', '2r', '2s', '2t', '2v', '2w', '2z', '2é', 'AC', 'DN', 'JO', 'K1', 'K2', 'Ka', 'Ke', 'Ki'  \
                , 'Kl', 'Km', 'Kn', 'Ko', 'Kr', 'Ks', 'Kt', 'Ku', 'Kâ', 'Ké', 'Kô', 'Kö', 'Kû', 'NA', 'ON', 'PY', 'S1', 'S2', 'SY', 'Sa'  \
                , 'Sb', 'Se', 'Si', 'So', 'Sr', 'St', 'Su', 'Sv', 'Sâ', 'Sé', 'Sô', 'Sö', 'Sû', 'Y1', 'Y2', 'YK', 'YS', 'Ya', 'Yg', 'Yi'  \
                , 'Yk', 'Yn', 'Yo', 'Yt', 'Yu', 'Yâ', 'Yé', 'Yô', 'Yû', 'a1', 'aK', 'aS', 'aY', 'ab', 'ad', 'af', 'ag', 'ai', 'aj', 'ak'  \
                , 'al', 'am', 'an', 'ao', 'ap', 'ar', 'as', 'at', 'au', 'av', 'aw', 'az', 'aâ', 'aç', 'aé', 'aö', 'aû', 'b1', 'b2', 'bY'  \
                , 'ba', 'bd', 'be', 'bi', 'bk', 'bl', 'bn', 'bo', 'br', 'bs', 'bu', 'bw', 'bz', 'bâ', 'bé', 'bô', 'bö', 'bû', 'd1', 'd2'  \
                , 'dY', 'da', 'db', 'de', 'df', 'dg', 'di', 'dl', 'dm', 'dn', 'do', 'dr', 'ds', 'dt', 'du', 'dz', 'dâ', 'dé', 'dí', 'dô'  \
                , 'dö', 'dû', 'e1', 'eK', 'eS', 'ea', 'eb', 'ed', 'ef', 'eg', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'er', 'es'  \
                , 'et', 'eu', 'ev', 'ew', 'ez', 'eâ', 'eç', 'eé', 'f1', 'f2', 'fY', 'fa', 'fe', 'fi', 'fl', 'fm', 'fo', 'fr', 'fs', 'ft'  \
                , 'fu', 'fâ', 'fé', 'fô', 'fö', 'fû', 'g1', 'g2', 'ga', 'gd', 'gi', 'gj', 'gl', 'gm', 'gn', 'go', 'gr', 'gs', 'gt', 'gu'  \
                , 'gw', 'gâ', 'gé', 'gô', 'gö', 'gû', 'i1', 'i2', 'iK', 'iS', 'ia', 'ib', 'id', 'ie', 'if', 'ig', 'ij', 'ik', 'il', 'im'  \
                , 'in', 'io', 'ip', 'ir', 'is', 'it', 'iu', 'iv', 'iz', 'iâ', 'iç', 'ié', 'iô', 'iö', 'iû', 'j1', 'j2', 'jY', 'ja', 'je'  \
                , 'ji', 'jk', 'jo', 'js', 'ju', 'jâ', 'jé', 'jô', 'jö', 'jû', 'k1', 'k2', 'kS', 'kY', 'ka', 'kb', 'kd', 'ke', 'kg', 'ki'  \
                , 'kl', 'kn', 'ko', 'kr', 'ks', 'kt', 'ku', 'kz', 'kâ', 'ké', 'kô', 'kö', 'kû', 'l1', 'l2', 'lK', 'lS', 'la', 'lb', 'ld'  \
                , 'le', 'lf', 'lg', 'li', 'lj', 'lk', 'lm', 'ln', 'lo', 'lp', 'ls', 'lt', 'lu', 'lv', 'lz', 'lâ', 'lç', 'lé', 'lí', 'ló'  \
                , 'lô', 'lö', 'lû', 'm1', 'm2', 'mY', 'ma', 'mb', 'me', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mp', 'mr', 'ms', 'mt', 'mu'  \
                , 'má', 'mâ', 'mé', 'mô', 'mö', 'mû', 'n1', 'n2', 'nK', 'nY', 'na', 'nb', 'ne', 'ng', 'ni', 'nk', 'no', 'np', 'ns', 'nu'  \
                , 'nâ', 'né', 'nô', 'nö', 'nû', 'o1', 'oK', 'oS', 'oY', 'oa', 'ob', 'od', 'of', 'og', 'oi', 'oj', 'ok', 'ol', 'om', 'on'  \
                , 'op', 'or', 'os', 'ot', 'ou', 'ov', 'ow', 'oz', 'oâ', 'oç', 'oé', 'oô', 'p1', 'p2', 'pS', 'pY', 'pa', 'pf', 'pg', 'pi'  \
                , 'pj', 'pk', 'pl', 'po', 'pr', 'ps', 'pt', 'pu', 'pz', 'pâ', 'pé', 'pô', 'pö', 'pû', 'r1', 'r2', 'rK', 'rS', 'rY', 'ra'  \
                , 'rb', 'rd', 're', 'rf', 'rg', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro', 'rp', 'rs', 'rt', 'ru', 'rv', 'rz', 'râ', 'rç'  \
                , 'ré', 'ró', 'rô', 'rö', 'rú', 'rû', 's1', 's2', 'sK', 'sY', 'sa', 'sd', 'se', 'sg', 'si', 'sj', 'sk', 'sl', 'sm', 'sn'  \
                , 'so', 'sp', 'sr', 'st', 'su', 'sz', 'sâ', 'sç', 'sé', 'sô', 'sö', 'sû', 't1', 't2', 'tK', 'tY', 'ta', 'te', 'tg', 'ti'  \
                , 'tj', 'tk', 'tl', 'tm', 'to', 'tp', 'tr', 'ts', 'tt', 'tu', 'tw', 'tz', 'tá', 'tâ', 'tç', 'té', 'tô', 'tö', 'tû', 'u1'  \
                , 'u2', 'uK', 'uS', 'uY', 'ua', 'ub', 'ud', 'uf', 'ug', 'ui', 'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up', 'ur', 'us', 'ut'  \
                , 'uv', 'uw', 'uz', 'uâ', 'uç', 'ué', 'uô', 'uö', 'v1', 'v2', 'vY', 'va', 've', 'vg', 'vi', 'vn', 'vo', 'vr', 'vu', 'vâ'  \
                , 'vé', 'vô', 'vö', 'vû', 'w1', 'wa', 'wb', 'wi', 'wk', 'wl', 'wn', 'ws', 'wu', 'wâ', 'wé', 'wô', 'z1', 'z2', 'zY', 'za'  \
                , 'zg', 'zi', 'zl', 'zm', 'zo', 'zs', 'zt', 'zu', 'zâ', 'zé', 'zô', 'zö', 'zû', 'ák', 'án', 'âK', 'âS', 'âa', 'âb', 'âd'  \
                , 'âg', 'âj', 'âk', 'âl', 'âp', 'âr', 'âs', 'ât', 'âv', 'âz', 'âç', 'ão', 'é1', 'é2', 'éK', 'éS', 'éY', 'éa', 'éb', 'éd'  \
                , 'ée', 'éf', 'ég', 'éi', 'éj', 'ék', 'él', 'ém', 'én', 'éo', 'ép', 'ér', 'és', 'ét', 'év', 'éz', 'éâ', 'éç', 'éé', 'éô'  \
                , 'ík', 'ín', 'ók', 'ón', 'ôK', 'ôS', 'ôb', 'ôd', 'ôf', 'ôg', 'ôj', 'ôk', 'ôp', 'ôr', 'ôs', 'ôt', 'ôz', 'öS', 'öa', 'öb'  \
                , 'öd', 'öf', 'öi', 'ök', 'öl', 'öm', 'ön', 'öo', 'ör', 'öt', 'öv', 'öz', 'ún', 'û1', 'û2', 'ûK', 'ûS', 'ûY', 'ûa', 'ûb'  \
                , 'ûd', 'ûf', 'ûg', 'ûi', 'ûj', 'ûk', 'ûl', 'ûm', 'ûn', 'ûp', 'ûr', 'ûs', 'ût', 'ûv', 'ûz', 'ûâ', 'ûç', 'ûé', 'ûô', 'ći', 'ćâ']

# Liste des mots phonétiques impossibles à la fin d'une phrase
MOTS_IMPOSSIBLE_FIN = [" ô", " a", " ki", " ke", " ne",  " me", " le"]

VOYELLES_PHO = ["a", "â", "e", "é", "è", "i", "o", "ô", "ö", "u", "û", "1", "2", "Y"]  # voyelles de la transcription phonétique
VOYELLES_PHO_SUBS = ["a", "â", "e", "é", "è", "i", "o", "ô", "ö", "u", "û", "1", "2"]  # voyelles phonétiques substituables
CONSONNES_PHO_SUBS = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q" \
                    , "r", "s", "t", "v", "w", "x", "z", "S", "K", "br", "cr", "dr", "fr" \
                    , "gr", "kr", "pr", "tr", "vr", "bl", "cl", "fl", "gl", "kl", "pl"]        # consonnes phonétiques non substituable avec une voyelle substituable
MOTS_PHO_APOS = ["S", "d", "j", "l", "m", "n", "k", "t"]
MOTS_PHO_FR = ["s", "c", "d", "j", "l", "m", "n", "qu", "t"]
DIFF_NB_MOTS = 2        # Nombre de mots maximum tolérés entre la phrase d'origine et la phrase résultat 
LIMITE = 4              # Nombre de caractères max sur lesquels on fait les substitutions
TOLERANCE_GG = 4        # Nombre de résultats au-dessus duquel on valide la phrase
ACTIVER_GG = True       # Activer la recherche gg, False pour les tests (sinon ralentissement et éventuellement blacklistage)
NB_MAX_APPELS_GG = 4    # Le nombre max d'appels à gg
NB_REPONSE_MAX_GG = 3   # Le nombre de "bonnes" réponses (supérieures à la TOLERANCE_GG)
NB_NIVEAUX_PRIO_MAX = 4 # Le nombre de notes pris en compte à partir de la priorité maximale, si "priorité de la phrase" > "prio max - NB_NIVEAUX_PRIO_MAX on prends la phrase
NB_MAX_PHRASES_PHO = 1000 # Si plus, on jette l'éponge : trop de possibilités
NB_MAX_PHRASES_FR = 1000000 # Si plus, afficher un message pour patienter
NB_MAX_PHRASES = 10000  # Le nombre maximum de phrases à traiter
TEST = True             # Activer l'affichage de données de test
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
URL_GG = "https://www.google.com/search?q="

MOTS_INCONNUS_GRA = ['désaler','imbroyable', 'glander']    # mot n'exisant pas dans le vérificateur grammalecte (échec de "verif_grammalecte_tab")

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
    """ renvoie un tableau des phonèmes de la phrase phonétique
    """
    tab_phonemes = []  
    for voyelle in VOYELLES_PHO:
        while voyelle in phrase_pho:
            phrase_pho = phrase_pho.replace(voyelle,"",1)
            tab_phonemes.append(voyelle)
    for car in phrase_pho:
        if car.strip():
            tab_phonemes.append(car)
    return sorted(tab_phonemes)
    

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
        elif 'infi' in tab_synt:
            return 'infi'
        elif 'ppas' in tab_synt:
            return 'ppas'
        elif 'ppre' in tab_synt:
            return 'ppre'
        return ''

    def get_pers(tab_synt):
        """ Si le verbe est conjugué, renvoie la personne """
        tab_pers = ["1sg", "2sg", "3sg", "1pl", "2pl", "3pl", "1pe", "2pe", "3pe"]
        res = [elt for elt in tab_synt if elt in tab_pers]  # intersection
        if res :
            return res[0]
        return ""

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
            str_pers = get_pers(tab_synt)
            if str_pers:
                pers = str_pers[0]
                nbr = str(str_pers[1:])
        elif type_mot == 'nom' or type_mot == 'patr' or type_mot == 'patr' or type_mot == 'npr':
            type_mot = 'nom'
        elif type_mot == 'mg':
            type_mot = tab_synt[1]
            if type_mot == 'detpos' or type_mot == 'detdem' or type_mot == 'detind':
                type_mot = 'det'
            if 'propersuj' in tab_synt:
                type_mot = 'propersuj'
                str_pers = get_pers(tab_synt)
                if str_pers:
                    pers = str_pers[0]
            if 'advint' in tab_synt:
                type_mot = 'advint'
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
                elif tab_type[indice + 1] == 'cjco':  # le déterminant est suivi par une conjonction de coordination, on élimine
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
        
    def pers_compatible(pers1, pers2):
        """ Renvoie si les personnes (1, 2 ou 3) sont compatibles """
        if pers1 and pers2:
            if pers1 != pers2:
                return False
        return True
        
    def est_conjugue(tab_tag_verb):
        """ renvoie si le verbe est directement conjugué (s'il a une personne pour moi) """
        if tab_tag_verb[4]:
            return True
        return False
        
    def pronom_accorde_verbe(tab_tag_pronom, tab_tag_verbe):
        """ revoie True si le pronom personnel sujet et le verbe sont accordés """
        if pers_compatible(tab_tag_pronom[4],tab_tag_verbe[4]) \
            and nb_compatible(tab_tag_pronom[2], tab_tag_verbe[2]):
            return True
        return False
        
    tab_retour = []
    for tup in tab_new:
        tab_phrase = tup[0].replace("'"," ").replace("  "," ").split(" ")
        nb_mots = len(tab_phrase)
        tab_tag = get_tag_synt(tab_phrase)  # (type_mot, genre, nbr, tps, pers)

        tab_type = [tag[0] for tag in tab_tag]
        nb_verb = tab_type.count('verb')
        coef = 0
        tab_motif_coef = []
        if not "nom" in tab_type:  # pas de nom dans la phrase, on élimine
            continue
        if not verif_noms(tab_type):  # deux noms qui se suivent, on élimine
            continue
        if nb_verb >= 2:
            if not verif_verbes(tab_tag):  # deux verbes qui se suivent, on élimine sous condition
                continue
        if 'det' in tab_type and not verif_determinants(tab_tag):
            continue  # anomalie déterminant, on élimine
            

        if 'proint' in tab_type and not verif_pronom_int(tab_phrase, tab_type):
            continue  # anomalie pronom relatif, on élimine
        if 'prep' in tab_type and not verif_preposition(tab_type):
            continue  # anomalie préposition, on élimine
        if tab_type[0] == "verb" and not (tab_tag[0][3] == "ipre" or tab_tag[0][3] == "impe" or tab_tag[0][3] == "infi"):
            continue  # la phrase commence par un verbe qui n'est pas au présent, à l'impératif ou à l'infinitif
            # TODO : vérification forme interrogative
        if tab_type[nb_mots - 1] == "cjco" or tab_type[nb_mots - 1] == "advint":
            continue        # conjonction de coordination ou adverbe interrogatif en dernier on élimine
        if 'verb' in tab_type :
            for index_mot, type_mot in enumerate(tab_type):
                if type_mot == 'verb':
                    if index_mot == 0:
                        coef -= 1
                        tab_motif_coef.append("A verb en premier : -1")
                    else :
                        nombre_du_verb = tab_tag[index_mot][2]
                        nb_mot_avant = tab_tag[index_mot - 1][2]
                        if nb_mot_avant and nombre_du_verb:
                            if nombre_du_verb != nb_mot_avant:  # le verbe et le mot devant le verbe n'ont pas le même nombre (sing/plur) : malus
                                coef -= 1
                                tab_motif_coef.append("C avant et verb nb diff nb_mot_avant=="+nb_mot_avant+"< nombre_du_verb=="+nombre_du_verb+"<: -1")
                            else:
                                coef += 1
                                tab_motif_coef.append("D avant et verb même diff : +1")
                            
                        type_mot_avant = tab_type[index_mot - 1]
                        if type_mot_avant == 'nom' and tab_tag[index_mot][4] != '3':  # le mot d'avant est un nom et le verbe
                            coef -= 2  # n'est pas à la 3ième personne : malus
                            tab_motif_coef.append("E avant=nom et pers verb != 3 : -2")
                        # pronom personnel sujet, doit s'accorder avec le verbe    
                        if type_mot_avant == 'propersuj' and est_conjugue(tab_tag[index_mot]) \
                                    and pronom_accorde_verbe(tab_tag[index_mot - 1], tab_tag[index_mot]):
                            coef += 2
                            tab_motif_coef.append("F pronom personnel accordé suivi verb : +2")
                        else:
                            coef -= 2
                            tab_motif_coef.append("G pronom personnel non accordé suivi verb : -2")
                    if index_mot < nb_mots - 1:
                        type_mot_apres = tab_tag[index_mot + 1][0]  # le verbe est suivi directement par un nom : malus
                        if type_mot_apres == 'nom':
                            coef -= 1
                            tab_motif_coef.append("H verb suivi par nom : -1")                   
                        if type_mot_apres == 'verb' and est_conjugue(tab_tag[index_mot]) and est_conjugue(tab_tag[index_mot + 1]):
                            coef -= 1 
                            tab_motif_coef.append("H-1 deux verb conjugués de suite : -1") 
                        if type_mot_apres == 'propersuj' and est_conjugue(tab_tag[index_mot]) \
                                    and pronom_accorde_verbe(tab_tag[index_mot + 1], tab_tag[index_mot]):
                            coef += 2
                            tab_motif_coef.append("H-2 verb suivi par pronom presonnel accordé : +2") 
                        else:
                            coef -= 2
                            tab_motif_coef.append("H-3 verb suivi par pronom presonnel non accordé : -2") 
        if 'det' in tab_type :
            for index_mot, type_mot in enumerate(tab_type):
                if type_mot == 'det':
                    type_mot_apres = tab_tag[index_mot + 1][0]  # la phrase ayant un déterminant placé en dernier a déjà été éliminée
                    if type_mot_apres == 'nom' and genre_compatible(tab_tag[index_mot][1],tab_tag[index_mot + 1][1]) \
                                            and nb_compatible(tab_tag[index_mot][2], tab_tag[index_mot + 1][2]):
                        coef += 1  # le déterminant est suivi d'un nom genre et nombre compatible  : bonus
                        tab_motif_coef.append("I det + nom genre te nb ok det="+tab_phrase[index_mot]+" : +1")
        if 'prodem' in tab_type :
            for index_mot, type_mot in enumerate(tab_type):
                if type_mot == 'prodem':
                    if index_mot < nb_mots - 1:
                        type_mot_apres = tab_tag[index_mot + 1][0]   # pronom déterminant
                        if type_mot_apres == 'verb':
                            coef += 1
                            tab_motif_coef.append("J prodem suivi de verb : +1")
                        elif type_mot_apres == 'nom' or type_mot_apres == 'det':
                            coef -= 1
                            tab_motif_coef.append("K prodem suivi de nom ou det : -1")
                    else :              # prodem en dernier
                        coef -= 1
                        tab_motif_coef.append("L prodem en dernier : -1")  
        if 'adj' in tab_type :         # adjectif
            for index_mot, type_mot in enumerate(tab_type):
                if type_mot == 'adj':
                    if index_mot < nb_mots - 1:
                        type_mot_apres = tab_tag[index_mot + 1][0]
                        if type_mot_apres == 'nom':     # si le mot suivant est un nom, il doit s'accorder
                            if genre_compatible(tab_tag[index_mot][1],tab_tag[index_mot + 1][1]) and nb_compatible(tab_tag[index_mot][2], tab_tag[index_mot + 1][2]):
                                coef += 1
                                tab_motif_coef.append("M adj "+tab_phrase[index_mot]+" + nom "+tab_phrase[index_mot + 1]+" accord : +1")
                            else :
                                coef -= 1
                                tab_motif_coef.append("N adj + nom non-accord : -1")
                    if index_mot > 0 :
                        type_mot_avant = tab_tag[index_mot - 1][0]
                        if type_mot_avant == 'det' or type_mot_avant == 'nom':     # si le mot précédent est est un déterminant ou un nom , il doit s'accorder

                            if genre_compatible(tab_tag[index_mot][1],tab_tag[index_mot - 1][1]) and nb_compatible(tab_tag[index_mot][2], tab_tag[index_mot - 1][2]):
                                coef += 1
                                tab_motif_coef.append("O det "+tab_phrase[index_mot-1]+" avant adj "+tab_phrase[index_mot]+" accord : +1")
                            else :
                                coef -= 1
                                tab_motif_coef.append("P det avant adj non-accord : -1")
        if 'prep' in tab_type :          # préposition
            for index_mot, type_mot in enumerate(tab_type):
                if type_mot == 'prep':
                    if index_mot < nb_mots - 1:
                        type_mot_apres = tab_tag[index_mot + 1][0]       # préposition suivie d'un déterminant, d'un nom ou d'un verbe à l'infinitif : bonus
                        # exception pour "au", "aux" : c'est une préposition contractée avec l'article qui suit ("à le") 
                        if tab_phrase[index_mot] != "au" and tab_phrase[index_mot] != "aux" \
                                            and (type_mot_apres =='det' or type_mot_apres =='nom' or (type_mot_apres =='verb' and tab_tag[index_mot + 1][3] == "infi")):
                            coef += 1
                            tab_motif_coef.append("Q det avant adj accord : +1")
                        else:
                            coef -= 1
                            tab_motif_coef.append("P det avant adj non-accord : -1")
                        
                    else :              # préposition en dernier : malus
                        coef -= 1
                        tab_motif_coef.append("P préposition en dernier : -1")
                
        new_tup = (tup[0],coef,tab_motif_coef)
        tab_retour.append(new_tup)
        
    tab_retour = sorted(tab_retour, key=lambda bout: bout[0], reverse=True)
    # print(tab_retour[0:4000])
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
        elif "°" in tab_retour[1]:
            return ""
        elif len(tab_retour) > 7:	# il y a plus d'une erreur et suggestion
            return ""
        if tab_retour[4] and "|" not in tab_retour[4]:           # il y a une suggestion unique grammalecte, on la prends
            if ":" in tab_retour[4]:
                suggestion_gr = tab_retour[4].split(":")[1].strip()
                tab_inter = tab_retour[2].split(" ")[2][1:-1].split(":")
                i_deb = int(tab_inter[0])
                i_fin = int(tab_inter[1])
                deb = tab_retour[0][0:i_deb]
                fin = tab_retour[0][i_fin:]
                a_remplacer = tab_retour[0][i_deb:i_fin]
                if a_remplacer[-1] == "’":
                    suggestion_gr = suggestion_gr + " "
                return (deb + suggestion_gr + fin).replace("’","'")
        return ""

    def verif_grammalecte(phrase, oGrammarChecker):
        """ Vérification de l'orthographe et de la grammaire par grammalecte https://grammalecte.net/ """
        tab_phrase = phrase.split(" ")
        if [x for x in tab_phrase if x in MOTS_INCONNUS_GRA]:   # (intersection) un mot utile n'est pas connu de grammalecte
            return phrase                                       # TODO : rajouter des mots dans grammalecte
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
    tab_existe = []
    for tup in tab_new:
        new_phrase = verif_grammalecte(tup[0], oGrammarChecker)
        if new_phrase and new_phrase not in tab_existe:
        	# TODO ajouter un bonus si tab_existe
            # TODO relancer le calcul du coef si new_phrase != tup[0] (phrase changée par suggestion gramma)
            tab_retour.append((new_phrase, int(tup[1]), tup[2]))
            tab_existe.append(new_phrase)
    return tab_retour


def classer_reponses(tab_new_phrase, tab_phrase_init):
    """ Classe les phrases en attibuant des points :
        - aux phrases contenant des mots trouvés dans le "dictionnaire prioritaire" (dictionnaire des mots usuels dans les contrepèteries)
        - aux phrases contenant des mots de la phrase initiale
    """
    
    def remettre_apos(phrase):
        """ on replace les apostrophe pour que la sortie soit jolie """
        tab_phrase = phrase.split(" ")
        intersection_apos = [x for x in tab_phrase if x in MOTS_PHO_FR]
        #for mot_apos in intersection_apos:
            #phrase = phrase.replace(mot_apos+" ",mot_apos+"'")
        return phrase
        
    def nb_mots_phrase(phrase):
        """ Renvoie le nombre de mots de la phrase"""
        phrase = phrase.replace("'"," ").replace("’", " ")
        return len(phrase.split(" "))
    
    tab_inter = []
    for tup_phrase in tab_new_phrase:
        phrase = tup_phrase[0]
        prio = tup_phrase[1]
        
        tab_motif_coef = tup_phrase[2]
        tab_phrase = phrase.split(" ")
        nb_mots = nb_mots_phrase(phrase)
        if nb_mots == len(tab_phrase_init):     # même nombre de mots  : bonus (discutable)
            prio += 1
            tab_motif_coef.append("Q même nombre de mots : +1")
        else :
            prio -= fabs(nb_mots - len(tab_phrase_init))
            tab_motif_coef.append("R Différence de mots : -"+str(fabs(len(tab_phrase) - len(tab_phrase_init))))
        if sorted(tab_phrase) == sorted(tab_phrase_init):   # la phrase est constituée des mêmes mots: on élimine
            continue
        nb_mots = len(tab_phrase)
        prio_exist = 0
        for i, mot in enumerate(tab_phrase):
            if cle_existe(dico_prio, mot):  # le mot existe dans le dictionnaire prioritaire : bonus
                prio += int(dico_prio[mot][1:])
                tab_motif_coef.append("S Existe dans prioritaire "+mot+": +"+dico_prio[mot][1:])
            if mot in tab_phrase_init:  # le mot existe dans la phrase initiale : bonus

                if len(tab_phrase_init) > i:
                    if tab_phrase_init[i] == mot:  # et à la même place : bonus!
                        prio_exist += 1
                        tab_motif_coef.append("T et à la même place :"+mot+": +1")
        if prio_exist >= len(tab_phrase_init) - 1:  # trop de priorité tue la priorité!
            prio_exist = 1
            tab_motif_coef.append("U RAZ : somme(T= = +1")

        tab_inter.append((phrase, prio + prio_exist, tab_motif_coef))
    tab_inter = sorted(tab_inter, key=lambda bout: bout[1], reverse=True)
    
    if len(tab_inter) > NB_MAX_PHRASES:     # limitation arbitraire du nombre de résultat renvoyé
        tab_inter = tab_inter[:NB_MAX_PHRASES]

    bonus_max = tab_inter[0][1]  # note maximale attribuée à une des phrases
    max_prio = bonus_max - NB_NIVEAUX_PRIO_MAX      # on ne prends que les meilleures > max_prio
    return [(remettre_apos(elem[0]), elem[1], elem[2]) for elem in tab_inter if elem[1] > max_prio]


def verif_suggestion_gg(tab_new_phrase, suggestion):
    """ Si la suggestion gg est déjà parmi nos choix, c'est vraiement la bonne """
    if suggestion[1] in [el[1] for el in tab_new_phrase]:
        return True
    return False


def gg_est_mon_ami(phrase_orig, phrase_tab_phon, phrase):
    """ la phrase trouvée est vérifiée par une recherche sur google """
    
    def verif_phonemes(phrase_tab_phon, phrase):
        """ Vérifie que les phonèmes de la phrase de départ se retrouvent dans la phrase française
            retraduite en phonétique
        """
        tab_phrase = get_tab_phrase(phrase)
        phrase_pho = get_phrase_pho(tab_phrase, " ")
        if phrase_tab_phon == sorted(get_tab_phonemes(phrase_pho)):
            return True
        return False
    
    global gg_bloque
    if ACTIVER_GG and not gg_bloque:
        sleep(uniform(1, 2))        # on laisse un temps entre deux appels sinon google y bloque...
        url = URL_GG + '"' + phrase + '"'
        result = get(url, headers=HEADERS)
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
        if suggestion_gg and suggestion_gg != phrase_orig and verif_phonemes(phrase_tab_phon, suggestion_gg):  # on vérifie que tous les phonèmes sont dans la suggestion
            if nb_res != 0:
                return 666, suggestion_gg, "mg", gg_bloque
            else:
                return 1, suggestion_gg, "mg", gg_bloque
        return (nb_res, phrase, "", gg_bloque)
    else:  # pour tests, évite les lenteurs et le blacklistage ou si gg_bloque
        print("ACTIVER_GG",ACTIVER_GG,"gg_bloque",gg_bloque)
        return (0, phrase, "", gg_bloque)

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
        
    def sous_chaines_ok(subst_1, subst_2):
        """ Vérifie la compatibilité des sous chaines """
        if chaines_includes(subst_2, subst_1) and chaines_includes(subst_1, subst_2):
            return False
        if len(subst_1) == 1 or len(subst_2) == 1:
            if subst_1 == "Y" or subst_2 == "Y":    # "ill" est échangeable avec tout
                return True
            if subst_1 in VOYELLES_PHO_SUBS and subst_2 in CONSONNES_PHO_SUBS:
                return False
            elif subst_2 in VOYELLES_PHO_SUBS and subst_1 in CONSONNES_PHO_SUBS:
                return False
        return True

    def verif_subst(subst_1, subst_2):
        """ Vérifie que les chaines de substitution sont compatibles. Cas foireux :
                - les chaines sont les mêmes
                - les chaines sont incluses l'une dans l'autre
                - une voyelle ne doit pas être substituée par une consonne
        """
        return subst_1 != subst_2 and sous_chaines_ok(subst_1, subst_2)

    def intervertir_dans_chaine(chaine, subst_1, subst_2, oc_1, oc_2):
        """ Inverse l'occurence oc_1 le la sous chaine subst_1 et l'occurence oc_2 le la sous chaine subst_2 dans la chaine """
        # remplacement subst_1 par subst_2
        where = [m.start() for m in finditer(subst_1, chaine)][oc_1-1]
        before = chaine[:where]
        after = chaine[where:]
        after = after.replace(subst_1, subst_2, 1)
        chaine = before + after
        # remplacement subst_2 par subst_1
        where = [m.start() for m in finditer(subst_2, chaine)][oc_2-1]
        before = chaine[:where]
        after = chaine[where:]
        after = after.replace(subst_2, subst_1, 1)
        chaine = before + after
        return chaine

    def chercher_toute_subst(chaine, subst_1, subst_2):
        """ Renvoie le tableau des chaines après substitution.
            (Si l'une ou les deux des chaines de substitution existent plusieurs fois dans "chaine"
            il y a plusieurs chaines substituées résultantes)
        """
        tab_retour = []
        for i in range(chaine.count(subst_1)):
            for j in range(chaine.count(subst_2)):
                chaine_res = intervertir_dans_chaine(chaine, subst_1, subst_2, i, j)
                if chaine_res != chaine and chaine_res[-2:] in TERMINAISONS:
                    tab_retour.append(chaine_res)
        return tab_retour
    tab_retour = []
    for index_subst_1 in range(len(tab_subst)):
        subst_1 = tab_subst[index_subst_1]
        for index_subst_2 in range(len(tab_subst)):
            subst_2 = tab_subst[index_subst_2]
            if verif_subst(subst_1, subst_2):
                tab_retour += chercher_toute_subst(chaine, subst_1, subst_2)
    tab_retour = list(set(tab_retour))  # suppression des doublons
    return tab_retour


def commence_voyelle(mot):
    """ Renvoie si un mot phonétique commence par une voyelle """
    if not mot:
        return False
    return mot[0] in VOYELLES_PHO


def get_toutes_phrases(tab_chaines, nb_mots_pho_orig):
    """ Renvoie un tableau de toutes les phrases phonétiques possibles d'un tableau de chaines """

    def verif_phrases(phrase, nb_mots_pho_orig):
        """ Éliminer un max de phrases incorrectes
            # Le dernier mot ne doit pas avoir d'apostrophe
            # Le mot suivant un mot à apostrophe doit commencer par une voyelle
            # Le dernier mot doit de trouver dans le dictionnaire
            # Le dernier mot ne doit pas se trouver dans MOTS_IMPOSSIBLE_FIN
            # Pas trop de différence de nombre de mots avec la phrase phonétique d'origine
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
        if not cle_existe(dico_phonetik, tab_phrase[-1]):
            return False
        if tab_phrase[-1] in MOTS_IMPOSSIBLE_FIN:
            return False
        if fabs(len(tab_phrase) - nb_mots_pho_orig) > DIFF_NB_MOTS:
            return False
        return True

    def contient_prio(phrase):
        """ Renvoie vrai si un des mots de la phrase phonétique se trouve dans le dictionnaire dico_prio_pho """
        tab_phrase = phrase.split(" ")
        if [elt for elt in tab_phrase if cle_existe(dico_prio_pho, elt)]:
            return True
        return False
        
    def classer_phrase_pho(tab_mots):
        """ On classe les phrases phonétiques par nombre de mots 
            Si le nombre de phrases est supérieur à NB_MAX_PHRASES_PHO, 
            on tronque à NB_MAX_PHRASES_PHO en gardant celles qui ont le moins de mots et qui contiennent un mot prioritaire.
        """
        tab_mots = sorted(tab_mots,key= lambda bout: len(bout.split(" ")))  # classer par nb de mots ascendant        
        nb_a_virer = len(tab_mots) - NB_MAX_PHRASES_PHO
        if nb_a_virer <= 0:
            return tab_mots
        tab_retour = []
        while nb_a_virer and tab_mots: 
            phrase = tab_mots.pop()
            nb_a_virer -= 1
            if contient_prio(phrase):
                tab_retour.append(phrase)
        tab_retour += tab_mots
        tab_retour = sorted(tab_retour,key= lambda bout: len(bout.split(" ")))      # on classe par nombre de mots ascendant
        if len(tab_retour) > NB_MAX_PHRASES_PHO:          # on tronque
            tab_retour = tab_retour[:NB_MAX_PHRASES_PHO]
        return tab_retour

    def chercher_phrases(chaine, nb_mots_pho_orig):
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
                        if verif_phrases(my_res, nb_mots_pho_orig):
                            tabs.append(my_res.strip())
        return tabs

    tab_phrases = []
    for chaine_res in tab_chaines:
        tab_res = chercher_phrases(chaine_res, nb_mots_pho_orig)
        tab_phrases = tab_phrases + tab_res    
    tab_phrases = list(set(tab_phrases))  # suppression des doublons
    nb_phrases = len(tab_phrases) 
    tab_phrases = classer_phrase_pho(tab_phrases)
    return (tab_phrases, nb_phrases)


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
            if commence_voyelle(suite):
                if cle_existe(dico_phonetik, suite):
                    tab_suite = dico_phonetik[suite]
                    if tab_suite:
                        tab_w = []
                        tab_w.append(dico_phonetik[char])
                        tab_w.append(tab_suite)
                        liste_w = list(map("'".join, (list(product(*tab_w)))))
                        tab_mot_pho += [elt for elt in liste_w if "''" not in elt]          
        return tab_mot_pho

    def get_tupple_phrase(phrase_pho, tab_res_fr):
        """ Renvoie un tableau de tous les tupple possibles (phrase_pho, phrase_fr) """
        tab_retour = []
        map_list = map(' '.join, (list(product(*tab_res_fr))))

        for phrase_fr in map_list:
            phrase_fr = phrase_fr.replace("' ","'") 
            tab_retour.append((phrase_fr, phrase_pho))
        return tab_retour

    tab_tupple_retour = []
    for phrase_pho in tab_phrases:
        tab_pho = phrase_pho.split(" ")
        tab_res_fr = []
        for mot_pho in tab_pho:
            tab_mots_fr = get_mots_possibles(dico_phonetik, mot_pho)
            
            tab_res_fr.append(tab_mots_fr)
        tab_tupple_retour += get_tupple_phrase(phrase_pho, tab_res_fr)
    tab_tupple_retour = list(set(tab_tupple_retour))  # suppression des doublons
    return tab_tupple_retour

def traiter_saisie(phrase):
    """ Modifie la phrase de saisie : en minuscule et enlève la ponctuation
    """
    phrase = phrase.lower().strip().replace("’", "'").replace("-", " ")
    return sub(r'[.,"?:!;]', '', phrase)



# TODO : Liaisons : traiter les liaisons des doubles consonnes (un-navet)
# TODO : Faire plusieurs substitutions
# TODO : Traiter les échanges avec "" (rien) (Ex : le tout de mon cRu)
# TODO : virer verif_phonemes_pho




