
import numpy as np

#matriz = [[1, 2, -43,78],
 #[4, 5, -56, 5],
 #[7, 8, 10, 200],
 #[99, 10, 9, 8]]

matriz = [[-3, -5, 0, 0, 0, 0],
 [1, 0, 1 , 0, 0 , 5],
 [0, 2, 0, 1,0,12],
 [3, 2, 0, 0, 1, 18]]
matriz_np = np.array(matriz)
matriz_np=np.float64(matriz_np)
filaPivote = []
#pivote = 0
#def imprimir_matriz(matriz):
   #  for columna in range(len(matriz[0])):
   #     for fila in range(len(matriz)):
    #        print(matriz[columna][fila], end=" ")
    #    print()
#imprimir_matriz(matriz)


#Necesito enviar la fila en la que está el pivote
def cambiar_fila(matriz,fila, numeroFilaPivote):
    

    #print("\n\n",fila)

    #print("\n\n", numeroFilaPivote)
    print("\n\nOriginal\n",matriz)
    #print(matriz)
    nueva_matriz = []
    for i in range(len(matriz)):
        if(i == numeroFilaPivote):
            #arreglo = np.array(matriz[i])
            #nueva_matriz.append(arreglo.tolist())
            j = 0
            while j < len(fila):
                print(fila[j])
                matriz[i][j]= fila[j]
                j += 1
    print("\n\nNUEVA\n",matriz)


        #else: 
             #nueva_matriz.append(fila)
             
    #matriz = nueva_matriz
    #print("\n\n",matriz)
    #print("Finalizado")
    #print(matriz[2][0])
    #print(fila)
    
    #NO BORRAR
    #for i in range(len(fila)):
       # print(fila[i])

    #i= numeroFilaPivote
   # for i in range(len(fila)):
    #    for j in range(len(matriz[0])):
    #        matriz[i][j] = fila[i]
   # print("\n\n",matriz)
            

    

#cambiar_fila(matriz_np)

#largo = [1, 45, 7]
def determinar_solucion(matriz):
    menorActual = 0
    posicionMenorEnColumna = 0
    #Sacamos al menor de U
    for x in range(len(matriz[0])):
        if matriz_np[0][x] <= 0 and matriz_np[0][x] < menorActual:
            menorActual = matriz_np[0][x]
            posicionMenorEnColumna = x
    print(menorActual)
    print(posicionMenorEnColumna)
    if(menorActual >= 0):
        print("Decimos que ya termino, pero falta implementar")
    else:
        print("ESTAMOS DESARROLLANDO")
        
        
        #columnaMenor es columnaPivote y columnaResultado es el LD
        columnaMenor = matriz_np[:,posicionMenorEnColumna]
        columnaResultado = matriz_np[:,(len(matriz_np[0])-1)]
        
        #print("ESTAMOS REVISANDO",columnaMenor)
        #print(columnaResultado)
        pivote = 100000
        numeroFila = 0
        #Acá sacamos al pivote y los respectivos valores de la división de LD / columna pivote
        for i in range(len(columnaMenor)):
            print("\nElemento de la Columna Pivote en la iteración: ",columnaMenor[i])
            print("Elemento de columna resultado: ",columnaResultado[i])
            print("Columna Resultado: ", (columnaResultado[i] / columnaMenor[i]))
            if (pivote > (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                    pivote = columnaMenor[i]
                    filaPivote = matriz_np[i]
                    numeroFila= i
                    print("Fila pivote:",filaPivote)
                    print("Pivote: ", pivote)
                    print("Resultado de LD/elementos de la columna pivote: ",columnaResultado[i] / columnaMenor[i])
                    print("Número de fila del pivote: ", i)
                    
        
        #ARREGLAR PORQUE SOLO ES PARA MxM
        #print("\n",filaPivote)
        nuevaFila = []    
        
        i =0
        while i < len(filaPivote):
            nuevaFila.append(filaPivote[i] / pivote)
            
            i+=1
        
        print(nuevaFila)

    return cambiar_fila(matriz,nuevaFila,numeroFila)
            
determinar_solucion(matriz_np)


