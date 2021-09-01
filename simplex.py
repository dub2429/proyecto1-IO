import numpy as np

def leerDocumento():
    with open('archivo1.txt') as documento:
        contenido = documento.read()
    arreglo = contenido.split("\n")
    arregloMatriz = []
    for i in range(len(arreglo)):
        arregloMatriz.append(arreglo[i].split(","))
    #print(arregloMatriz)
    return crear_matriz(arregloMatriz)

def determinarSoluciones(variablesBasicas,variables, matrizNumero):
    #print("largo variables basicas: "+ str(len(variablesBasicas)))
    for i in range(len(variables)):
        if variables[i] not in variablesBasicas:
            variables[i] = 0
        else:
           #print("Pos "+ str(variablesBasicas.index(variables[i])))
            pos = variablesBasicas.index(variables[i])
            #print("# "+str(matriz[pos+2][len(matriz[0])-1]))
            variables[i] = matrizNumero[pos+1][len(matrizNumero[0])-1]
            #print(variables)
    return variables

def crear_matriz(matrizDocumento):
    numero_varZ = int(matrizDocumento[0][2])
    numero_inec = int(matrizDocumento[0][3])
    num_filas = numero_inec + 2
    num_colum = numero_inec + numero_varZ + 2
    matriz = []
    variablesBasicas = numero_inec+numero_varZ
    variablesNoBasicas = numero_varZ
    variablesNoBasicasIngresar = numero_varZ
    variablesBasicas = numero_varZ+1
    #print("#Variables Básicas: "+ str(variablesBasicas-variablesNoBasicas)+ "   #Variables No Básicas: " + str(variablesNoBasicas))
    for i in range(num_filas):
        matriz.append([])
        for j in range(num_colum):
                matriz[i].append(0)
    
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
                    matriz[i][j] = "X"+str(variablesBasicas)
                    variablesBasicas +=1
                elif elemento<len(matrizDocumento[i]) and matrizDocumento[i][elemento] != "<=" :
                     matriz[i][j] = float(matrizDocumento[i][elemento])
                     elemento += 1
                if j == variablesNoBasicasIngresar+1:
                    matriz[i][j] = 1
                    
                else:
                    if j == len(matriz[i])-1:
                        matriz[i][j] = float(matrizDocumento[i][len(matrizDocumento[i])-1])
                        variablesNoBasicasIngresar += 1
    return matriz



matriz = leerDocumento()
matriz_np = np.array(matriz)
elemento= matriz_np[1][1]
#print(float(elemento)*5)
matrizATrabajar = matriz_np[1:, 1:]
matrizATrabajar=np.float64(matrizATrabajar)


filaPivote = []

def cambiar_fila(matriz,fila, numeroFilaPivote):
    for i in range(len(matriz)):
        if(i == numeroFilaPivote):
            j = 0
            while j < len(fila):
                matriz[i][j]= fila[j]
                j += 1


def escribir(dato):
    archivo = open('datos.txt','a')
    nuevaLinea= str(dato) + "\n"
    archivo.write(nuevaLinea)
texto = "Matriz inicial: " + "\n" + str(matriz_np) + "\n\n\n"  
escribir(texto)

