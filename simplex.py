import numpy as np


import numpy as np

def leerDocumento():
    with open('archivo1.txt') as documento:
        contenido = documento.read()
        #print(contenido.rstrip())
    arreglo = contenido.split("\n")
    arregloMatriz = []
    for i in range(len(arreglo)):
        arregloMatriz.append(arreglo[i].split(","))
    print(arregloMatriz)
    return crear_matriz(arregloMatriz)

i = 0
def crearMatriz(contenido):
    print(contenido)





def crear_matriz(matrizDocumento):
    numero_varZ = int(matrizDocumento[0][2])
    numero_inec = int(matrizDocumento[0][3])
    num_filas = numero_inec + 2
    num_colum = numero_inec + numero_varZ + 2
    matriz = []
    variablesBasicas = numero_inec+numero_varZ
    variablesNoBasicas = numero_varZ
    variablesNoBasicasIngresar = numero_varZ

    print("#Variables Básicas: "+ str(variablesBasicas-variablesNoBasicas)+ "   #Variables No Básicas: " + str(variablesNoBasicas))
    for i in range(num_filas):
        matriz.append([])
        for j in range(num_colum):
                matriz[i].append(0)
    #print(matriz)
    
    for i in range(num_filas):
        if i == 0:
            for j in range(num_colum):
                if(j==0):
                    matriz[i][j] = "VB"
                elif(j==(num_colum-1)):
                    matriz[i][j] = "LD"
                else:
                    matriz[i][j] = "X"+str(j)
        elif i == 1:
            elemento = 0
            for j in range(num_colum):
                if j == 0:
                    matriz[i][j] = "U"
                elif elemento<len(matrizDocumento[i]) and matrizDocumento[i][elemento]:
                     matriz[i][j] = -float(matrizDocumento[i][elemento])
                     elemento += 1
                
        else:
            elemento = 0
            for j in range(num_colum):
                if j == 0:
                    matriz[i][j] = "X"+str(i+1) #Cambiar y meter las variables básicas del arreglo
                elif elemento<len(matrizDocumento[i]) and matrizDocumento[i][elemento] != "<=" :
                     matriz[i][j] = float(matrizDocumento[i][elemento])
                     elemento += 1
                #elif matrizDocumento[i][j] == "<=":
                    #elemento += 1
                if j == variablesNoBasicasIngresar+1:
                    matriz[i][j] = 1
                    
                else:
                    if j == len(matriz[i])-1:
                        matriz[i][j] = float(matrizDocumento[i][len(matrizDocumento[i])-1])
                        variablesNoBasicasIngresar += 1
                    

    print(matriz)
    return matriz



matriz = leerDocumento()
matriz_np = np.array(matriz)

#np.array([[15,26,2,17,22],[13,8,9,3,4]])
elemento= matriz_np[1][1]
print(float(elemento)*5)

matrix = matriz_np[1:, 1:]
matrix=np.float64(matrix)


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
        print("\nMatriz Final: \n", matriz, "\nU: ", matriz[0][len(matriz[0])-1] ,"\nSolución: ", "Sin Terminar")
        texto = "\n\nMatriz Final: \n"+ str(matriz)+ "\nU: "+ str(matriz[0][len(matriz[0])-1]) +"\nSolución: "+ "Sin Terminar"
        return escribir(texto)
    else:                
        #columnaMenor es columnaPivote y columnaResultado es el LD
        columnaMenor = matriz[:,posicionMenorEnColumna]
        columnaResultado = matriz[:,(len(matriz[0]))-1]               
        numeroFila = 0
        textoColumnaPivote = "\nColumna Pivote: "+ str(columnaMenor) 
        
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
        texto = "\n\nPivote: " +str(pivote) +textoColumnaPivote+"\nCambiando Fila: Pivote" +"\nFila Pivote: " + str(filaAntigua) + "\nNueva Fila pivote: " + str(filaPivoteNueva) + "\nNueva Matriz:\n"+ str(matriz) +  "\n\n\n"
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
        
    #print(matriz)
    determinar_solucion(matriz, 1)
    

            
determinar_solucion(matrix, 0)