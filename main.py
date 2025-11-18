import pygame
import numpy as np
import sys
import cv2
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, StringVar, Radiobutton, filedialog, messagebox
from scipy.special import *
from fonctions_propagation import *
from PIL import Image, ImageTk
from propagation_rules import *
from transformation_couleur import *

# Initialisation de Pygame
pygame.init()

def process_image():
    # on commence par chercher le chemin de l'image que l'on va utiliser, puis on demande le nom que devront
    # avoir les images modifiées
    image_path = entry_path.get()
    output_name = entry_name.get()
    try:
        max_size = int(entry_size.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une taille maximale valide.")
        return

    if not image_path or not output_name:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    # on charge l'image
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Erreur", "L'image n'a pas pu être chargée. Vérifiez le chemin.")
        return

    # on cherche les dimensions de l'image initiale
    original_height, original_width = image.shape[:2]
    print(f"Taille originale de l'image : {original_width}x{original_height} pixels")

    # on redimensionne l'image pour que le côté le plus long soit égal à la taille donnée par l'utilisateur
    height, width = image.shape[:2]
    if height > max_size or width > max_size:
        scaling_factor = min(max_size / height, max_size / width)
        new_width = int(np.minimum(width, height) * scaling_factor)
        new_height = int(np.minimum(width, height) * scaling_factor)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_size = f"{new_width}x{new_height}"
    else:
        resized_size = f"{width}x{height}"

    print(f"Taille après redimensionnement : {resized_size} pixels")

    # On traite l'image pour la passer en noir et blanc et appliquer un filtre de flou
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # on détecte les contours présents dans l'image
    edges = cv2.Canny(gray, 50, 150)

    # on modifie les contours détectés pour corriger les erreurs induites par le redimensionnement et le filtre 
    # afin de fermer les contours dessinés
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=2)
    thin_contours = cv2.erode(closed, kernel, iterations=1)
    grid_univers = (thin_contours > 0).astype(np.uint8)

    # on cherche des zones fermées par des contours
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=3)
    inverted_binary = cv2.bitwise_not(closed)
    contours, _ = cv2.findContours(inverted_binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # On calcule le nombre de zones, et on les discrimine pour ne garder que les plus grandes
    num_zones = len(contours)
    total_area = image.shape[0] * image.shape[1]
    threshold_area = total_area * 0.001

    # création d'une liste contenant les pixels de chaque zone conservée
    zones_pixels = []

    # On met des couleurs aléatoires dans chacune des zones pour pouvoir mieux les visualiser
    #et on remplit la liste contenant les pixels des différentes zones
    grid_colored = np.zeros_like(image)
    colored_zones = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= threshold_area:

            # on répertorie les pixels constituant la zone
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

            # conversion des pixels en liste de tuples (y, x)
            zone_pixels = [(int(y), int(x)) for y, x in zip(*np.where(mask == 255))]
            zones_pixels.append(zone_pixels)


    # on reprend la grille univers avec seulement les contours en noir et blanc
    global grid_bw
    grid_bw = (grid_univers * 255).astype(np.uint8)
    
    print(f"Nombre total de zones gardées : {len(zones_pixels)}")
    
    #transformation de la matrice dans le format 0/1 pour utilisation de la matrice lors de la 
    # détermination des frontières
    
    for k in range(len(grid_bw)):
        for j in range(len(grid_bw[k])):
            if grid_bw[k][j] > 0 :
                grid_bw[k][j] = 0
            else :
                grid_bw[k][j] = 1
    
    # on renvoie une matrice avec des 0 et des 1
    return  grid_bw


#mise en place de la recherche de l'image à modifier avec l'explorateur
def browse_image():
    file_path = filedialog.askopenfilename(
        title="Choisir une image",
        filetypes=[("Fichiers image", "*.jpg *.jpeg *.png *.bmp *.tiff")],
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)


#mise en place des interfaces tkinter
root_image = tk.Tk()
root_image.title("Traitement d'image avec détection de zones")
root_image.geometry("500x300")

#chemin de l'image
label_path = tk.Label(root_image, text="Chemin de l'image :")
label_path.pack(pady=5)
entry_path = tk.Entry(root_image, width=50)
entry_path.pack(pady=5)
button_browse = tk.Button(root_image, text="Parcourir", command=browse_image)
button_browse.pack(pady=5)

# nom de la photo (pour renommer et enregistrer les images et grilles)
label_name = tk.Label(root_image, text="Nom de la photo (pour les sauvegardes) :")
label_name.pack(pady=5)
entry_name = tk.Entry(root_image, width=30)
entry_name.pack(pady=5)
entry_name.insert(0, "image")

# choix de la taille maximale de l'image et donc de la grille
label_size = tk.Label(root_image, text="Taille maximale d'un côté (en pixels) :")
label_size.pack(pady=5)
entry_size = tk.Entry(root_image, width=10)
entry_size.pack(pady=5)
entry_size.insert(0, "500")  

# bouton pour lancer le traitement de l'image
button_process = tk.Button(root_image, text="Lancer le traitement", command=process_image)
button_process.pack(pady=20)


def get_parameters():
    def submit():
        nonlocal k, n, color_choice, selected_function, speed
        k = float(k_entry.get())
        n = float(n_entry.get())
        color_choice = colormap_var.get()
        selected_function = function_var.get()
        speed = float(speed_entry.get())
        screen_parameter = float(screen_entry.get())
        root.destroy()

    root = tk.Toplevel(root_image)
    root.title("Paramètres de la simulation")

    # Activer le mode plein écran
    #root.attributes("-fullscreen", True)

    # Ajouter un bouton pour quitter le plein écran
    def exit_fullscreen():
        root.attributes("-fullscreen", False)

    tk.Button(root, text="Quitter le plein écran", command=exit_fullscreen).pack()

    rules_text = (
        "Bienvenue dans piCSelart.\n\n"
        "Voici les touches qui vous permettront de jouer.\n"
        "1. R : réinitialiser la map\n"
        "2. Espace : mettre le jeu en pause\n"
        "3. Clic-gauche (il faut que le jeu soit en pause) : Rajout de graine/frontière \n"
        "4. F : Permet d'enlever toutes les frontières. \n"
        "5. B: switcher entre mode graine/frontière. \n"
        "POUR LANCER : 'Valider' (avec vos paramètres), Rentrez une image -> 'lancer le Traitement'\n"
        "puis fermer la fenêtre"
    )

    tk.Label(root, text=rules_text, justify="left", wraplength=800, fg="blue").pack(pady=10)

    # Variables pour les entrées

    k = 1.0
    n = 1.0
    color_choice = "inferno"
    selected_function = ""
    speed = 0.01
    screen_parameter = 1080

    # Coefficient k
    tk.Label(root, text="Coefficient k").pack()
    k_entry = tk.Entry(root)
    k_entry.insert(0, "1.0")
    k_entry.pack()

    # Choix de n
    tk.Label(root, text="Coefficient n:").pack()
    n_entry = tk.Entry(root)
    n_entry.insert(0, "1.0")
    n_entry.pack()

    image_path = "picselartlogo.webp"  # Remplacez par le chemin de votre image WEBP
    image=Image.open(image_path)
    image_resized = image.resize((250, 250))

    # Convertir l'image redimensionnée en un format compatible avec Tkinter (PhotoImage)
    image_tk = ImageTk.PhotoImage(image_resized)

        # Placer l'image dans le coin supérieur droit
    root.update_idletasks()

    # Calculer la position pour le coin supérieur droit
    label_right = tk.Label(root, image=image_tk)
    label_right.place(x=root.winfo_width() - image_resized.width, y=0, anchor="ne")  # Coin supérieur droit

    # Choix de la colormap
    tk.Label(root, text="Choix de la colormap:").pack()
    colormap_var = StringVar(value="inferno")
    for cmap in ["inferno", "plasma", "viridis", "cividis", "magma", "cubehelix", "copper", "afmhot", "bone"]:
        Radiobutton(root, text=cmap, variable=colormap_var, value=cmap).pack(anchor=tk.W)
    # Variables pour les entrées

    # Choix de la fréquence de défilement
    tk.Label(root, text="Vitesse ou intervalle entre les générations (en secondes)").pack()
    speed_entry = tk.Entry(root)
    speed_entry.insert(0, "0.01")
    speed_entry.pack()
    
    #résolution de l'écran
    
    tk.Label(root, text="taille de la fenêtre ").pack()
    screen_entry = tk.Entry(root)
    screen_entry.insert(0, "1080")
    screen_entry.pack()

    # Choix de la fonction
    tk.Label(root, text="Choix de la fonction:").pack()
    function_var = StringVar(value=list(fonc_prop.keys())[0])
    for func_name in fonc_prop.keys():
        Radiobutton(root, text=func_name, variable=function_var, value=func_name).pack(anchor=tk.W)

    tk.Button(root, text="Valider", command=submit).pack()

    root.mainloop()
    return selected_function, k, n, speed, color_choice, screen_parameter

# Récupérer les paramètres
choix, k, n, speed, color_map, WINDOW_SIZE= get_parameters()
GRID_SIZE_1, GRID_SIZE_2 = len(grid_bw), len(grid_bw[0])
CELL_SIZE = WINDOW_SIZE // GRID_SIZE_1

# Implémentation de la fonction choisie
fonction_simul = fonc_prop[choix]

# Grille de jeu
grid = np.zeros((GRID_SIZE_1, GRID_SIZE_2), dtype=float)

# Grille de frontières (1: zone active, 0: zone bloquée)
boundaries = np.ones((GRID_SIZE_1, GRID_SIZE_2), dtype=int)


# Couleurs
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Dessin de la grille
def draw_grid(grid):
    """Dessine la grille et les cellules sur l'écran"""
    screen.fill(BLACK)
    colors = valeur_vers_couleur(grid, color_map)  # Convertit toute la grille en couleurs
    for x in range(GRID_SIZE_1):
        for y in range(GRID_SIZE_2):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # Si la cellule est dans les frontières, coloriez normalement
            if grid_bw[x, y] == 1:
                pygame.draw.rect(screen, colors[x, y], rect)
            else:
                pygame.draw.rect(screen, (206, 206, 206), rect)  # Couleur sombre pour les zones bloquées
            
            pygame.draw.rect(screen, GRAY, rect, 1)  # Dessine la grille

def draw_parameters():
    """Affiche les paramètres à droite de la simulation"""
    font = pygame.font.SysFont('Arial', 16)
    
    # Créer les lignes de texte
    lines = [
        f"Coefficient n: {n}",
        f"Coefficient k: {k}",
        f"Colormap: {color_map}",
        f"Fonction: {choix}",
        f"Vitesse: {speed} s",
        "espace pour mettre sur pause",
        "b switcher entre mode graine/frontière",
        "f pour effacer les frontières",
        "r pour effacer les jeux de la vie"
    ]
    
    # Affichage des lignes de texte
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (WINDOW_SIZE + 20, 30 + i * 30))

