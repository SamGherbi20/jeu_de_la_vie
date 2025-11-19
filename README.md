# piCSelart
**“Laissez les mathématiques colorier pour vous !”**

## Notre produit (MVP,MVC)

Peut-on **dynamiser** le pixel art ? Avec le jeu de la vie, pourquoi pas ?

Nous avons voulu, à partir d'un pixel-art **morne** et **statique**, qu'on appellera “squelette”, réussir à en remplir les “régions” ainsi délimitées de l’univers avec des couleurs : le caractère morne a disparu !

C'est grâce à un **jeu de la vie** régi par les **mathématiques**, qu'on observerait à la fois le remplissage de chacune des régions et qu'on obtiendrait un coloriage dynamique, vivant, presque aléatoire : le caractère statique a disparu !

Ce produit est d'usage récréatif. Il saura éveiller tout aussi bien la curiosité des artistes que ceux des matheux.

## Quelques détails techniques.

Des fonctions mathématiques bien choisies vont contrôler la valeur de couleur de chaque cellule colorée, à partir de celles voisines. Ainsi, **pas d’uniformisation, mime d'un comportement pseudo-chaotique, le tout avec une esthétique agréable.**

Un **squelette** correspond à l'ensemble des frontières. 
Les **frontières** sont soit :
- Dessinées au départ par l’utilisateur,
- Délimitées par une image importée par l'utilisateur (elle-même transposée en frontière par le programme). 

Les frontières délimitent ainsi des morceaux de l’espace où donc, plusieurs jeux de la vie se déroulent **indépendamment** les uns des autres.

L’enjeu est donc le suivant : de découvrir comment les fonctions choisies permettent de dynamiser le pixel art auparavant fixe, avec des couleurs toujours en mouvement !

## Prérequis - Paramétrage

Modules à installer depuis un terminal bash avec la command pip install "module" :
- numpy
- opencv-python
- tkinter
- pygame
- matplotlib.pyplot
- sys
- scipy

## Tutoriel - Comment utiliser le produit ?

- Commencez par importer les modules ci-dessus.
- Lancez le programme

2 fenêtres apparaissent :  

**1ère fenêtre : celle en plein écran.**
- Commencez par lire le tutoriel in-game (en bleu)
- Voici son contenu :  
R : réinitialiser la map  
Espace : mettre le jeu en pause  
Clic-gauche (le jeu doit être en pause) : rajouter une graine/une frontière  
F : enlever toutes les frontières  
B : switcher entre mode graine / mode frontière

- Choisissez la fonction de génération: un conseil, commencez avec Dirichlet n = 50
- Modifiez les coefficients k/n
- Choisissez la colormap
- Choisissez la vitesse de génération
- Cliquez sur VALIDER.

**Vous pouvez ensuite aller sur la seconde fenêtre:**
- Choisissez l'image à importer, le nom du fichier image_pixelisée, la taille maximale d'un pixel (+ elle est grande, + ça sera précis).
- Cliquez sur Lancer le traitement
- Fermez la fenêtre



## Stratégie - Feuille de route
**Objectif 1 : Échapper à un remplissage uniforme : propagation chaotique**
- Fonctionnalité 1 : Import d’un panel de couleur
- Fonctionnalité 2 : Définition d’une “bonne” - fonction de croissance
- Fonctionnalité 3 : Initialisation de l’univers – Définition des conditions initiales 
- Fonctionnalité 4 : Evolution de l’univers génération après génération

**Objectif 2 : Délimiter les zones de dessin : les frontières**
- Fonctionnalité 5 : Régulation des frontières  
- Fonctionnalité 6 : Indépendance des zones et des jeux de la vie  

**Objectif 3 : Contrôler la grille : l’interface graphique**
- Fonctionnalité 7 : Choix de la taille de l’univers 
- Fonctionnalité 8 : Choix de la colormap 
- Fonctionnalité 9 : Tracé des frontières “à la main”
- Fonctionnalité 10 : Choix et paramétrage des fonctions de croissance
- Fonctionnalité 11 : Placement des couleurs initiales
- Fonctionnalité 12 : Ajout d’automates in-game

**Objectif 4 : Transposer une photo en pixel art : conversion photo-pixel**
- Fonctionnalité 13 : Choix, importation et lecture de l’image
- Fonctionnalité 14 : Traitement de l’image : application d’un flou et passage N&B
- Fonctionnalité 15 : Détermination des frontières, localisation des zones, mise sous la forme d’une matrice

**Objectif 5 : Le tout, dans une seule et même application**
- Fonctionnalité 16 : Cohérence entre les 2 sous-codes
- Fonctionnalité 17 : Finition, ergonomie

## Développement réel

- Modification de l’implémentation de l’état des cellules du jeu de Conway, de sorte qu’elle puisse prendre des valeurs continues entre 0 et 1, afin de modifier la couleur de chaque cellule en fonction de sa valeur, selon des règles de colour mapping (matplotlib).
- Introduction de nouvelles règles de propagation des couleurs sur la grille : la somme des valeurs des voisins est passée en argument d’une fonction mathématique donnant la nouvelle valeur.
- Utilisation de Tkinter pour permettre à l’utilisateur de rentrer différents paramètres : taille de la grille, colour map, fonction et ses paramètres…
- Programmation de la lecture de photos pour reconnaître les différentes zones à colorier dans une image. Le programme ouvre la photo, la redimensionne, passe un filtre floutant pour enlever du détail, convertit l’image en noir et blanc.
- Ajout d'une fonctionnalité pour repérer et compter les différentes zones à colorier de l’image.
- Avec les différentes zones, on améliore le programme de propagation de couleur pour qu’il soit implémentes dans des zones de toutes formes : d’abord rectangulaire, puis arbitraire. Ce que l’on fait alors c’est empêcher le jeu de se propager aux frontières.
- Ajout d'une fonctionnalité pygame permettant de tracer manuellement les frontières.
Nous avons ensuite combiné les deux programmes principaux afin d’utiliser le traitement d’image dans le jeu de la vie.
- Amélioration de l’interface Tkinter pour afficher les règles au démarage.

## Notre équipe

- Délégué : Ryliskis Arsène
- Respo COM & Brainstorm : Luong Ethan
- Respo Performances et Stabilité : Delmas Pierre
- Respo Mathématiques : Gherbi Samuel 
- Respo Innovation : Aupretre Damien

- Respo Photo : Evreux Simon
