# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import (leastsq, curve_fit)


def mc(banda_i, error_i, banda_z, error_z, c_0):
    '''Realiza una simulación de Monte Carlo para obtener el intervalo de
    confianza del 95%'''
    Nmc = 10000
    cte = np.zeros(Nmc)
    pendiente = np.zeros(Nmc)
    for j in range(Nmc):
        r = np.random.normal(0, 1, size=len(banda_i))
        muestra_i = banda_i + error_i * r
        muestra_z = banda_z + error_z * r
        pendiente[j], cte[j] = np.polyfit(muestra_i, muestra_z, 1)

    pendiente = np.sort(pendiente)
    cte = np.sort(cte)
    limite_bajo_1 = pendiente[int(Nmc * 0.025)]
    limite_alto_1 = pendiente[int(Nmc * 0.975)]
    limite_bajo_2 = cte[int(Nmc * 0.025)]
    limite_alto_2 = cte[int(Nmc * 0.975)]
    print """El intervalo de confianza al
             95% para la pendiente es: [{}:{}]""".format(limite_bajo_1,
                                                         limite_alto_1)
    print """El intervalo de confianza al
             95% para el coef de posicion es: [{}:{}]""".format(limite_bajo_2,
                                                                limite_alto_2)

#Main

data = np.loadtxt("data/DR9Q.dat", usecols=(80, 81, 82, 83))
banda_i = data[:, 0] * 3.631
error_i = data[:, 1] * 3.631
banda_z = data[:, 2] * 3.631
error_z = data[:, 3] * 3.631
c = np.polyfit(banda_i, banda_z, 1)
print("recta : {}x + {}".format(c[0], c[1]))
intervalo_confianza = mc(banda_i, error_i, banda_z, error_z, c)