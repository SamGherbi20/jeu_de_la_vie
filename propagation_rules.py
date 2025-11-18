import numpy as np
from scipy.signal import convolve2d

def neighbors_with_boundaries(universe,grid_arg):
    """
    Calcule les voisins tout en prenant en compte les frontières.
    Si une cellule a des voisins hors des frontières, ces voisins sont ignorés.
    """
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    voisins = convolve2d(universe > 0, kernel, mode='same', boundary='wrap')
    
    # Masque les voisins selon les frontières
    valid_mask = convolve2d(grid_arg, kernel, mode='same', boundary='wrap')
    voisins[valid_mask < kernel.sum()] = 0  # Réduire les voisins si frontière
    return voisins


def generation(uni,grid_arg,func,n,k):
    vois = neighbors_with_boundaries(uni,grid_arg)
    new_grid = func(n, k, vois)
    # Clamp les valeurs pour rester dans l'intervalle [0, 1]
    new_grid = np.clip(new_grid, 0, 1)
    # Appliquer les frontières
    new_grid[grid_arg == 0] = 0
    return new_grid