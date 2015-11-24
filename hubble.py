# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import (leastsq, curve_fit)
"""
Este codigo extrae los datos medidos de Hubble y deriva la constante de Hubble
incluyendo su intervalo de confianza al 95%, usando curve_fit.
"""

def f_hubble1(params, d):
    H = params
    return H * d
    
def f_hubble2(params, v):
    H = params
    return v / H

def funcion_a_minimizar1(H, d):
    params = H
    return f_hubble1(params, d)
    
def funcion_a_minimizar2(H, v):
    params = H
    return f_hubble2(params, v)
    
def bootstrap(data, H_0):
    ''' Simulación de bootstrap para encontrar el
    intervalo de  confianza (95%)'''
    N, N1 = data.shape
    N_boot = 10000
    H = np.zeros(N_boot)
    for i in range(N_boot):
        s = np.random.randint(low=0, high=N, size=N)
        fake_data = data[s][s]
        d = fake_data[:, 0]
        v = fake_data[:, 1]
        a_optimo1, a_covarianza1 = curve_fit(funcion_a_minimizar1,
                                               d, v, 2)
        a_optimo2, a_covarianza2 = curve_fit(funcion_a_minimizar2,
                                               v, d, 2)
        a_promedio = (a_optimo2 + a_optimo1) / 2
        H[i] = a_promedio
    H = np.sort(H)
    limite_bajo = H[int(N_boot * 0.025)]
    limite_alto = H[int(N_boot * 0.975)]
    print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo,
                                                                limite_alto)
        
    
#Main

hubble = np.loadtxt("data/hubble_original.dat")
d = hubble[:, 0]
v = hubble[:, 1]

a_optimo1, a_covarianza1 = curve_fit(funcion_a_minimizar1, d, v, 2)
a_optimo2, a_covarianza2 = curve_fit(funcion_a_minimizar2, v, d, 2)
a_promedio = (a_optimo1 + a_optimo2) / 2
H_0 = a_promedio
print ("H_0 = " + str(H_0))

intervalo_confianza = bootstrap(hubble, H_0)