import numpy as np
import matplotlib.pyplot as plt


# Conversion des valeurs en couleurs
def valeur_vers_couleur(matrice, color_map):
    # Normaliser les valeurs de la matrice entre 0 et 1
    matrice = np.clip(matrice, 0, 1)
    
    # Utiliser le colormap de Matplotlib
    colormap = plt.get_cmap(color_map)
    colors = (colormap(matrice)[:, :, :3] * 255).astype(int)
    
    return colors