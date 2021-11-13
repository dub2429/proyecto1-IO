#Proyecto4
#Investigación de operaciones
#Programación dinámica: el contenedor
#Estudiantes:
#Erick Blanco
#David Umañan
#Fabián Vives
#Profesor: Carlos Gamboa


import numpy as np
import time
import matplotlib.pyplot as plt
import random
import pandas as pd
import datetime
from itertools import combinations
import sys
from statistics import mean
from operator import itemgetter



#contenedor.py algoritmo -a archivo.txt iteraciones
#algoritmo requerido, valores 1=fuerza bruta, 2=pd bottom-up, 3=pd top-down
# -a archivo.txt archivo con los datos del problema
# iteraciones cantidad de corridas para medir tiempo promedio
documento_entrada = sys.argv[3]

modo = sys.argv[2]
if modo == "-a":
    numeroIteraciones = int(sys.argv[4])    
elif modo == "-p":
    numeroIteraciones = int(sys.argv[7]) 
#print(sys.argv[0:])#len = 5

elementosFB = []



def leerDocumento():
        #Llama a la función donde se crea la matriz iniciar
        #document = sys.argv[1]
        #print(sys.argv[1])
        #Función reutilizada de proyectos anteriores en el curso
        with open(str(documento_entrada)) as documento:
            contenido = documento.read()
        arreglo = contenido.split("\n")
        arregloMatriz = []
        for i in range(len(arreglo)):
            arregloMatriz.append(arreglo[i].split(","))
        #print(arregloMatriz)
        return arregloMatriz

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
    
    #PARA IMPRIMIR
   #diccionario = {}
   #for i in range(len(matrizCeros[0])):
   #    nuevaColumna = "C" + str(i)
   #    columnaTemp = [0]
   #    columnaTemp.extend(matrizCeros[:,i])
   #   #print(matrizCeros[:i])
   #    diccionario[nuevaColumna] = columnaTemp
   ##print(diccionario)
   #




   #df = pd.DataFrame(data=diccionario)
   # print(df)
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
##########################################################################################################################################################
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
#########################################################################################################################################################
#AGREGAR FUERZA BRUTA

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

#carga máxima del camión

# Útiles para acceso al peso y valores (irían mejor definiendo una clase)
start = time.perf_counter()
get_peso = itemgetter(0)
beneficios = []
valores = []
arregloValores = []


for i in range(len(valores)):
    beneficios.append(valores[i][1])
#print("ABSHBAS",str(beneficios))
get_valor = itemgetter(1)

def total_peso(paquetes):
    return sum(get_peso(x) for x in paquetes)

def total_valor(paquetes):
    #print(sum(get_valor(x) for x in paquetes))
    return sum(get_valor(x) for x in paquetes)

# Obtención de todas las combinaciones posibles
# Función recursiva
def combinaciones(paquetes, peso_maximo):
    paqs = [ p for p in paquetes if get_peso(p) <= peso_maximo ]
    resultado = []
    for p in paqs:
        res = combinaciones([x for x in paqs if x!=p], peso_maximo - get_peso(p))
        if len(res) == 0:
            resultado.append([p])
        else:
            resultado.extend([[p]+x for x in res])
    
    return resultado

# solución



###########################################################################################################################################################

