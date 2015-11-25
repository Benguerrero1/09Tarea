# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import (leastsq, curve_fit)
"""
Este codigo extrae los datos medidos y deriva la constante de Hubble
incluyendo su intervalo de confianza al 95%, usando curve_fit.
"""
def graficar(d, v, H1, H2, H_promedio):
    ''' 
    Recibe el arreglo de distancias y velocidades y las grafica.
    '''
    ax, fig = plt.subplots()
    plt.scatter(d, v, label="Datos originales")
    fig.plot(d, f_hubble1(H1, d), label="H0 tal que V=D*H")
    fig.plot(f_hubble2(H2, v), v, label="H0 tal que V/H = D")
    fig.plot(d, H_promedio * d, label="H promedio")
    fig.set_title("Datos modernos y ajuste lineal")
    fig.set_xlabel("Distancia [Mpc]")
    fig.set_ylabel("Velocidad [Km/s]")
    plt.legend(loc=2)
    plt.savefig("SNIa.jpg")

def f_hubble1(params, d):
    H = params
    return H * d
    
def f_hubble2(params, v):
    H = params
    return v / H

def funcion_a_minimizar1(d, H):
    params = H
    return f_hubble1(params, d)
    
def funcion_a_minimizar2(v, H):
    params = H
    return f_hubble2(params, v)
    
def bootstrap(data, H_0):
    ''' 
    Simulación de bootstrap para encontrar el
    intervalo de  confianza (95%)
    '''
    N, N1 = data.shape
    N_boot = 10000
    H = np.zeros(N_boot)
    for i in range(N_boot):
        s = np.random.randint(low=0, high=N, size=N)
        fake_data = data[s][s]
        v = fake_data[:, 0]
        d = fake_data[:, 1]
        a_optimo1, a_covarianza1 = curve_fit(funcion_a_minimizar1,
                                               d, v, 2)
        a_optimo2, a_covarianza2 = curve_fit(funcion_a_minimizar2,
                                               v, d, 2)
        a_promedio = (a_optimo2 + a_optimo1) / 2
        H[i] = a_promedio
    fig2, ax2 = plt.subplots()
    plt.hist(H, bins=30)
    plt.axvline(H_0, color='r', label="valor obtenido de H0")
    plt.legend(loc=2)
    ax2.set_title("Simulacion bootstrap")
    ax2.set_xlabel("H [Km/s /Mpc]")
    ax2.set_ylabel("frecuencia")
    plt.savefig("bootstrap_2.jpg")
    H = np.sort(H)
    limite_bajo = H[int(N_boot * 0.025)]
    limite_alto = H[int(N_boot * 0.975)]
    print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo,
                                                                limite_alto)
        
    
#Main

datos = np.loadtxt("data/SNIa.dat", usecols=(1,2))
v = datos[:, 0]
d = datos[:, 1]

a_optimo1, a_covarianza1 = curve_fit(funcion_a_minimizar1, d, v, 2)
a_optimo2, a_covarianza2 = curve_fit(funcion_a_minimizar2, v, d, 2)
a_promedio = (a_optimo1 + a_optimo2) / 2
H_0 = a_promedio
print ("H_0 = " + str(H_0))

graficar(d, v, a_optimo1, a_optimo2, a_promedio)
intervalo_confianza = bootstrap(datos, H_0)
plt.show()