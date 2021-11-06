import numpy as np
import time
import matplotlib.pyplot as plt
import random
import pandas as pd
import functools


def top_down(valor, peso, capacidad):
    """Devuelve el valor máximo de los artículos que no supere la capacidad.
 
    valor[i] is the valor of item i and weight[i] is the weight of item i
    for 1 <= i <= n where n is the number of items.
 
    capacidad is the maximum weight.
    """
    n = len(valor)-1
 
    # m[i][w] will store the maximum valor that can be attained with a maximum
    # capacidad of w and using only the first i items
    m = [[-1]*(capacidad + 1) for _ in range(n + 1)]
 
    return top_down_aux(valor, peso, m, n, capacidad)
 
 
def top_down_aux(valor, peso, m, i, w):
    """Return maximum valor of first i items attainable with weight <= w.
 
    m[i][w] will store the maximum valor that can be attained with a maximum
    capacidad of w and using only the first i items
    This function fills m as smaller subproblems needed to compute m[i][w] are
    solved.
 
    valor[i] is the valor of item i and weight[i] is the weight of item i
    for 1 <= i <= n where n is the number of items.
    """
    if m[i][w] >= 0:
        return m[i][w]
 
    if i == 0:
        q = 0
    elif peso[i] <= w:
        q = max(top_down_aux(valor, peso,m, i - 1 , w - peso[i])+ valor[i],top_down_aux(valor, peso,m, i - 1 , w))
    else:
        q = top_down_aux(valor, peso,m, i - 1 , w)
    m[i][w] = q
    imprimir_tabla(m)
    return q

def imprimir_tabla(matriz):
    #E: La matriz para imprimir la tabla
    #S: La tabla impresa
    for i in range(0,len(matriz)):
        print(matriz[i])
 
'''
n = int(input('Enter number of items: '))
valor = input('Enter the valors of the {} item(s) in order: '
              .format(n)).split()
valor = [int(v) for v in valor]
valor.insert(0, None) # so that the valor of the ith item is at valor[i]
peso = input('Enter the positive weights of the {} item(s) in order: '
               .format(n)).split()
peso = [int(w) for w in peso]
peso.insert(0, None) # so that the weight of the ith item is at weight[i]
capacidad = int(input('Enter maximum weight: '))

'''


#ans = top_down(valor, peso, capacidad)

valor = [20, 50, 60, 62,40]
valor.sort()
valor.insert(0, None)
peso = [5, 15, 10, 10, 8]
peso.insert(0, None) 

ans = top_down(valor,peso,30)
print('The maximum valor of items that can be carried:', ans)




