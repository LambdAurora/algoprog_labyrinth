# --------------------------------------------------------------
# Samedi 30 juin 2018
# Arash Habibi
# construction labyrinth
# --------------------------------------------------------------

import random
import math


# --------------------------------------------------------------
# n : entier
# retourne un booleen : True si n est impair et False autrement.

def estImpair(n):
    return n % 2 != 0


# --------------------------------------------------------------
# n : entier
# retourne un entier : le nombre de chiffres de n en decimal

def nbChiffres(n):
    if n < 10 and n > -10:
        return 1
    else:
        return 1 + nbChiffres(n / 10)


# --------------------------------------------------------------
# n : entier
# max : entier
# On suppose que n est inferieur a max.
# Cette fonction retourne une chaine de caracteres constituee
# d'autant de caracteres qu'il y a de chiffres dans max - 1.
# Ces caracteres representent les chiffres de n suivi d'espaces

def entierNbCaracteresFixe(n, max):
    nb_digits_n = nbChiffres(n)
    nb_digits_m = nbChiffres(max)
    if nb_digits_m < nb_digits_n:
        print("intToSTring : n must be smaller than max.")
        return ""
    else:
        output = str(n)
        for i in range(nb_digits_m - nb_digits_n - 1):
            output += " "
        return output


# --------------------------------------------------------------
# max : entier
# cette fonction retourne une chaine de caracteres composee d'espaces.
# Autant d'espaces que le nombre de chiffres de max - 1.

def rembourrage(max):
    nb_digits_m = nbChiffres(max)
    output = ""
    for i in range(nb_digits_m - 1):
        output += " "
    return output


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# Une classe representant la position d'une cellule dans
# le labyrinthe (l'abscisse et l'ordonnee entieres).

class Cellule:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # ----
    # Retourne une chaine de caracteres representant le couple d'entiers

    def enChaine(self):
        return "(" + entierNbCaracteresFixe(self.x, 1000) + "," + entierNbCaracteresFixe(self.y, 1000) + ")"

    # ----
    # Affiche sur le terminal les composantes du couple

    def montre(self, label=""):
        if len(label) == 0:
            print(self.enChaine())
        else:
            print(label + " : " + self.enChaine())

    # ----
    # c1 et c2 etant des cellules,
    # c1 % c2 est une cellule (mais avec des composantes flottantes)
    # representant le milieu de c1 et de c2.

    def __mod__(self, c):
        return Cellule((self.x + c.x) / 2, (self.y + c.y) / 2)

    # ----
    # c est une cellule
    # retourne un booleen valant True si les composantes de la cellule
    # courante sont les memes que celles de c. Retourne False sinon.

    def estEgalA(self, c):
        return self.x == c.x and self.y == c.y

    # ----
    # c1 et c2 sont des cellules
    # Retourne un booleen valant True si la cellule courante est
    # au milieu de c1 et de c2

    def estAuMilieuDe(self, c1, c2):
        return c2.x - self.x == self.x - c1.x and c2.y - self.y == self.y - c1.y


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

class pileCellules:

    def __init__(self):
        self.tableau = []
        self.premiere_place_libre = 0

    def montre(self, label=""):
        print("Montre pile de cellules : (" + label + ")")
        for i in range(0, self.premiere_place_libre):
            self.tableau[i].montre(str(i) + " : ")

    def estVide(self):
        return self.premiere_place_libre == 0

    def empiler(self, c):
        self.tableau += [c]
        self.premiere_place_libre += 1

    def depiler(self):
        if self.premiere_place_libre > 0:
            self.premiere_place_libre -= 1
        else:
            print("pileCelules.depiler : la pile est vide. Impossible de depiler")

    def tete(self):
        return self.tableau[self.premiere_place_libre - 1]


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# Cette classe represente les voisins d'une cellule
# Les voisins simples sont simplement les voisins qui sont
# cote a cote. Les voisins relies sont des voisins relies par
# un couloir.
# Toutes les cellules ont toujours 4 voisins simples
# sauf si elles sont au bord (3 voisins) ou dans un coin (2 voisins)
# Ce sont les voisins relies qui definissent la topologie du labyrinthe.

class Voisins:

    def __init__(self):
        self.simples = []
        self.relies = []

    # ----

    def montre(self, label=""):
        print("montre voisins : " + label + "---------------------")
        voisins = "voisins : "
        for nv in range(len(self.simples)):
            voisins += self.simples[nv].enChaine() + " "
        print(voisins)

        voisins = "voisins relies : "
        for nv in range(len(self.linked_voisins)):
            voisins += self.relies[nv].enChaine() + " "
        print(voisins)


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# Le marqueur d'exploration
# Un tableau 2D de booleens qui permet de marquer les cellules
# du labyrinthe qui ont deja ete explorees.

