# -*- coding: UTF-8 -*-
import sys
import time
import numpy as np
import pandas as pd
import igraph as ig

def solucion_calcular_costo(n, s, c):
    aux = c[s[n-1]][s[0]]     
    for i in range(n-1):
        aux += c[s[i]][s[i+1]]
    return aux

def inicializarSolucionInicial(cant_ciudades):
    SolucionInicial = np.array([])
    for i in range(0, cant_ciudades):
        SolucionInicial = np.arange(0, cant_ciudades)
        np.random.shuffle(SolucionInicial)
    return SolucionInicial

def inicializarMatrizFeromona(matriz,x,y, initw):
    m_feromona = np.full((x,y),initw,dtype=float)
    return m_feromona

def assignHormigasAColonias(cant_hormigas, cant_ciudades):
    xyHormigasAColonias = np.full((cant_hormigas, cant_ciudades), 0)
    for i in range(0, cant_hormigas):
        xyHormigasAColonias[i][0] = np.random.randint(0, cant_ciudades-1)
    return xyHormigasAColonias

if len(sys.argv) == 8:
    np.set_printoptions(threshold=sys.maxsize)
    np.set_printoptions(suppress=True)
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
    """ print(sys.argv[0], " ", seed, " ", n, " ", iter, " ", alpha, " ", beta, " ", q0, " ", data) """
    xy_coordenadas = pd.read_table(data, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
    cant_variables = xy_coordenadas.shape[0]
    """ print(xy_coordenadas) """
    """ print(cant_variables) """
    xy_distancia = np.full((cant_variables, cant_variables), fill_value=-1, dtype=float)
    for i in range(cant_variables-1):
        for j in range(i+1, cant_variables):
            xy_distancia[i][j] = np.sqrt(np.sum(np.square(xy_coordenadas[i]-xy_coordenadas[j])))
            xy_distancia[j][i] = xy_distancia[i][j]
    xy_distancia = np.around(xy_distancia, decimals=4)
    """ print("Matriz distancia:") """
    """ print(xy_distancia) """
    xy_heuristica = 1/xy_distancia
    """ print("Matríz heurística",xy_heuristica) """
    # Uso de algoritmo
    # Matriz feromóna
    matriz_feromona = inicializarMatrizFeromona(xy_heuristica, cant_variables, cant_variables, -1)
    print("Matríz feromóna: ", matriz_feromona)
    i = 1
    # Solución inicial
    sol_inic = inicializarSolucionInicial(cant_variables)
    calc_fitness = solucion_calcular_costo(cant_variables, sol_inic, xy_distancia)
    """ print("Costo de la solución: ", calc_fitness) """
    matriz_transicion = np.array([])
    matriz_feromonainit = np.array([])
    matriz_feromonainit = np.append(matriz_feromonainit, 1/calc_fitness)
    while i <= iter:
        # Matriz de hormigas
        print("Hormigas a Colonia: ", assignHormigasAColonias(n, cant_variables))
        for i in range(0, cant_variables):
            for j in range(0, n):
                nq0 = np.random.rand()
                if nq0 <= q0:
                    
                    print(matriz_feromonainit)
                else:
                    print("xd")
        print("Primera solución: ", inicializarSolucionInicial(cant_variables))
        print("Matriz de transicion: ", matriz_transicion)
        i += 1
    
else:
    print("Porfavor reingrese los parámetros de manera correcta.")
    print("Parametros a ingresar: 'Nombre del archivo' 'Semilla' 'Tamaño de la colonia' 'Cantidad de iteraciones' 'Factor de evaporación' 'Paso de heurística' 'Probabilidad limite' ")
    # .\berlin52.py 0 10 100 0.1 2.5 0.9 berlin52.tsp.txt
    sys.exit(0)
