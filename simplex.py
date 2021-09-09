#PROYECTO 1 del curso de Investigación de operaciones
#Instituto Tecnológico de Costa Rica
#Estudiantes: Erick Blanco, David Umaña, Fabián Vives
#Profesor: Carlos gamboa
#Método SIMPLEX
import sys
import numpy as np
from collections import defaultdict

documento_entrada = sys.argv[1]
documento_salida = documento_entrada.split(".")

def leerDocumento():
    #S: Llama a la función donde se crea la matriz iniciar
    
    with open(str(documento_entrada)) as documento:
        contenido = documento.read()
    arreglo = contenido.split("\n")
    arregloMatriz = []
    for i in range(len(arreglo)):
        arregloMatriz.append(arreglo[i].split(","))
    return crear_matriz(arregloMatriz)


def determinarMultiplesSoluciones(encabezado,variablesBasicas,matrizNumeros):
    #E:La fila 0 de la matriz inicial, la columna 0 de la matriz y una matriz que solo contiene números
    #S: respuesta; esto para determinar si la matriz es de solución multiple
    #La posición de la variable no básica que hace a la matriz de solucón múltiple
    #textoSolucion:Texto para agregar en el documento y mostrar en pantalla
    encabezado = matriz[0][1:len(matriz[0])-1]
    respuesta = 0
    posicionVariableNoBásica = -1
    i = 0
    textoSolucion = ""
    while i < (len(encabezado)):
        if encabezado[i] not in variablesBasicas:
            if matrizNumeros[0][i] == 0:
                posicionVariableNoBásica = i
                textoSolucion = "Hay solución múltiple por variable "+ encabezado[i]+ " en la posicion "+ str(i+1)+ " de la fila U, ya que es variable No Básica y el valor es 0"
                print(textoSolucion)
                i = len(encabezado)+1
                respuesta = 1
        i += 1
        return(respuesta, posicionVariableNoBásica, textoSolucion)  


def determinarSoluciones(variablesBasicas,variables, matrizNumero):
    #E: Columna 0 de la matriz actual, el encabezado y la matriz de números
    #S: Devuelve las nuevas variables Básicas de la matriz
    for i in range(len(variables)):
        if variables[i] not in variablesBasicas:
            variables[i] = 0
        else:
            pos = variablesBasicas.index(variables[i])
            variables[i] = matrizNumero[pos+1][len(matrizNumero[0])-1]
    return variables

def determinarDegenerada(columnaPivote, columnaLD):
    #E: Columna Pivote y la columna resultado (columna Lado derecho)
    #S Determina si existen resultados iguales después de dividir elemento de LD entre el elemento de la columna pivote 
    columnaResultado= [] #Guarda los resultados obtenidos inicialmente
    arregloresultados= [] 
    for i in range(len(columnaPivote)):
        if(float(columnaPivote[i])):
            arregloresultados.append(float(columnaLD[i])/float(columnaPivote[i]))
            x = float(columnaLD[i])/float(columnaPivote[i])
            columnaResultado.append(x)

    llaves = defaultdict(list);
    lista = []
    # Recorre todos los elementos de la columnaResultado:
    for llave, valor in enumerate(columnaResultado):

        # Adiciona el indice en lista de índices:
        llaves[valor].append(llave)

    for valor in llaves:
        if len(llaves[valor]) > 1:
            lista = llaves[valor]
    #print(lista)
    tamaño = len(lista)       
    return lista,tamaño


