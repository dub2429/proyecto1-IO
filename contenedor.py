import numpy as np
import time
import matplotlib.pyplot as plt
import random
import pandas as pd
import datetime
from itertools import combinations

#Falta agregar una fila de ceros al inicio

def BottomUp(pesos, beneficios,capacidad):
    matrizCeros = np.zeros((len(pesos), capacidad+1),dtype=int)
    k = 0
    
    
    
    while k < len(pesos):
        for w in range(capacidad+1):
            if pesos[k] > w:
               matrizCeros[k,w]=matrizCeros[k-1,w]
            else:
                if beneficios[k]+matrizCeros[k-1,w-pesos[k]]> matrizCeros[k-1,w]:
                    matrizCeros[k,w]=beneficios[k]+matrizCeros[k-1, w-pesos[k]]
                else:
                    matrizCeros[k,w]=matrizCeros[k-1,w]
        k+=1  
             

    diccionario = {}
    for i in range(len(matrizCeros[0])):
        nuevaColumna = "C" + str(i)
        columnaTemp = [0]
        columnaTemp.extend(matrizCeros[:,i])
       #print(matrizCeros[:i])
        diccionario[nuevaColumna] = columnaTemp
    #print(diccionario)
    


    df = pd.DataFrame(data=diccionario)
    print(df)
    #print("p "+str(pesos))
    print("El resultado del Bottom up es: "+str((matrizCeros[-1,-1])))
    for i in range(len(beneficios)):
        comb = combinations(beneficios, i)
        for j in list(comb):
            if sum(j) == matrizCeros[-1,-1]:
                #print(j)
                listaIndices = []
                for k in range(len(j)):
                    listaIndices.append(str(beneficios.index(j[k])+1))
                #print(beneficios)
                print("Los artículos son: " + ','.join(listaIndices))
               # print("Encontrado")
                break
            #print(j)
def top_down(valor, peso, capacidad,valorCopia):
    #E: valor[i] es el valor del item i y el peso[i] es el peso del item i
    #para 1 <= i <= n donde n es el numero de items
    #Capacidad es el peso maximo.
    #S: Devuelve el valor máximo de los artículos que no supere la capacidad.

    n = len(valor)-1
 
    # m[i][w] almacenará el valor máximo que se puede obtener con una capacidad 
    # máxima de p (pesos) utilizando solo los primeros i elementos
    m = [[-1]*(capacidad + 1) for _ in range(n + 1)]
    
    return top_down_aux(valor, peso, m, n, capacidad,valorCopia)
 

def top_down_aux(valor, peso, m, i, w,valorCopia):
    #E: Los items, el peso de los items, la matriz de los calculos, cantidad de items, la capacidad de la mochila
    # Funcion auxuliar de top dpwn
    # m[i][w] almacenará el valor máximo que se puede obtener con una capacidad 
    # máxima de p (pesos) utilizando solo los primeros i elementos
    # esta función llena m como subproblemas más pequeños necesarios para calcular m[i][w] 
    # que esten ya resueltos.
 
    # valor[i] es el valor del item i y el peso[i] es el peso del item i
    # para 1 <= i <= n donde n es el numero de items
    
    #S: Devuelve el valor máximo de los primeros i elementos posibles con el peso <= p.

    global resultadoTop
    global articulos
    if m[i][w] >= 0:
        return m[i][w]
 
    if i == 0:
        q = 0
    elif peso[i] <= w:
        q = max(top_down_aux(valor, peso,m, i - 1 , w - peso[i],valorCopia)+ valor[i],top_down_aux(valor, peso,m, i - 1 , w,valorCopia))
    else:
        q = top_down_aux(valor, peso,m, i - 1 , w,valorCopia)
    m[i][w] = q
    resultadoTop = m
    
    for i in range(len(valorCopia)):
        comb = combinations(valorCopia, i)
        for j in list(comb):
            if sum(j) == q:
                #print(j)
                listaIndices = []
                for k in range(len(j)):
                    listaIndices.append(str(valorCopia.index(j[k])+1))
                #print(beneficios)
                articulos = "Los artículos son: " + ','.join(listaIndices)
                #print("Los artículos son: " + ','.join(listaIndices))
               # print("Encontrado")
                break
            #print(j)
    
    return q

