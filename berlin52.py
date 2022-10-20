# -*- coding: UTF-8 -*-
import sys
import time
import numpy as np
import pandas as pd
import igraph as ig


if len(sys.argv) == 7:
    semilla = int(sys.argv[1])
    if semilla>=0:
        np.random.seed(semilla)
    else:
        semilla = np.random.seed()
    tamanoColonia = int(sys.argv[2])
    cantidadIteraciones = int(sys.argv[3])
    factorEvaporacion = int(sys.argv[4])
    pesoHeuristica = float(sys.argv[5])
    valorProbabilidadLimite = float(sys.argv[6])
    print("xd")
else:
    print("Porfavor reingrese los parámetros de manera correcta.")
    print("Parametros a ingresar: 'Nombre del archivo' 'Semilla' 'Tamaño de la colonia' 'Cantidad de iteraciones' 'Factor de evaporación' 'Paso de heurística' 'Probabilidad limite' ")
    sys.exit(0)