def menu():
    

    
    
    #print(pesos)
    #print(beneficios)


    if int(sys.argv[1]) == 1:
        #print("Fuerza bruta")
        if modo=="-a":
            elementos = leerDocumento()
            capacidad = elementos[0]
            capacidad = int(capacidad[0])
            pesos = []
            beneficios = []
            j = 1
            while j < len(elementos):
                pesos.append(int(elementos[j][0]))
                beneficios.append(int(elementos[j][1]))
                j +=1
            lista1 = []
            with open(str(documento_entrada)) as documento:
                    contenido = documento.read()
            arreglo = contenido.split("\n")
            elementosFB.append(arreglo[1:])
            arregloValores = []
            for i in range(len(elementosFB[0])):
                    arregloValores.append(elementosFB[0][i])
            valores = []
            for j in range(len(arregloValores)):
                valores.append(arregloValores[j].split(","))
            for i in range(len(valores)):
                for j in range(len(valores[i])):
                    valores[i][j] = int(valores[i][j])
            print(valores)
            print(arregloValores)
                
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                print("\n")
                print("---------------------------------------------------------")
                print("Iteración "+str(i+1))
                a=max(combinaciones(valores, capacidad), key=total_valor)
                #print(a)
                suma = 0
                print(a)
                for i in range(len(a)):
                    suma += (a[i][1])
                
                #print(total_valor)
                
                print("El beneficio máximo del algortimo de fuerza bruta es:"+str(suma))
                for i in range(len(beneficios)):
                    comb = combinations(beneficios, i)
                    for j in list(comb):
                        if sum(j) == suma:
                            #print(j)
                            listaIndices = []
                            for k in range(len(j)):
                                listaIndices.append(str(beneficios.index(j[k])+1))
                            #print(beneficios)
                            #articulos = "Los artículos son: " + ','.join(listaIndices)
                            print("Los artículos incluidos para el algortimo de fuerza bruta son: " + ','.join(listaIndices))
                            print("---------------------------------------------------------")
                        # print("Encontrado")
                            break

                end = time.perf_counter()
                #print(end-start)
                lista1.append(end-start)
            print("\nProceso finalizado, el tiempo promedio es "+str(mean(lista1)))
        elif modo=="-p":
            print("Estamos trabajando eso")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            lista1 = []
            valores = []
            for i in range(len(beneficios)):
                valores.append([pesos[i],beneficios[i]])
            for i in range(len(valores)):
                for j in range(len(valores[i])):
                    valores[i][j] = int(valores[i][j])
            print(valores)
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                print("\n")
                print("---------------------------------------------------------")
                print("Iteración "+str(i+1))
                a=max(combinaciones(valores, capacidad), key=total_valor)
                #print(a)
                suma = 0
                print(a)
                for i in range(len(a)):
                    suma += (a[i][1])
                
                #print(total_valor)
                
                print("El beneficio máximo del algortimo de fuerza bruta es:"+str(suma))
                for i in range(len(beneficios)):
                    comb = combinations(beneficios, i)
                    for j in list(comb):
                        if sum(j) == suma:
                            #print(j)
                            listaIndices = []
                            for k in range(len(j)):
                                listaIndices.append(str(beneficios.index(j[k])+1))
                            #print(beneficios)
                            #articulos = "Los artículos son: " + ','.join(listaIndices)
                            print("Los artículos incluidos para el algortimo de fuerza bruta son: " + ','.join(listaIndices))
                            print("---------------------------------------------------------")
                        # print("Encontrado")
                            break

                end = time.perf_counter()
                #print(end-start)
                lista1.append(end-start)
            print("\nProceso finalizado, el tiempo promedio es "+str(mean(lista1)))

    elif int(sys.argv[1]) == 2:
        if modo=="-a":
            elementos = leerDocumento()
            capacidad = elementos[0]
            capacidad = int(capacidad[0])
            pesos = []
            beneficios = []
            j = 1
            while j < len(elementos):
                pesos.append(int(elementos[j][0]))
                beneficios.append(int(elementos[j][1]))
                j +=1
            iteraciones = []
            
            for i in range(numeroIteraciones):

                start = time.perf_counter()
                BottomUp(pesos,beneficios,capacidad)
                end = time.perf_counter()
                iteraciones.append(float("{:.6f}".format((end - start))))
            
            #print(iteraciones)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoBottomUp = mean(iteraciones)
            print(tiempoBottomUp)
        elif modo=="-p":
            print("Estamos trabajando eso")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            iteraciones = []
            
            for i in range(numeroIteraciones):

                start = time.perf_counter()
                BottomUp(pesos,beneficios,capacidad)
                end = time.perf_counter()
                iteraciones.append(float("{:.6f}".format((end - start))))
            
            #print(iteraciones)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoBottomUp = mean(iteraciones)
            print(tiempoBottomUp)
        
    elif int(sys.argv[1]) == 3:
        if modo=="-a":
            elementos = leerDocumento()
            capacidad = elementos[0]
            capacidad = int(capacidad[0])
            pesos = []
            beneficios = []
            j = 1
            while j < len(elementos):
                pesos.append(int(elementos[j][0]))
                beneficios.append(int(elementos[j][1]))
                j +=1
            iteracionesTD = []
            valorC = beneficios.copy()
            beneficios.insert(0, None)  #de modo que el valor del i-ésimo artículo está en valor [i]
            pesos.insert(0, None) #de modo que el peso del i-ésimo artículo sea el peso [i] 

            respuesta = top_down(beneficios,pesos,capacidad,valorC)
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                #valor = beneficios
                
                respuesta = top_down(beneficios,pesos,capacidad,valorC)
                print('El valor máximo de los artículos que se pueden llevar: ', respuesta)
                #imprimir_tabla(resultadoTop)
                print(articulos)
                end = time.perf_counter()
                iteracionesTD.append(float("{:.6f}".format((end - start))))

            #print(iteracionesTD)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoTopDown = mean(iteracionesTD)
            print(tiempoTopDown)
        elif modo=="-p":
            print("Estamos trabajando eso")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            iteracionesTD = []
            valorC = beneficios.copy()
            beneficios.insert(0, None)  #de modo que el valor del i-ésimo artículo está en valor [i]
            pesos.insert(0, None) #de modo que el peso del i-ésimo artículo sea el peso [i] 

            respuesta = top_down(beneficios,pesos,capacidad,valorC)
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                #valor = beneficios
                
                respuesta = top_down(beneficios,pesos,capacidad,valorC)
                print('El valor máximo de los artículos que se pueden llevar: ', respuesta)
                #imprimir_tabla(resultadoTop)
                print(articulos)
                end = time.perf_counter()
                iteracionesTD.append(float("{:.6f}".format((end - start))))

            #print(iteracionesTD)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoTopDown = mean(iteracionesTD)
            print(tiempoTopDown)
    elif int(sys.argv[1]) == 4:
        if modo=="-p":

