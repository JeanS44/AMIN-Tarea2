# -*- coding: UTF-8 -*-
import sys
import time
import numpy as np
import pandas as pd
import igraph as ig


if len(sys.argv) == 8:
    seed = int(sys.argv[1])
    if seed>=0:
        np.random.seed(seed)
    else:
        seed = np.random.seed()
    n = int(sys.argv[2])
    iter = int(sys.argv[3])
    alpha = float(sys.argv[4])
    beta = float(sys.argv[5])
    q0 = float(sys.argv[6])
    data = sys.argv[7]
    print(sys.argv[0], " ", seed, " ", n, " ", iter, " ", alpha, " ", beta, " ", q0, " ", data)
    xy_coordenadas = pd.read_table(data, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
    cant_variables = xy_coordenadas.shape[0]
    print(xy_coordenadas)
    print(cant_variables)
    xy_distancia = np.full((cant_variables, cant_variables), fill_value=-1, dtype=float)
    print(xy_distancia)
    for i in range(cant_variables-1):
        for j in range(i+1, cant_variables):
            xy_distancia[i][j] = np.sqrt(np.sum(np.square(xy_coordenadas[i]-xy_coordenadas[j])))
            xy_distancia[j][i] = xy_distancia[i][j]
    xy_distancia = np.around(xy_distancia, decimals=4)
    print(xy_distancia)

    xy_heuristica = 1/xy_distancia
    print(xy_heuristica)
else:
    print("Porfavor reingrese los parámetros de manera correcta.")
    print("Parametros a ingresar: 'Nombre del archivo' 'Semilla' 'Tamaño de la colonia' 'Cantidad de iteraciones' 'Factor de evaporación' 'Paso de heurística' 'Probabilidad limite' ")
    # .\berlin52.py 0 10 100 0.1 2.5 0.9 berlin52.tsp.txt
    sys.exit(0)