def crear_matriz(matrizDocumento):
    #E: La matriz que proviene posterior a leer el docuemento
    #S: La matriz con el encabezado, VB y sus respectivos valores
    numero_varU = int(matrizDocumento[0][2])
    numero_inec = int(matrizDocumento[0][3])
    num_filas = numero_inec + 2
    num_colum = numero_inec + numero_varU + 2
    matriz = []
    variablesBasicas = numero_inec+numero_varU
    variablesNoBasicasIngresar = numero_varU
    variablesBasicas = numero_varU+1
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
matriz_np = np.array(matriz)#Hacemos que la matriz sea Numpy para realizar diferentes operaciones sobre la misma
elemento= matriz_np[1][1]
matrizATrabajar = matriz_np[1:, 1:]
matrizATrabajar=np.float64(matrizATrabajar)
letrasEncabezado = matriz_np[0]
encabezado = np.array(letrasEncabezado)
filaPivote = []
print("Matriz Inicial: \n"+ str(matriz_np))

def cambiar_fila(matriz,fila, numeroFilaPivote):
    #E:Una matriz de números, la nueva fila y el número de fila a cambiar
    #S: La nueva matriz
    for i in range(len(matriz)):
        if(i == numeroFilaPivote):
            j = 0
            while j < len(fila):
                matriz[i][j]= fila[j]
                j += 1
    return matriz

def escribir(dato):
    #E: Información a escribir en el documento de salida 
    #S: La creación del documento si no lo está y si está escribe sobre el mismo
    nombre_archivo = documento_salida[0]+"_solution.txt"
    archivo = open(nombre_archivo,'a')
    nuevaLinea= str(dato) + "\n"
    archivo.write(nuevaLinea)
texto = "Matriz inicial: " + "\n" + str(matriz_np) + "\n"  
escribir(texto)