####################################################################################################################################
            print("\n\n")
            print("BU")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            iteraciones = []
            
            for i in range(numeroIteraciones):

                start = time.perf_counter()
                print("\n")
                BottomUp(pesos,beneficios,capacidad)
                end = time.perf_counter()
                iteraciones.append(float("{:.6f}".format((end - start))))
            
            #print(iteraciones)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoBottomUp = mean(iteraciones)
            print(tiempoBottomUp)
####################################################################################################################################
            print("\n\n")
            print("TD")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            iteracionesTD = []
            valorC = beneficios.copy()
            beneficios.insert(0, None)  #de modo que el valor del i-ésimo artículo está en valor [i]
            pesos.insert(0, None) #de modo que el peso del i-ésimo artículo sea el peso [i] 

            respuesta = top_down(beneficios,pesos,capacidad,valorC)
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                #valor = beneficios
                
                respuesta = top_down(beneficios,pesos,capacidad,valorC)
                print('El valor máximo de los artículos que se pueden llevar: ', respuesta)
                #imprimir_tabla(resultadoTop)
                print(articulos)
                end = time.perf_counter()
                iteracionesTD.append(float("{:.6f}".format((end - start))))

            #print(iteracionesTD)
            print("La media de ejecución es:")
            #print(datetime.timedelta(seconds= end  - start))
            tiempoTopDown = mean(iteracionesTD)
            print(tiempoTopDown)

####################################################################################################################################
            print("Estamos trabajando eso")
            print(sys.argv[6])
            rangoBeneficios = sys.argv[6]
            beneficios = list(range(int(rangoBeneficios[0]),int(rangoBeneficios[2])+1))
            print(beneficios)
            capacidad = sys.argv[4]
            capacidad = int(capacidad[0])
            print(capacidad)
            rangoPesos = sys.argv[5]
            pesos = list(range(int(rangoPesos[0]),int(rangoPesos[2])+1))
            print(pesos)
            j = 1
            lista1 = []
            valores = []
            for i in range(len(beneficios)):
                valores.append([pesos[i],beneficios[i]])
            for i in range(len(valores)):
                for j in range(len(valores[i])):
                    valores[i][j] = int(valores[i][j])
            print(valores)
            for i in range(numeroIteraciones):
                start = time.perf_counter()
                print("\n")
                print("---------------------------------------------------------")
                print("Iteración "+str(i+1))
                a=max(combinaciones(valores, capacidad), key=total_valor)
                #print(a)
                suma = 0
                print(a)
                for i in range(len(a)):
                    suma += (a[i][1])
                
                #print(total_valor)
                
                print("El beneficio máximo del algortimo de fuerza bruta es:"+str(suma))
                for i in range(len(beneficios)):
                    comb = combinations(beneficios, i)
                    for j in list(comb):
                        if sum(j) == suma:
                            #print(j)
                            listaIndices = []
                            for k in range(len(j)):
                                listaIndices.append(str(beneficios.index(j[k])+1))
                            #print(beneficios)
                            #articulos = "Los artículos son: " + ','.join(listaIndices)
                            print("Los artículos incluidos para el algortimo de fuerza bruta son: " + ','.join(listaIndices))
                            print("---------------------------------------------------------")
                        # print("Encontrado")
                            break

                end = time.perf_counter()
                #print(end-start)
                lista1.append(end-start)
            tiempoFB = mean(lista1)
            print("\nProceso finalizado, el tiempo promedio es "+str(tiempoFB))
####################################################################################################################################
            lista=[float("{:.6f}".format(tiempoBottomUp)),float("{:.6f}".format(tiempoTopDown)), float("{:.6f}".format(tiempoFB))]
            
            #Si se quiere graficar otro, nada más se debe agregar un .plot

            fig, ax = plt.subplots()
            ejercicio = ['BU', 'TD', 'FB']
            tiempo = {'Promedios': lista}#,'prueba2': lista2 }#Para agregar otro 

            #ax.plot(ejercicio, tiempo['BottomUp'])
            ax.set_title('Ánalisis de los algoritmos', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
            ax.set_xlabel("Ejercicio", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
            ax.set_ylabel("Tiempo ejecución",fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
            ax.set_ylim((0,0.01))
            ax.set_yticks((0,0.01))
            ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
            plt.bar(ejercicio, lista)
            #plt.plot(ejercicio, lista2, color='green', linestyle='--', marker='o')#Para agregar otro 
            for i, txt in enumerate(lista):
                ax.annotate(txt, (ejercicio[i], lista[i]))

            plt.show()
        else:
            print("Algoritmo no encontrado")

    else:
        print("Algortimo no encontrado")
    

menu()
