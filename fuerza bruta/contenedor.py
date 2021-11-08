import sys
import numpy as np
import time
from collections import defaultdict
start_time = time.time()
#------------------------------------------------------Entrada txt-----------------------------------------------------#

''' Abrir archivo recibe un archivo txt y almacena su contenido en la variable lineas'''


def abrir_archivo(input):
    lineas = [line.rstrip() for line in open(sys.argv[3])]
    return lineas


''' imprimir matriz, imprime los resultados de una matriz de una manera en que las filas y las columnas se vean representadas
de una manera estetica'''


def imprimir_matriz(matriz):
    print('\n'.join([''.join(['{:4}'.format(elemento) for elemento in fila])
                     for fila in matriz]))


#-------------------------------------------------------Mochila PD-----------------------------------------------------#

'''Distribuir entrada recibe los elementos de la entrada, y devuelve una lista con los elementos distribuidos en las
cantidades indicadas en la entrada por cada elemento.'''


def distribuir_entrada(elementos_ordenados):
    elementos_distribuidos = []
    i = 0
    while(i < len(elementos_ordenados)):
        j = 0
        while(j < elementos_ordenados[i][1]):
            elementos_distribuidos.append(elementos_ordenados[i])
            j += 1
        i += 1
    return elementos_distribuidos


'''Generador lista de ceros recibe un n, que va a ser el largo de la lista de ceros que se retorna.
Tomado del proyecto del Metodo Simplex y Gran M '''


def generador_lista_de_ceros(n):
    return n*[0]


#-------------------------------------------------------Mochila FB-----------------------------------------------------#
'''Mochila fuerza bruta, llama a todas las funciones necesarias para imprimir la solucion de la mochila, recibe el nombre del archivo
de entrada e imprime la solucion de la mochila.'''


def mochila_fuerza_bruta(input):
    entrada = abrir_archivo(input)
    i = 0
    while (i < len(entrada)):
        entrada[i] = [int(e) for e in entrada[i].split(',')]
        i += 1
    w = entrada[0][0]
    elementos = np.array(entrada[1:])
    elementos_ordenados = elementos[np.argsort(elementos[:, 0])]
    elementos_distribuidos = distribuir_entrada(elementos_ordenados)
    n = len(elementos_distribuidos)
    soluciones = []
    beneficio = mochila_recursiva(
        w, elementos_distribuidos, n, entrada, soluciones)
    respuesta = generador_lista_de_ceros(len(entrada)-1)
    for i in range(len(soluciones)):
        respuesta[entrada.index(soluciones[i])-1] += 1
    print("Mochila Fuerza Bruta")
    print(beneficio)
    for i in range(len(respuesta)):
        if respuesta[i] != 0:
            print(str(i+1)+","+str(respuesta[i]) + " # articulo " +
                  str(i+1) + " " + str(respuesta[i]) + " unidades")


'''Mochila recursiva, realiza la solucion de la mochila de una manera recursiva usando fuerza bruta, recibe el peso total que se tiene,
los elementos que se pueden utilizar, la cantidad de elementos, la entrada generada por el archivo txt, y una lista de soluciones
que esta llena de ceros al inicio para saber cuantas veces se uso un elemento'''


def mochila_recursiva(w, elementos_distribuidos, n, entrada, soluciones):
    lista_llevo = []
    lista_no_llevo = []
    if n == 0 or w == 0:
        return 0
    if (elementos_distribuidos[n-1][0] > w):
        return mochila_recursiva(w, elementos_distribuidos, n - 1, entrada, lista_no_llevo)

    lista_llevo.append(elementos_distribuidos[n-1].tolist())

    llevo = elementos_distribuidos[n-1][1] + mochila_recursiva(
        w - elementos_distribuidos[n-1][0], elementos_distribuidos, n - 1, entrada, lista_llevo)
    no_llevo = mochila_recursiva(
        w, elementos_distribuidos, n - 1, entrada, lista_no_llevo)

    resp = max(llevo, no_llevo)
    if (resp == llevo):
        for i in lista_llevo:
            soluciones.append(i)
    else:
        for i in lista_no_llevo:
            soluciones.append(i)

    return resp


#------------------------------------------------------- Main ---------------------------------------------------------#
'''Main es el controlador, que de acuerdo a la entrada, llama a los metodos indicados por el usuario en terminal'''


def main():
    if sys.argv[1] == "-h":
        print("El presente proyecto se ejecuta en terminal de la siguiente manera:")
        print("python3 contenedor.py PROBLEMA ALGORITMO ARCHIVO")
        print("En donde PROBLEMA, ALGORITMO y ARCHIVO representan lo siguiente: ")
        print("ALGORITMO valor de 1 2 3, indicando el algoritmo a usar, 1 fuerza bruta, 2 programación dinámica, 3 programación dinámica bottom-up")
        print("ARCHIVO indica el archivo de entrada donde el programa toma los parámetros del problema y procede a resolverlo con el algoritmo especificado.")
    else:
        if sys.argv[1] == "1":
            mochila_fuerza_bruta(sys.argv[1])
        else:
            print("Algoritmo no reconocido")


main()
print("--- %s segundos ---" % (time.time() - start_time))
