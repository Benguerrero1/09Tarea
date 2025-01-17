# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import (leastsq, curve_fit)

'''
Este código genera la linea recta que mejor modela la relacion entre las 
bandas i y z, incluyendo los intervalos de confianza al 95% usando MC,
a partir de los datos en data/DR9Q.dat 
'''

def graficar(banda_i, error_i, banda_z, error_z, c):
    '''Grafica los datos originales con sus errores asociados,
    junto con el ajuste lineal polyfit'''
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.errorbar(banda_i, banda_z, xerr=error_i, yerr=error_z, fmt="o",
                 label="Datos originales con error")
    x = np.linspace(-100, 500, 600)
    ax1.plot(x, c[1] + x*c[0], color="r", label="ajuste lineal")
    ax1.set_title("Datos originales y ajuste lineal")
    ax1.set_xlabel("Flujo banda i [$10^{-6}Jy$]")
    ax1.set_ylabel("Flujo banda z [$10^{-6}Jy$]")
    plt.legend(loc=2)
    plt.savefig("DR9Q.jpg")

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
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.hist(pendiente, bins=30)
    ax2.axvline(c[0], color='r', label="valor obtenido")
    plt.legend(loc=2)
    ax2.set_title("Simulacion de Montecarlo (pendientes)")
    ax2.set_xlabel("pendiente [adimensional]")
    ax2.set_ylabel("frecuencia")
    plt.savefig("mc_1.jpg")

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    ax3.hist(cte, bins=30)
    ax3.axvline(c[1], color='r', label="valor obtenido")
    plt.legend(loc=2)
    ax3.set_title("Simulacion de Montecarlo (coef de posicion)")
    ax3.set_xlabel("coef de posicion [adimensional]")
    ax3.set_ylabel("frecuencia")
    plt.savefig("mc_2.jpg")
    
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

datos = np.loadtxt("data/DR9Q.dat", usecols=(80, 81, 82, 83))
banda_i = datos[:, 0] * 3.631
error_i = datos[:, 1] * 3.631
banda_z = datos[:, 2] * 3.631
error_z = datos[:, 3] * 3.631
c = np.polyfit(banda_i, banda_z, 1)
print("recta : {}x + {}".format(c[0], c[1]))
intervalo_confianza = mc(banda_i, error_i, banda_z, error_z, c)
graficar(banda_i, error_i, banda_z, error_z, c)
plt.show()