###############Solución##################################################################################
def determinar_solucion(matriz, iteracion):
    #E: Una matriz de números y un entero 
    #S: Retorna la matriz final en pantalla o los casos especiales, además de llamar la función de escribir
    #para guardar los valores respectivos
    menorActual = 0 #variable en la que se guarda el menor de la fila U
    posicionMenorEnColumna = 0 #Variable en la que se guarda la posición del menor en U
    
    #Sacamos al menor de U
    for x in range(len(matriz[0]-1)):
        if matriz[0][x] <= 0 and matriz[0][x] < menorActual:
            menorActual = matriz[0][x]
            posicionMenorEnColumna = x
    #Determinamos si existe un número menor o igual que 0 en la fila de U   
    if(menorActual >= 0):
        matrizSolucion= crearMatrizFinal(matriz_np,matriz)#Llamada a crear la función final 
        j = 2
        listaVB = []#Lista de variables básicas
        elemento = " "#Se debe poner ya que sino al no tener variables degeneradas, produce un fallo

        while j <len(matriz_np):
            elemento = matriz_np[j][0]
            listaVB.append(elemento)
            j+=1
        variables = matriz_np[0][1:len(matriz_np[0])-1]
        #Se determina la solución a escribir en el documento de salida
        solucion= determinarSoluciones(listaVB, variables, matriz) 
        texto = "\n\nMatriz Final: \n"+ matrizSolucion+ "\nU: "+ str(matriz[0][len(matriz[0])-1]) +"\nSolución: "+ str(solucion)
        escribir(texto)
        print(texto)
        #Se hacela consulta de si existen multiples soluciones 
        estadoSolucionesMultiples = determinarMultiplesSoluciones(encabezado,listaVB,matriz)
        numeroColumna = estadoSolucionesMultiples[1]+1
        textoSolucionMultiple = estadoSolucionesMultiples[2]
        #Se pregunta si existen Variables no básicas iguales que 0
        if(estadoSolucionesMultiples[0] == 1 and estadoSolucionesMultiples[1]>-1):
            texto = "\n\n\n\n" + textoSolucionMultiple
            escribir(texto)
            pivote = 0
            columnaVNB = matriz[:,estadoSolucionesMultiples[1]]
            columnaResultado = matriz[:,(len(matriz[0]))-1]
            VBNueva= encabezado[numeroColumna]
            #Determina la nueva fila pivote
            for i in range(len(matriz[:,(len(matriz[0]))-1])):
                if columnaVNB[i] > 0 and (pivote < (columnaResultado[i] / columnaVNB[i])) and ((columnaResultado[i] / columnaVNB[i]) > 0):
                    pivote = columnaVNB[i]
                    numeroFila = i
            filaAntigua = []
            escribir("Columna Pivote: "+str(matriz[:,estadoSolucionesMultiples[1]])+ "\nNúmero Pivote: " + str(pivote))
            #Realiza los procedimientos respectivos de la fila pivote
            for i in range(len(matriz[0])):
                filaAntigua.append(matriz[numeroFila][i])
                texto = "\nOperación a realizar: " + str(matriz[numeroFila][i]) + "/" +str(pivote)+ "\n"
                escribir(texto)
                matriz[numeroFila][i] = matriz[numeroFila][i] / pivote
            escribir("Fila Pivote: "+ str(filaAntigua))
            columnaPivoteNueva = matriz[:,estadoSolucionesMultiples[1]]#COLUMNA PIVOTE
            filaPivoteNueva = matriz[numeroFila] 
            escribir("Fila nueva del pivote:"+str(filaPivoteNueva)+"\n")
            filaAntigua = []
            m = 1
            nuevaFila = [] 
            matriz_np[0]= letrasEncabezado
            matriz_np[numeroFila+1,0] = VBNueva
            solucionPivote= crearMatrizFinal(matriz_np,matriz)
            escribir("Nueva matriz: \n"+ solucionPivote)
            #Determina las nuevas filas de la matriz e imprime en consola y en el documento los datos de la nueva matriz
            listaVB[numeroFila-1]= VBNueva
            while m < len(matriz):
                if m != numeroFila:
                    n =0
                    while n < len(filaPivoteNueva):
                        filaAntigua.append(matriz[m][n])
                        texto = "\nOperación a realizar: " + str(matriz[m][n]) + "+" +str(-columnaPivoteNueva[m])+"*"+str(filaPivoteNueva[n])
                        escribir(texto)
                        nuevaFila.append(matriz[m][n]+((-columnaPivoteNueva[m])*filaPivoteNueva[n]))
                        n += 1
                    cambiar_fila(matriz, nuevaFila, m)
                    texto = "\nCambiando Fila: " + str(m+1) +"\nFila Antigua: " + str(filaAntigua) + "\nNueva Fila: " + str(nuevaFila)+ "\nNueva Matriz:\n"+ crearMatrizFinal(matriz_np,matriz)+ "\n\n\n"
                    escribir(texto) 
                    nuevaFila = []  
                    filaAntigua = []
                m += 1

            matrizFinal = []
            listaVBU=  (["U"])
            columnaLetras = []
            columnaLetras.extend(listaVBU)
            columnaLetras.extend(listaVB)
            for i in range(len(matriz)):
                letra = np.array(columnaLetras[i])
                numeros = np.array(matriz[i])
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
            #Imprime la solución extra
            escribir("\nResultado de solución extra:")
            print("Resultado de solución extra:\n")
            print(encabezado)
            escribir(encabezado)
            solucion= determinarSoluciones(columnaLetras[1:], encabezado[1:len(encabezado)-1], matriz) 
            U = matrizFinal[1][len(matrizFinal[1])-1]
            textoFinal =  textoMatriz + "U: "+ str(U)+ "\nSolución:"+ str(solucion)
            print(textoFinal)
            return escribir(textoFinal)

        return escribir(texto)    

    else:   
             
        #columnaMenor es columnaPivote y columnaResultado es el LD 
        #columnaPivoteVariables es la columnaPivote de la matriz que contiene las VB
        columnaMenor = matriz[:,posicionMenorEnColumna]
        columnaResultado = matriz[:,(len(matriz[0]))-1]  
        columnaPivoteVariables = matriz_np[:,posicionMenorEnColumna+1]           
        numeroFila = 0
        textoColumnaPivote = "\nColumna Pivote: "+ str(columnaMenor) 
        #Acá sacamos al pivote y los respectivos valores de la división de LD / columna pivote
        if iteracion == 0:  
            #Pivote es es = 10000 ya que en el caso de la iteración 0, columnaResultado[i] / columnaMenor[i] nunca será menor que 0
            pivote = 10000
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote > (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            numeroFila= i
            tamañoDegenerada = determinarDegenerada(columnaMenor[1:],matriz[1:,len(matriz[0])-1])[1]
            posicionVariablesDegeneradas = determinarDegenerada(columnaMenor[1:],matriz[1:,len(matriz[0])-1])[0]

            if tamañoDegenerada >1 :
                i = 0
                variablesDegeneradas = []
                while i<len(posicionVariablesDegeneradas):
                    variablesDegeneradas.append(matriz_np[posicionVariablesDegeneradas[i]+2,0])
                    i+=1
                print("Las variables degeneradas son: "+ ' '.join(variablesDegeneradas))
                texto = "\nLas variables degeneradas de la matriz actual son: " + ' '.join(variablesDegeneradas)
                escribir(texto)

        elif iteracion >0:
            pivote = 0
            for i in range(len(matriz)):
                if columnaMenor[i] > 0 and (pivote < (columnaResultado[i] / columnaMenor[i])) and ((columnaResultado[i] / columnaMenor[i]) > 0): 
                            pivote = columnaMenor[i]
                            filaPivote = matriz[i]
                            filaPivoteVariables = matriz_np[i+1]
                            #print("\nFila Pivote Matriz_np: "+str(filaPivoteVariables))
                            numeroFila= i
            #Tamaño de la lista de las variables degeneradas
            tamañoDegenerada = determinarDegenerada(columnaMenor[1:],matriz[1:,len(matriz[0])-1])[1]
            posicionVariablesDegeneradas = determinarDegenerada(columnaMenor[1:],matriz[1:,len(matriz[0])-1])[0]
            if tamañoDegenerada >1 :
                #print(tamañoDegenerada)
                i = 0
                variablesDegeneradas = []
                while i<len(posicionVariablesDegeneradas):
                    variablesDegeneradas.append(matriz_np[posicionVariablesDegeneradas[i]+2,0])
                    i+=1
                print("Las variables degeneradas son: "+ ' '.join(variablesDegeneradas))
                texto = "\nLas variables degeneradas de la matriz actual son: " + ' '.join(variablesDegeneradas)
                escribir(texto)
        #No es buena práctica, pero se sobre entiende en caso de los ciclos    
        y = 0
        z = 0
        m = 0
        nuevaFila = [] 
        filaPivoteNueva= []
        filaAntigua = []
        nuevaVB = []
        if numeroFila != 0:
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
                y+=1
            
            texto = "\n\nPivote: " +str(pivote) +textoColumnaPivote+"\nCambiando Fila: Pivote" +"\nFila Pivote: " + str(filaAntigua) + "\nNueva Fila pivote: " + str(filaPivoteNueva) + "\nNueva Matriz:\n"+crearMatrizFinal(matriz_np,matriz)[1:] +  "\n\n\n"
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
                    texto = "\nCambiando Fila: " + str(m+1) +"\nFila Antigua: " + str(filaAntigua) + "\nNueva Fila: " + str(nuevaFila)+ "\nNueva Matriz:\n"+ crearMatrizFinal(matriz_np,matriz)+ "\n\n\n"
                    escribir(texto) 
                    nuevaFila = []  
                    filaAntigua = []
                
                m += 1 
        else:
            print("Matriz no acotada")
            texto = "Tipo de Matriz: No acotada"
            return escribir(texto)
             
            
        
    determinar_solucion(matriz, 1)

def crearMatrizFinal(matrizConLetras,matrizConNumeros):
   #E: Dos matrices, una que contiene las letras y otra de solo números
   #S: Un string de la matriz para imprimirlo en consola y documneto de salida
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
    textoFinal = str(encabezado)+ "\n" + textoMatriz 
    return textoFinal
           
determinar_solucion(matrizATrabajar, 0)
