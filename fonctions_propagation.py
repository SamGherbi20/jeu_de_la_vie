import numpy as np
from scipy.special import *

def sinus_poly(n, k, x):
    return np.sin(k*(x**n))

def cos_att(n, k, x):
    return np.cos(k*x)*np.exp(-n*x)

def Diri(n, k, x):
    return np.sin((n + 1/2)*x)/(np.sin(x/2) + 0.00001)

def Bess(n, k, x):
    return jn(n, x)

def cos_exp_sin(n, k, x):
    return np.cos(n*x)*np.exp(np.sin(k*x))

def cos_sin(n, k, x):
    return np.cos(k*x)*np.sin(n*x)

def cos_sin(n, k, x):
    return np.cos(k*x)*np.sin(n*x)

def exp(n, k, x):
    return (x**n)*np.exp(-k*x)

fonc_prop = {'sin(k*(x**n))': sinus_poly, 'Dirichlet n-ieme (mettre n = 50 par défaut)': Diri, 'Bessel n-ieme (mettre n=4 par défaut)': Bess, 'cos(kx)sin(nx)': cos_sin, 'x^n * exp(-kx)': exp}