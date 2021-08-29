import numpy as np


matriz = [[-3, -5, 0, 0, 0, 0],
 [1, 0, 1 , 0, 0 , 4],
 [0, 2, 0, 1,0,12],
 [3, 2, 0, 0, 1, 18]]
matriz_np = np.array(matriz)
matriz_np=np.float64(matriz_np)
filaPivote = []

def cambiar_fila(matriz,fila, numeroFilaPivote):
    for i in range(len(matriz)):
        if(i == numeroFilaPivote):
            j = 0
            while j < len(fila):
                matriz[i][j]= fila[j]
                j += 1

def determinar_solucion(matriz, iteracion):

    menorActual = 0
    posicionMenorEnColumna = 0
    #Sacamos al menor de U
    for x in range(len(matriz[0]-1)):
        if matriz[0][x] <= 0 and matriz[0][x] < menorActual:
            menorActual = matriz[0][x]
            posicionMenorEnColumna = x

    if(menorActual >= 0):
        
        print("\nMatriz Final: \n", matriz, "\nU: ", matriz[0][len(matriz[0])-1] ,"\nSolución: ", "Sin Terminar")
        return 1
    else:                
        #columnaMenor es columnaPivote y columnaResultado es el LD
        columnaMenor = matriz[:,posicionMenorEnColumna]
        columnaResultado = matriz[:,(len(matriz[0]))-1]               
        numeroFila = 0
        
        #Acá sacamos al pivote y los respectivos valores de la división de LD / columna pivote
        if iteracion == 0:
            pivote = 10000
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote > (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            numeroFila= i
        elif iteracion >0:
            pivote = 0
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote < (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            numeroFila= i
        y = 0
        z = 0
        m = 0
        nuevaFila = [] 
        filaPivoteNueva= []
        print(numeroFila)

        while y < len(matriz):
            if y == numeroFila:
                while z < len(filaPivote):
                    nuevaFila.append(filaPivote[z] / pivote)
                    filaPivoteNueva.append(filaPivote[z] / pivote)
                    z +=1
                cambiar_fila(matriz, filaPivoteNueva, numeroFila)
                nuevaFila = []                    
            y+=1
      
        while m < len(matriz):
            if m != numeroFila:
                n =0
                
                while n < len(filaPivote):
                    nuevaFila.append(matriz[m][n]+((-columnaMenor[m])*filaPivoteNueva[n]))
                    n += 1
            cambiar_fila(matriz, nuevaFila, m)
            nuevaFila = [] 
            
            m += 1
    print(matriz)
    determinar_solucion(matriz, 1)
    

            
determinar_solucion(matriz_np, 0)



