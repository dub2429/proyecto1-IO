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
    #texto = "\n\n\n\n\n\n\nNueva Matriz\n" + str(matriz) 
    #escribir(texto)

def escribir(dato):
    archivo = open('datos.txt','a')
    nuevaLinea= str(dato) + "\n"
    archivo.write(nuevaLinea)
texto = "Matriz inicial: " + "\n" + str(matriz_np) + "\n\n\n"  
escribir(texto)

def determinar_solucion(matriz, iteracion):

    menorActual = 0
    posicionMenorEnColumna = 0
    #Sacamos al menor de U
    for x in range(len(matriz[0]-1)):
        if matriz[0][x] <= 0 and matriz[0][x] < menorActual:
            menorActual = matriz[0][x]
            posicionMenorEnColumna = x

    if(menorActual >= 0):
        #print("\nMatriz Final: \n", matriz, "\nU: ", matriz[0][len(matriz[0])-1] ,"\nSolución: ", "Sin Terminar")
        texto = "\n\nMatriz Final: \n"+ str(matriz)+ "\nU: "+ str(matriz[0][len(matriz[0])-1]) +"\nSolución: "+ "Sin Terminar"
        return escribir(texto)
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
        filaAntigua = []
        #print(numeroFila)

        while y < len(matriz):
            if y == numeroFila:
                while z < len(filaPivote):
                    texto = "\nOperación a realizar: " + str(filaPivote[z]) + "/" + str(pivote)
                    escribir(texto)
                    nuevaFila.append(filaPivote[z] / pivote)
                    filaAntigua.append(filaPivote[z])
                    filaPivoteNueva.append(filaPivote[z] / pivote)
                    z +=1
                cambiar_fila(matriz, filaPivoteNueva, numeroFila)
                nuevaFila = []                    
            y+=1
        texto = "\n\nPivote: " +str(pivote) +"\nCambiando Fila: Pivote" +"\nFila Pivote: " + str(filaAntigua) + "\nNueva Fila pivote: " + str(filaPivoteNueva) + "\nNueva Matriz:\n"+ str(matriz) +  "\n\n\n"
        escribir(texto)
        filaAntigua = []
        while m < len(matriz):
            if m != numeroFila:
                n =0
                
                while n < len(filaPivote):
                    filaAntigua.append(matriz[m][n])
                    texto = "\nOperación a realizar: " + str(matriz[m][n]) + "+" +str(-columnaMenor[m])+"*"+str(filaPivoteNueva[n])
                    escribir(texto)
                    nuevaFila.append(matriz[m][n]+((-columnaMenor[m])*filaPivoteNueva[n]))
                    n += 1
                cambiar_fila(matriz, nuevaFila, m)
                texto = "\nCambiando Fila: " + str(m+1) +"\nFila Antigua: " + str(filaAntigua) + "\nNueva Fila: " + str(nuevaFila)+ "\nNueva Matriz:\n"+ str(matriz)+ "\n\n\n"
                escribir(texto) 
                nuevaFila = []  
                filaAntigua = [] 
            m += 1
        
    print(matriz)
    determinar_solucion(matriz, 1)
    
            
determinar_solucion(matriz_np, 0)


