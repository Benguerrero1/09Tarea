# -*- coding: utf-8 -*-
"""
Este codigo extrae los datos medidos de Hubble y deriva la constante de Hubble
incluyendo su intervalo de confianza al 95%
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def f_hubble(params, d):
    H = params
    return H * d

def funcion_a_aminimizar(H, d):
    params = H
    return f_hubble(params, d)

hubble = np.loadtxt("data/hubble_original.dat")
d = hubble[:, 0]
v = hubble[:, 1]


