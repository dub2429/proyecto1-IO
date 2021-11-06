import numpy as np
import time
import matplotlib.pyplot as plt
import random
import pandas as pd

#Falta agregar una fila de ceros al inicio

def mochila(pesos, beneficios,capacidad):
    matrizCeros = np.zeros((len(pesos), capacidad+1))
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
        nuevaColumna = "Columna " + str(i)
        columnaTemp = [0]
        columnaTemp.extend(matrizCeros[:,i])
       #print(matrizCeros[:i])
        diccionario[nuevaColumna] = columnaTemp
    #print(diccionario)
   

    df = pd.DataFrame(data=diccionario)
    print(df)




start = time.perf_counter()

mochila([2,3,4,5],[3,4,5,6],5)
#mochila([5,15,10,10,8],[20,50,60,62,40],30)

end = time.perf_counter()
print("El tiempo de ejecución calculado es:")
print(end - start)

tiempoBottomUp = float("{:.6f}".format(end - start))

lista = []
for i in range(4):
    lista.append(tiempoBottomUp+ random.randrange(4))#Quitar el random, acá se deben meter las pruebas





#Si se quiere graficar otro, nada más se debe agregar un .plot

fig, ax = plt.subplots()
ejercicio = ['E1', 'E2', 'E3', 'E4']
#lista2 = [1,2.6,3.3,0.8564]
tiempo = {'BottomUp': lista} #,'prueba2': lista2 }#Para agregar otro 

#ax.plot(ejercicio, tiempo['BottomUp'])
ax.set_title('BottomUp', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_xlabel("Ejercicio", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_ylabel("Tiempo ejecución",fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
ax.set_ylim([-1,5])
ax.set_yticks(range(-1, 5))
ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.plot(ejercicio, lista, color='#a12424', linestyle='--', marker='o')
#plt.plot(ejercicio, lista2, color='green', linestyle='--', marker='o')#Para agregar otro 
for i, txt in enumerate(lista):
    ax.annotate(txt, (ejercicio[i], lista[i]))

#for i, txt in enumerate(lista):#Para agregar otro 
#   ax.annotate(txt, (ejercicio[i], lista2[i]))#Para agregar otro 
plt.show()