###############Solución##################################################################################
def determinar_solucion(matriz, iteracion):

    menorActual = 0
    posicionMenorEnColumna = 0
    #Sacamos al menor de U
    for x in range(len(matriz[0]-1)):
        if matriz[0][x] <= 0 and matriz[0][x] < menorActual:
            menorActual = matriz[0][x]
            posicionMenorEnColumna = x

    if(menorActual >= 0):
        matrizSolucion= crearMatrizFinal(matriz_np,matriz)
        #No borrar, estamos trabajando en esto
        j = 2
        listaVB = []
        elemento = ""
        while j <len(matriz_np):
            elemento = matriz_np[j][0]
            listaVB.append(elemento)
            j+=1
            #print("VARIABELSB" + str(listaVB))#Saca VB
        variables = matriz_np[0][1:len(matriz_np[0])-1]
        #print("VARIABELS"+str(matrizConLetras[0][1:len(matrizConLetras)-1]))#saca la variables sin VB y LD del ecnabezado
        solucion= determinarSoluciones(listaVB, variables, matriz)
        #print("Solución" + str(sol))

        #determinarSoluciones(str(matrizSolucion[1:,0]), str(matrizSolucion[0]), matrizSolucion)
        print("\nMatriz Final: \n", matrizSolucion, "\nU: ", matriz[0][len(matriz[0])-1] ,"\nSolución: ", solucion)
        texto = "\n\nMatriz Final: \n"+ matrizSolucion+ "\nU: "+ str(matriz[0][len(matriz[0])-1]) +"\nSolución: "+ str(solucion)
        return escribir(texto)
    else:                
        #columnaMenor es columnaPivote y columnaResultado es el LD 
        #columnaPivoteVariables es la columnaPivote de la matriz que contiene las VB
        columnaMenor = matriz[:,posicionMenorEnColumna]
        columnaResultado = matriz[:,(len(matriz[0]))-1]  
        columnaPivoteVariables = matriz_np[:,posicionMenorEnColumna+1]           
        numeroFila = 0
        textoColumnaPivote = "\nColumna Pivote: "+ str(columnaMenor) 
        #print("\nColumna Pivote Matriz_np: "+str(columnaPivoteVariables))
        #Acá sacamos al pivote y los respectivos valores de la división de LD / columna pivote
        if iteracion == 0:
            pivote = 10000
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote > (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            filaPivoteVariables = matriz_np[i+1]
                            #print("\nFila Pivote Matriz_np: "+str(filaPivoteVariables))
                            numeroFila= i
        elif iteracion >0:
            pivote = 0
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote < (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            filaPivoteVariables = matriz_np[i+1]
                            #print("\nFila Pivote Matriz_np: "+str(filaPivoteVariables))
                            numeroFila= i
            
        y = 0
        z = 0
        m = 0
        nuevaFila = [] 
        filaPivoteNueva= []
        filaAntigua = []
        nuevaVB = []

        while y < len(matriz):
            if y == numeroFila:
                while z < len(filaPivote):
                    texto = "\nOperación a realizar: " + str(filaPivote[z]) + "/" + str(pivote)
                    escribir(texto)
                    nuevaFila.append(filaPivote[z] / pivote)
                    filaAntigua.append(filaPivote[z])
                    filaPivoteNueva.append(filaPivote[z] / pivote)
                    z +=1
                nuevaVB.append(columnaPivoteVariables[0])
                cambiar_fila(matriz, filaPivoteNueva, numeroFila)
                cambiar_fila(matriz_np, nuevaVB, numeroFila+1)
                nuevaFila = []
                nuevaVB = []    
                #print("\n\n La nuevaVB en matriz_np es: \n "+str(matriz_np))                
            y+=1
        
        texto = "\n\nPivote: " +str(pivote) +textoColumnaPivote+"\nCambiando Fila: Pivote" +"\nFila Pivote: " + str(filaAntigua) + "\nNueva Fila pivote: " + str(filaPivoteNueva) + "\nNueva Matriz:\n"+ crearMatrizFinal(matriz_np,matriz) +  "\n\n\n"
        escribir(texto)
        filaAntigua = []
        while m < len(matriz):
            if m != numeroFila:
                n =0
                
                while n < len(filaPivote):
                    filaAntigua.append(matriz[m][n])
                    texto = "\nOperación a realizar: " + str(matriz[m][n]) + "+" +str(-columnaMenor[m])+"*"+str(filaPivoteNueva[n])
                    #escribir(texto)
                    nuevaFila.append(matriz[m][n]+((-columnaMenor[m])*filaPivoteNueva[n]))
                    n += 1
                cambiar_fila(matriz, nuevaFila, m)
                texto = "\nCambiando Fila: " + str(m+1) +"\nFila Antigua: " + str(filaAntigua) + "\nNueva Fila: " + str(nuevaFila)+ "\nNueva Matriz:\n"+ crearMatrizFinal(matriz_np,matriz)+ "\n\n\n"
                escribir(texto) 
                nuevaFila = []  
                filaAntigua = []
             
            m += 1 
          
    determinar_solucion(matriz, 1)


def crearMatrizFinal(matrizConLetras,matrizConNumeros):
   
    matrizFinal = []
    columnaLetras = matrizConLetras[1:,0]

    
    for i in range(len(matrizConNumeros)):
        letra = np.array(columnaLetras[i])
        numeros = np.array(matrizConNumeros[i])
        matrizFinal.append(letra)
        matrizFinal.append(numeros)
    
    textoMatriz= ""
    i = 0  
    while i < (len(matrizFinal)):
        filaNumeros = ""
        for j in range (len(matrizFinal[i+1])):
            filaNumeros += str(round(matrizFinal[i+1][j],2)) + "  "
        textoMatriz += "   " + str(matrizFinal[i])+ "  " + filaNumeros + "\n"
        i += 2
    
    
    textoFinal = str(matrizConLetras[0])+ "\n" + textoMatriz 
    return textoFinal


              
determinar_solucion(matrizATrabajar, 0)
