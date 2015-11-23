# -*- coding: utf-8 -*-
"""
Este codigo extrae los datos medidos de Hubble y deriva la constante de Hubble
incluyendo su intervalo de confianza al 95%
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

hubble = np.loadtxt("C:/Users/Administrador/09Tarea/data/hubble_original.dat")
print hubble