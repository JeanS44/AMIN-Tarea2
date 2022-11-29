# -*- coding: UTF-8 -*-
import sys
import time
import numpy as np
import pandas as pd
import igraph as ig
import math

def solucionCalcularCosto(n, s, c):
    aux = c[s[n-1]][s[0]]     
    for i in range(n-1):
        aux += c[s[i]][s[i+1]]
    return aux

def determinarRuleta(TxN):
    x = np.full_like(TxN, 0, dtype=np.longdouble)
    sumaTxN = np.sum(TxN)
    for i in range(len(TxN)):
        x[i] = TxN[i]/sumaTxN
    pos = np.where(np.random.uniform(min(x), max(x), len(TxN)) < x)[0]
    aux = 0
    for i in pos:
        if x[i] > aux:
            j0 = i
            aux = x[i]
    return j0

def fixMatriz(m):
    for i in range(52):
        for j in range(52):
            if m[i][j] == -1:
                m[i][j] = 0
    return m

def inicializarSolucionInicial(cant_ciudades):
    SolucionInicial = np.array([])
    for i in range(0, cant_ciudades):
        SolucionInicial = np.arange(0, cant_ciudades)
        np.random.shuffle(SolucionInicial)
    return SolucionInicial

def inicializarMatrizFeromona(x, y, initw):
    m_feromona = np.full((x, y), initw, dtype=np.longdouble)
    return m_feromona

def asignarHormigasAlMapa(cant_hormigas, cant_ciudades, m_memoria):
    xyHormigasAColonias = np.full((cant_hormigas, cant_ciudades), 0)
    for i in range(0, cant_hormigas):
        randomInt = np.random.randint(0, cant_ciudades-1)
        xyHormigasAColonias[i][0] = randomInt
        m_memoria[i][randomInt] = 1
    return xyHormigasAColonias

def matrizTransicion(m_colonia, m_heuristica, m_feromona, m_memoria, b):
    HxV = np.full_like(m_memoria, 0, dtype=np.longdouble)
    i = 0
    while(i < len(m_heuristica)):
        if m_memoria[i] == 0:
            # Aquí se calculará la multiplicación entre la Matríz de heuristica
            # con la matríz de feromóna
            Tij = m_feromona[m_colonia][i]
            Nij = m_heuristica[m_colonia][i]
            NijpowB = math.pow(Nij, b)
            TxN = Tij * NijpowB
            HxV[i] = TxN
        i += 1
    return HxV

if len(sys.argv) == 8:
    # Asignación de parámetros.
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
    print(sys.argv[0], " Seed:", seed, " n:", n, " Iteraciones:", iter, " Alpha:", alpha, " Beta:", beta, " q0:", q0, " Name:", data)
    # Término de asignación de parámetros.

    # Extracción de coordenadas en el archivo 'berlin52.tsp.txt'.
    xy_coordenadas = pd.read_table(data, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
    cant_ciudades = xy_coordenadas.shape[0]
    # Termino de extracción de coordenadas del archivo.

    # Se forma la matríz de distancia y heurística.
    xy_distancia = np.full((cant_ciudades, cant_ciudades), fill_value=-1, dtype=float)
    for i in range(cant_ciudades-1):
        for j in range(i+1, cant_ciudades):
            xy_distancia[i][j] = np.sqrt(np.sum(np.square(xy_coordenadas[i]-xy_coordenadas[j])))
            xy_distancia[j][i] = xy_distancia[i][j]
    xy_distancia = fixMatriz(xy_distancia)
    xy_distancia = np.around(xy_distancia, decimals=4)
    xy_heuristica = 1/xy_distancia
    # Término de la formación de la matríz de distancia y heurística.
    # Uso de algoritmo
    i = 0
    # Solución inicial, generamos un arreglo desde 0 hasta la cant_ciudades-1 y se procede a calcular el fitness de esta solución.
    solucion_inicial = inicializarSolucionInicial(cant_ciudades)
    calcular_fitness = solucionCalcularCosto(cant_ciudades, solucion_inicial, xy_distancia)
    matriz_feromona = inicializarMatrizFeromona(cant_ciudades, cant_ciudades, 1/(calcular_fitness*cant_ciudades))
    matriz_memoria = np.zeros((n, cant_ciudades), dtype=int)
    matriz_colonia = asignarHormigasAlMapa(n, cant_ciudades, matriz_memoria)
    print(matriz_colonia)
    """ print("Matríz feromóna: ", matriz_feromona) """
    """ print("Costo de la solución: ", calcular_fitness) """
    # Término de la solución inicial.
    
    j0 = 0
    while i < iter:
        # Matriz de hormigas
        """ print("Hormigas a Colonia: ", asignarHormigasAlMapa(n, cant_ciudades)) """
        for i in range(1, cant_ciudades):
            for j in range(n):
                nq0 = np.random.rand()
                mT = matrizTransicion(matriz_colonia[j][i-1], xy_heuristica, matriz_feromona, matriz_memoria[j], beta)
                print(nq0)
                print("mT", len(mT))
                if nq0 <= q0:
                    j0 = np.random.choice(np.where(mT == mT.max())[0])
                    print("j0 1", j0, j, i)
                else:
                    j0 = determinarRuleta(mT)
                    print("j0 2", j0, j, i)
        i += 1
else:
    print("Porfavor reingrese los parámetros de manera correcta.")
    print("Parametros a ingresar: 'Nombre del archivo' 'Semilla' 'Tamaño de la colonia' 'Cantidad de iteraciones' 'Factor de evaporación' 'Paso de heurística' 'Probabilidad limite' ")
    # .\berlin52.py 0 10 100 0.1 2.5 0.9 berlin52.tsp.txt
    sys.exit(0)