class MarqueurDExploration:

    def __init__(self, larg, haut):
        self.larg = larg
        self.haut = haut
        self.grille = []
        for i in range(larg * haut):
            self.grille += [False]

    def init(self):
        for i in range(len(self.grille)):
            self.grille[i] = False

    def marquer(self, c):
        indice = c.y * self.larg + c.x
        self.grille[indice] = True

    def estMarquee(self, c):
        indice = c.y * self.larg + c.x
        return (self.grille[indice])

    def montre(self, label=""):
        print("Montre Exploration (" + label + ")--------")
        print(str(self.larg) + " x " + str(self.haut))
        for y in range(self.haut):
            ligne = ""
            for x in range(self.larg):
                if (self.grille[y * self.larg + x]):
                    ligne += "T "
                else:
                    ligne += "F "
            print(ligne)


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

class Labyrinthe:
    def __init__(self, mtx_largeur, mtx_hauteur, niveau=3):

        # Dimensions du labyrinthe aux murs epais
        self.mtx_largeur = mtx_largeur
        self.mtx_hauteur = mtx_hauteur
        # Diemsnsions du labyrinthe aux murs fins
        self.largeur = (mtx_largeur - 1) // 2
        self.hauteur = (mtx_hauteur - 1) // 2

        self.niveau = niveau
        self.entree = Cellule(0, 0)
        self.sortie = Cellule(0, 0)

        self.construire(self.largeur, self.hauteur, niveau)
        self.choixEntreeSortie(niveau)

    # ----

    def montre(self, quoi=0, label=""):
        if (quoi == 0):
            print("Cellules (" + label + ")")
            for ny in range(self.hauteur):
                colonne = ""
                for nx in range(self.largeur):
                    colonne += self.cellules[nx][ny].enChaine() + " "
                print(colonne)

        elif (quoi == 1):
            print("Nombre de voisins simples (" + label + ")")
            for ny in range(self.hauteur):
                colonne = ""
                for nx in range(self.largeur):
                    colonne += str(len(self.tab_voisins[nx][ny].simples)) + " "
                print(colonne)

        elif (quoi == 2):
            print("Nombre de voisins relies (" + label + ")")
            for ny in range(self.hauteur):
                colonne = ""
                for nx in range(self.largeur):
                    colonne += str(len(self.tab_voisins[nx][ny].relies)) + " "
                print(colonne)

    # ----
    # Cree un tableau de largeur x hauteur cellules

    def creerCellules(self):
        self.cellules = []
        for nx in range(self.largeur):
            colonne = []
            for ny in range(self.hauteur):
                colonne += [Cellule(nx, ny)]
            self.cellules += [colonne]

    # ----
    # Definit le voisinage simple

    def initVoisins(self):
        self.tab_voisins = []
        for nx in range(self.largeur):
            colonne = []
            for ny in range(self.hauteur):
                colonne += [Voisins()]
            self.tab_voisins += [colonne]

        for nx in range(self.largeur):
            for ny in range(self.hauteur):
                if (nx == 0):
                    self.tab_voisins[nx][ny].simples += [Cellule(nx + 1, ny)]
                elif (nx == self.largeur - 1):
                    self.tab_voisins[nx][ny].simples += [Cellule(nx - 1, ny)]
                else:
                    self.tab_voisins[nx][ny].simples += [Cellule(nx - 1, ny)]
                    self.tab_voisins[nx][ny].simples += [Cellule(nx + 1, ny)]

                if (ny == 0):
                    self.tab_voisins[nx][ny].simples += [Cellule(nx, ny + 1)]
                elif (ny == self.hauteur - 1):
                    self.tab_voisins[nx][ny].simples += [Cellule(nx, ny - 1)]
                else:
                    self.tab_voisins[nx][ny].simples += [Cellule(nx, ny - 1)]
                    self.tab_voisins[nx][ny].simples += [Cellule(nx, ny + 1)]

    # ----
    # c1 et c2 sont des cellules
    # Cette fonction met c2 dans les voisins relies de c1 et vice-versa

    def relier(self, c1, c2):
        self.tab_voisins[c1.x][c1.y].relies += [c2]
        self.tab_voisins[c2.x][c2.y].relies += [c1]

    # ----
    # c est une cellule
    # Cette fonction retourne la liste des voisins simples non explores de c

    def voisinsSimplesNonExplorees(self, c):
        non_explorees = []
        voisins = self.tab_voisins[c.x][c.y].simples
        for nv in range(len(voisins)):
            v = voisins[nv]
            if (not self.expl.estMarquee(v)):
                non_explorees += [v]
        return non_explorees

    # ----
    # c est une cellule
    # Cette fonction choisit au hasard et retourne une des voisins simples
    # et non explorees de c.

    def voisinSimpleNonExploreAuHasard(self, c):
        non_explores = self.voisinsSimplesNonExplorees(c)
        if (len(non_explores) == 0):
            # print("Labyrinthe.voisinSimpleNonExploreAuHasard : " + c.enChaine() + " n'a aucun voisin non exploree")
            return 0
        else:
            rnd = int(len(non_explores) * random.random())
            return (non_explores[rnd])

    # ----
    # c est une cellule
    # A partir de la cellule c, cette fonction
    # explore le labyrinthe non explore de facon aleatoire
    # jusqu'a tomber sur une impasse. Elle retourne la pile
    # constituee des cellules parcourues.

    def marcheAleatoire(self, c):
        impasse = False
        chemin = pileCellules()
        while (not impasse):
            chemin.empiler(c)
            self.expl.marquer(c)
            voisin = self.voisinSimpleNonExploreAuHasard(c)
            if (voisin == 0):
                impasse = True
            else:
                self.relier(c, voisin)
                c = voisin
        return chemin

    # ----
    # c est une cellule
    # A partir de la cellule c, cette fonction
    # explore le labyrinthe non construit de facon aleatoire
    # jusqu'a tomber sur une impasse. Puis elle revient sur
    # ses pas et fait de meme avec toutes les cellules qui ont
    # encore des voisins non explorees.

    def marcheAleatoireRecursive(self, c):
        chemin = self.marcheAleatoire(c)
        issue_trouvee = False
        while (not chemin.estVide()):
            t = chemin.tete()
            v = self.voisinSimpleNonExploreAuHasard(t)
            if (v != 0):
                self.marcheAleatoireRecursive(t)
            else:
                chemin.depiler()

    # ----
    # Etant donnes une largeur, une hauteur et un niveau, cette fonction
    # creer les cellules, les voisins et les chemins.
    # L'entree et la sortie ne sont pas choisies

    def construire(self, largeur, hauteur, niveau):
        self.expl = MarqueurDExploration(self.largeur, self.hauteur)
        self.creerCellules()
        self.initVoisins()

        depart = self.cellules[int(self.largeur * random.random())][int(self.hauteur * random.random())]
        self.marcheAleatoireRecursive(depart)

    # ----
    # Cette fonction retourne la liste des cellules qui sont des impasses
    # c'est a dire celles qui sont reliees a seulement une autre cellule.

    def lesImpasses(self):
        impasses = []
        for nx in range(self.largeur):
            for ny in range(self.hauteur):
                c = self.cellules[nx][ny]
                if (len(self.tab_voisins[nx][ny].relies) == 1):  # si impasse
                    impasses += [c]
        return impasses

    # ----
    # Cette fonction parcourt toutes les impasses (cellules qui ne sont reliees qu'a une seule cellule voisine
    # Elle trouve le plus long chemin qu'on peut parcourir a partir de cette impasse sans rencontrer de
    # jonction ou d'autre impasse. Elle retourne ce chemin le plus long.

    def impasseLaPlusLongue(self):
        impasses = self.lesImpasses()
        longueur_max = 0
        plus_longue_impasse = []
        for imp in impasses:
            chemin = [imp]
            c = self.tab_voisins[imp.x][imp.y].relies[0]
            oldc = imp
            ya_deux_voisins = True
            while (ya_deux_voisins):
                chemin += [c]
                if (len(self.tab_voisins[c.x][c.y].relies) != 2):
                    ya_deux_voisins = False
                else:
                    vois1 = self.tab_voisins[c.x][c.y].relies[0]
                    vois2 = self.tab_voisins[c.x][c.y].relies[1]
                    if (vois1.estEgalA(oldc)):
                        vois = vois2
                    else:
                        vois = vois1
                    oldc = c
                    c = vois
            if (len(chemin) > longueur_max):
                longueur_max = len(chemin)
                plus_longue_impasse = chemin
        return (plus_longue_impasse)

    # ----
    # Cette fonction trouve deux cellules non voisines mais qui ont une voisine commune
    # On veut que la probabilite que les trois cellules soient alignees soit la meme
    # que la proabilite qu'elles ne soient pas alignees. Par ailleurs, on privilegiera
    # les cellules qui ont beaucoup de voisins.

    def aDeuxPasLunDeLAutre(self):
        meilleure_note = 0
        cherche_alignes = True
        if (random.random() < 0.5):
            cherche_alignes = False
        if (cherche_alignes):
            for nx in range(self.largeur):
                for ny in range(self.hauteur):
                    c1 = self.cellules[nx][ny]
                    nb_vois1 = len(self.tab_voisins[nx][ny].relies)
                    for nv1 in range(nb_vois1):
                        c2 = self.tab_voisins[nx][ny].relies[nv1]
                        nb_vois2 = len(self.tab_voisins[c2.x][c2.y].relies)
                        note = nb_vois1 + nb_vois2
                        if (note > meilleure_note):
                            meilleure_note = note
                            entree = c1
                            sortie = c2
        else:
            for nx in range(self.largeur):
                for ny in range(self.hauteur):
                    c = self.cellules[nx][ny]
                    note = len(self.tab_voisins[nx][ny].relies)
                    if (note > meilleure_note):
                        meilleure_note = note
                        angle = c
            nb_vois = len(self.tab_voisins[angle.x][angle.y].relies)
            c1 = self.tab_voisins[angle.x][angle.y].relies[0]
            if (nb_vois == 2):
                c2 = self.tab_voisins[angle.x][angle.y].relies[1]
            else:
                for nv in range(1, nb_vois):
                    vois = self.tab_voisins[angle.x][angle.y].relies[nv]
                    if (not angle.estAuMilieuDe(c1, vois)):
                        c2 = vois
            entree = c1 % angle
            sortie = c2 % angle
        return (entree, sortie)

    # ----
    # niveau est un entier compris entre 1 et 3
    # Cette fonction choisit l'entree et la sortie du labyrinthe en fonction du niveau
    # niveau 1 : l'entree et la sortie sont a deux pas l'une de l'autre
    # niveau 2 : l'entree et la sortie sont plus loin, mais le chemin de l'un vers l'autre ne contient aucune bifurcation
    # niveau 3 : l'entree est en haut a gauche et la sortie en bas a droite

    def choixEntreeSortie(self, niveau):
        if (niveau >= 3):
            self.entree = Cellule(0, 0)
            self.sortie = Cellule(self.largeur - 1, self.hauteur - 1)
        elif (niveau == 2):
            chemin = self.impasseLaPlusLongue()
            self.entree = chemin[0]
            self.sortie = chemin[-1]
        elif (niveau == 1):
            (self.entree, self.sortie) = self.aDeuxPasLunDeLAutre()
        else:
            print("Labyrinthe.choixEntreeSortie : le niveau peut seulement etre 1, 2 ou 3.")

    # ----

    def tableau2D(self):
        tab_2D = []
        for nx in range(self.mtx_largeur):
            colonne = []
            for ny in range(self.mtx_hauteur):
                if (estImpair(nx) and estImpair(ny)):
                    colonne += [1]
                else:
                    colonne += [0]
            tab_2D += [colonne]

        for nx in range(self.largeur):
            for ny in range(self.hauteur):
                c = self.cellules[nx][ny]
                for nv in range(len(self.tab_voisins[nx][ny].relies)):
                    v = self.tab_voisins[nx][ny].relies[nv]
                    m = c % v
                    tab_2D[int(2 * m.x + 1)][int(2 * m.y + 1)] = 1

        tab_2D[int(2 * self.entree.x) + 1][int(2 * self.entree.y) + 1] = 2
        tab_2D[int(2 * self.sortie.x) + 1][int(2 * self.sortie.y) + 1] = 3

        return tab_2D

    # ----

    def montreTab_2D(self):

        tab_2D = self.tableau2D()

        output = rembourrage(1000) + " "
        for nx in range(self.largeur):
            if (nx % 2 == 0):
                output += entierNbCaracteresFixe(nx, 100)
            else:
                output += rembourrage(100)
        print(output)

        for ny in range(2 * self.hauteur + 1):
            if (ny % 2 == 0):
                output = rembourrage(1000)
            else:
                output = entierNbCaracteresFixe((ny - 1) // 2, 1000)

            for nx in range(2 * self.largeur + 1):
                if (tab_2D[nx][ny] == 0):
                    output += "x"
                elif (tab_2D[nx][ny] == 1):
                    output += " "
                else:
                    output += "#"
            print(output)


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

def creer(largeur, hauteur, niveau=3):
    laby = Labyrinthe(largeur, hauteur, niveau)
    # laby.montreTab_2D()
    return (laby.tableau2D())

# lst = creer(9, 15, niveau=1)
# print(lst)
