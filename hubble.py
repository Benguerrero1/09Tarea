# -*- coding: utf-8 -*-
"""
Este codigo extrae los datos medidos de Hubble y deriva la constante de Hubble
incluyendo su intervalo de confianza al 95%
"""
from scipy.optimize import (leastsq, curve_fit)
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def f_hubble1(params, d):
    H = params
    return H * d
    
def f_hubble2(params, v):
    H = params
    return H / v

def funcion_a_minimizar1(H, d):
    params = H
    return f_hubble1(params, d)
    
def funcion_a_minimizar2(H, v):
    params = H
    return f_hubble2(params, v)

hubble = np.loadtxt("data/hubble_original.dat")
d = hubble[:, 0]
v = hubble[:, 1]

a_optimo1, a_covarianza1 = curve_fit(funcion_a_minimizar1, d, v, 2)
a_optimo2, a_covarianza2 = curve_fit(funcion_a_minimizar2, d, v, 2)
a_promedio = (a_optimo1 + a_optimo2) / 2