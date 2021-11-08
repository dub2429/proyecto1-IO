import numpy as np
import time
import matplotlib.pyplot as plt
import random
import pandas as pd
import functools


def top_down(valor, peso, capacidad):
    #E: valor[i] es el valor del item i y el peso[i] es el peso del item i
    #para 1 <= i <= n donde n es el numero de items
    #Capacidad es el peso maximo.
    #S: Devuelve el valor máximo de los artículos que no supere la capacidad.

    n = len(valor)-1
 
    # m[i][w] almacenará el valor máximo que se puede obtener con una capacidad 
    # máxima de p (pesos) utilizando solo los primeros i elementos
    m = [[-1]*(capacidad + 1) for _ in range(n + 1)]
 
    return top_down_aux(valor, peso, m, n, capacidad)
 
 
def top_down_aux(valor, peso, m, i, p):
    #E: Los items, el peso de los items, la matriz de los calculos, cantidad de items, la capacidad de la mochila
    # Funcion auxuliar de top dpwn
    # m[i][w] almacenará el valor máximo que se puede obtener con una capacidad 
    # máxima de p (pesos) utilizando solo los primeros i elementos
    # esta función llena m como subproblemas más pequeños necesarios para calcular m[i][w] 
    # que esten ya resueltos.
 
    # valor[i] es el valor del item i y el peso[i] es el peso del item i
    # para 1 <= i <= n donde n es el numero de items
    
    #S: Devuelve el valor máximo de los primeros i elementos posibles con el peso <= p.
    
    if m[i][p] >= 0:
        return m[i][p]
 
    if i == 0:
        q = 0
    elif peso[i] <= p:
        q = max(top_down_aux(valor, peso,m, i - 1 , p - peso[i])+ valor[i],top_down_aux(valor, peso,m, i - 1 , p))
    else:
        q = top_down_aux(valor, peso,m ,i - 1, p)
        
    m[i][p] = q
    return q



valor = [20, 50, 60, 62, 40]
valor.sort()   #Se debe enviar los valores de los items ordenado ascendentemente
valor.insert(0, None)  #de modo que el valor del i-ésimo artículo está en valor [i]
peso = [5, 15, 10, 10, 8]
peso.insert(0, None) #de modo que el peso del i-ésimo artículo sea el peso [i]

respuesta = top_down(valor,peso,30)
print('El valor máximo de los artículos que se pueden llevar: ', respuesta)