def imprimir_tabla(matriz):
    df1 = pd.DataFrame(matriz)
    print(df1)

inicio = time.perf_counter()
n = 1

start = time.perf_counter()
for i in range(n):
    valor = [20, 50, 60, 62, 40]
    valorC = valor.copy()
    valor.sort() #Se debe enviar los valores de los items ordenado ascendentemente
    #valor2 = [3,4,5,6]
    #valor2.sort()
    #valor2.insert(0, None)  #de modo que el valor del i-ésimo artículo está en valor [i]
    #peso2 = [2,3,4,5]
    peso = [5, 15, 10, 10, 8]
    peso.insert(0, None) #de modo que el peso del i-ésimo artículo sea el peso [i] 

    respuesta = top_down(valor,peso,30,valorC)
    print('El valor máximo de los artículos que se pueden llevar: ', respuesta)
    imprimir_tabla(resultadoTop)
    print(articulos)

end = time.perf_counter()
print("El tiempo de ejecución calculado es en TopDown:")
print(datetime.timedelta(seconds= end  - start))

tiempoTopDown = float("{:.6f}".format((end - start)/60))






start = time.perf_counter()
for i in range(n):
   # valorA = [3,4,5,6]
   # mochila([2,3,4,5],valorA,5)
    valorA = [20, 50, 60, 62, 40]
    BottomUp([5,15,10,10,8],valorA,30)


    
end = time.perf_counter()
print("El tiempo de ejecución calculado es:")
print(datetime.timedelta(seconds= end  - start))
final = time.perf_counter()
print(datetime.timedelta(seconds=final - inicio))

tiempoBottomUp = float("{:.6f}".format((end - start)/60))
lista=[tiempoBottomUp,tiempoTopDown]
#lista = []
#for i in range(4):
#    lista.append(tiempoBottomUp)#Quitar el random, acá se deben meter las pruebas
#
#listaTop = []
#for i in range(4):
#    listaTop.append(tiempoTopDown)
#
#
#
##Si se quiere graficar otro, nada más se debe agregar un .plot
#
#fig, ax = plt.subplots()
#ejercicio = ['E1', 'E2', 'E3', 'E4']
##lista2 = [1,2.6,3.3,0.8564]
#tiempo = {'BottomUp': lista, 'TopDown': listaTop}#,'prueba2': lista2 }#Para agregar otro 
#
##ax.plot(ejercicio, tiempo['BottomUp'])
#ax.set_title('BottomUp', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
#ax.set_xlabel("Ejercicio", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
#ax.set_ylabel("Tiempo ejecución",fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
#ax.set_ylim([-1,10])
#ax.set_yticks(range(0, 1))
#ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
#plt.plot(ejercicio, lista, color='#a12424', linestyle='--', marker='o')
#plt.plot(ejercicio, listaTop, color='green', linestyle='--', marker='o')
##plt.plot(ejercicio, lista2, color='green', linestyle='--', marker='o')#Para agregar otro 
#for i, txt in enumerate(lista):
#    ax.annotate(txt, (ejercicio[i], lista[i]))
#
#for i, txt in enumerate(listaTop):#Para agregar otro 
#   ax.annotate(txt, (ejercicio[i], listaTop[i]))#Para agregar otro 
##for i, txt in enumerate(lista2):#Para agregar otro 
#   #ax.annotate(txt, (ejercicio[i], lista2[i]))#Para agregar otro 
#plt.show()




#Si se quiere graficar otro, nada más se debe agregar un .plot

fig, ax = plt.subplots()
ejercicio = ['BU', 'TD']
#lista2 = [1,2.6,3.3,0.8564]
tiempo = {'Promedios': lista}#,'prueba2': lista2 }#Para agregar otro 

#ax.plot(ejercicio, tiempo['BottomUp'])
ax.set_title('BottomUp', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_xlabel("Ejercicio", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_ylabel("Tiempo ejecución",fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_ylim([0,50])
ax.set_yticks(range(0,50))
ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.bar(ejercicio, lista)
#plt.plot(ejercicio, lista2, color='green', linestyle='--', marker='o')#Para agregar otro 
for i, txt in enumerate(lista):
    ax.annotate(txt, (ejercicio[i], lista[i]))

plt.show()