def main():
    global grid, grid_bw
    running = True
    paused = True
    drawing_boundaries = False  # Nouveau mode pour dessiner les frontières
    last_update_time = pygame.time.get_ticks()
    mouse_held = False  # État pour savoir si le bouton de la souris est enfoncé

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
                if drawing_boundaries:
                    grid_bw[x, y] = 0 if grid_bw[x, y] == 1 else 1
                else:
                    grid[x, y] = 1.0 if grid[x, y] == 0 else 0.0
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
            elif event.type == pygame.MOUSEMOTION and mouse_held:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
                if drawing_boundaries:
                    grid_bw[x, y] = 0
                else:
                    grid[x, y] = 1.0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Mettre en pause ou reprendre
                elif event.key == pygame.K_r:
                    grid = np.zeros((GRID_SIZE_1, GRID_SIZE_2), dtype=float)  # Réinitialiser la grille
                elif event.key == pygame.K_f:
                    grid_bw = np.ones((GRID_SIZE_1, GRID_SIZE_2), dtype=float)
                elif event.key == pygame.K_b:
                    drawing_boundaries = not drawing_boundaries  # Activer/désactiver le mode dessin de frontière

        current_time = pygame.time.get_ticks()
        if not paused and current_time - last_update_time >= speed * 1000:
            grid = generation(grid,grid_bw,fonction_simul,n,k)
            last_update_time = current_time

        draw_grid(grid)  # Dessiner la grille de simulation
        draw_parameters()  # Afficher les paramètres à droite
        pygame.display.flip()
        clock.tick(20) #C'est ici pr des raisons de fluidité, cela dicte la vitesse de calcul de pygames

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Initialisation de Pygame
    screen = pygame.display.set_mode((WINDOW_SIZE + 250, WINDOW_SIZE))  # Ajouter un espace à droite pour afficher les paramètres
    pygame.display.set_caption("Jeu de la Vie avec Couleurs et Paramètres")
    clock = pygame.time.Clock()
    main()