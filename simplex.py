# PROYECTO 1 del curso de Investigación de operaciones
# Instituto Tecnológico de Costa Rica
# Estudiantes: Erick Blanco, David Umaña, Fabián Vives
# Profesor: Carlos gamboa
# Método SIMPLEX

import sys
import numpy as np
from collections import defaultdict


# Función que abre el archivo para obtener la información de las matrices.

def abrir_archivo(file_name):
    archivo = open(file_name, 'r')
    Lineas = archivo.readlines()
    i = 0
    while(i < len(Lineas)):
        Lineas[i] = [int(e) if e.isdigit()
                     else e for e in Lineas[i].split(',')]
        i += 1
    #return Lineas
    print('Lineas> ', Lineas)


# Variables a utilizar para determinar si es degenerada o si existe una solucion extra
extra_sols = False
flagDeg = False

# -h es un parámetro de ingreso opcional
# python solver.py [-h] archivo.txt

if sys.argv[1] == "[-h]":
    print("El archivo de código fuente a ejecutarse debe llamarse simplex.py \n")
    print("Para ejecutarlo:python simplex.py [-h] (archivo).txt")
    Lineas = abrir_archivo(sys.argv[2])
    #nombre_archivo = documento_salida[0]+"_solution.txt"
    out = open(sys.argv[2]+"_solution", 'w')
else:
    Lineas = abrir_archivo(sys.argv[1])
    out = open(sys.argv[1]+"_solution", 'w')

metodo = Lineas[0][0]
optimizacion = Lineas[0][1]
aVariables = 0
dVariables = 0
bVariables = Lineas[0][2]
restricciones = int(Lineas[0][3])
matriz = []
degenerada = 0
divisiones = []


# Función que devuelve una lista de ceros para agregar a la matriz

def listaceros(n):
    return [0] * n

# Esta función hace el trabajo de agregar las variables adicionales


def contar_variables():
    global dVariables, aVariables, bVariables
    i = 2
    for i in range(2, len(Lineas)):
        if Lineas[i][bVariables] == "<=":
            dVariables += 1
        elif Lineas[i][bVariables] == ">=":
            dVariables += 1
            aVariables += 1
        else:
            aVariables += 1

# Esta función se usa para agregar las letras que representan los variables en la matriz, es principalmente destinado a la estética.


def prep_matriz():
    global dVariables, bVariables, aVariables
    temp = ["VB"]
    contar_variables()
    lenght = dVariables+aVariables+bVariables
    count = 1
    while(count < lenght+1):
        if count > (bVariables+dVariables):
            temp.append("r"+str(count-(dVariables+bVariables)))

        elif count > bVariables:
            temp.append("s"+str(count-bVariables))
        else:
            temp.append("x"+str(count))
        count += 1
    # columnaMenor es columnaPivote y columnaResultado es el LD
    temp.append("LD")
    matriz.append(temp)
    len_matrix = restricciones+1
    for i in range(len_matrix):
        temp = listaceros(lenght+2)
        matriz.append(temp)


print(matriz)

# Esta función crea la matriz inicial a partir de las líneas
# del archivo, comprueba el método para los escenarios de casos especiales en la primera línea,
# y si no, simplemente coloca los valores en sus respectivos lugares en la matriz.


def crearMatriz():
    global dVariables, bVariables
    prep_matriz()
    countD = bVariables+1
    countA = bVariables+dVariables+1
    matriz[1][0] = "U"
    i = 1
    while(i < len(Lineas)):
        j = 0
        while(j < len(Lineas[i])):
            if i == 1 and aVariables > 0 and metodo == 1:
                matriz[i][j+1] = float(Lineas[i][j])
                k = countA
                while(k < len(matriz[1])-1):
                    if optimizacion == "max":
                        matriz[1][k] = -1000
                    else:
                        matriz[1][k] = 1000
                    k += 1
            elif i == 1 and aVariables > 0 and metodo == 2:
                matriz[i][j+1] = float(Lineas[i][j])
                k = 1
                while(k < len(matriz[1])-1):
                    if(k < bVariables + dVariables + 1):
                        matriz[1][k] = 0
                    else:
                        matriz[1][k] = -1
                    k += 1
            elif i == 1:
                matriz[i][j+1] = -1*float(Lineas[i][j])
            elif Lineas[i][j] == "<=":
                matriz[i][0] = matriz[0][countD]
                matriz[i][countD] = 1
                countD += 1
            elif Lineas[i][j] == ">=":
                matriz[i][0] = matriz[0][countA]
                matriz[i][countD] = -1
                countD += 1
                matriz[i][countA] = 1
                countA += 1
            elif Lineas[i][j] == "=":
                matriz[i][0] = matriz[0][countA]
                matriz[i][countA] = 1
                countA += 1
            elif j == len(Lineas[i])-1 and i != 1:
                matriz[i][-1] = float(Lineas[i][j])
            else:
                matriz[i][j+1] = float(Lineas[i][j])
            j += 1
        i += 1

# print(Lineas)


# Función que inicializa el método simplex

def inic_simplex():
    out.write(""+"\n")
    out.write("Matriz Inicial"+"\n")
    print("")
    print("Matriz Inicial")
    out.write(matriz_string()+"\n")
    print(matriz_string())
    simplex(1)


# Funcion que retorna la matriz final en pantalla o los casos especiales, además de llamar la función de escribir
def simplex(iteracion):

    valor_neg_min = varNeg()

    # Cuando no hay variables negativas, el método símplex finaliza
    if valor_neg_min[0] == None:
        soluciones_extra()
        impr_sol()
        return 0

    else:
        restriccion = determinar_restriccion(valor_neg_min[2], iteracion)

        # Cuando hay una restricción inelegible, significa que no hay solución con simplex
        if restriccion[0] == None:
            out.write("Tipo de Matriz: No acotada"+"\n")
            print("Tipo de Matriz: No acotada")

        else:
            # Imprime la iteración actual y grafica el estado actual de la matriz
            out.write("Variable básica que entra: " + valor_neg_min[0]+"\n")
            out.write("Variable básica que sale: " + restriccion[0]+"\n")
            out.write("Número Pivote: " +
                      str(matriz[restriccion[2]][valor_neg_min[2]])+"\n")

            print("")
            print("Variable básica que entra: " + valor_neg_min[0])
            print("Variable básica que sale: " + restriccion[0])
            print("Número Pivote:: " +
                  str(matriz[restriccion[2]][valor_neg_min[2]]))

            matriz[restriccion[2]][0] = valor_neg_min[0]
            op_filas(valor_neg_min[2], restriccion[2])
            print("")
            out.write(""+"\n")
            out.write(matriz_string()+"\n")
            print(matriz_string())

            return simplex(iteracion + 1)


def varNeg():
    # La respuesta tiene la forma [variable, valor, número de columna]
    res = [None, 0, 0]
    var_cant = len(matriz[0]) - 1
    i = 1

    # Revisa las variables para encontrar si existe un negativo
    while i < var_cant:
        if matriz[1][i] <= res[1] and matriz[1][i] != 0:
            res = [matriz[0][i], matriz[1][i], i]
        i = i + 1

    return res


def determinar_restriccion(valor_neg_min, iteracion):
    global flagDeg
    divisiones = []
    # La respuesta tiene la forma [restricción, división con el resultado del valor minimo negativo, número de fila]
    res = [None, 0, 0]
    cant_res = len(matriz)  # Determina ctd. de restricciones
    i = 1
    while i < cant_res:
        if matriz[i][valor_neg_min] > 0 and matriz[i][-1] >= 0:
            res_div = matriz[i][-1]/matriz[i][valor_neg_min]
            divisiones.append(matriz[i][-1]/matriz[i][valor_neg_min])
            # Si es la primera división, se pone como respuesta
            if res[0] == None:
                res = [matriz[i][0], res_div, i]

            else:
                # revisa si la division es mejor a la respuesta actual
                if res_div < res[1]:
                    res = [matriz[i][0], res_div, i]

        i = i + 1
    if divisiones != [] and divisiones.count(min(divisiones)) > 1:
        flagDeg = True
        degenerada = iteracion
    return res

# Esta función se utiliza para aplicar las operaciones necesarias en la matriz para la iteración


def op_filas(valor_neg_min, restriccion):
    row_amount = len(matriz)
    column_amount = len(matriz[0])
# Calcula el multiplicativo inverso del valor valor_neg_min en la restricción elegida para multiplicarlos y asegurarse de que el resultado sea 1
    inverse_multiplicative = 1/matriz[restriccion][valor_neg_min]
    j = 1


# Multiplica la fila de restricción elegida por el multiplicativo inverso
    while j < column_amount:
        matriz[restriccion][j] = matriz[restriccion][j] * \
            inverse_multiplicative
        j = j + 1

    i = 1

# Va a través de la matriz, haciendo que la columna valor_neg_min sea 0 (excepto la restricción elegida)
    while i < row_amount:

        if i != restriccion:
            j = 1
            multiplier = - matriz[i][valor_neg_min]

            while j < column_amount:
                matriz[i][j] = round(matriz[restriccion][j]
                                     * multiplier + matriz[i][j], 2)
                j = j + 1

        i = i + 1


# Función que devuelve una cadena con una matriz en forma de tabla.

def matriz_string():
    res = ""

    for line in matriz:

        for rengl in line:
            rengl_largo = len(str(rengl))
            if rengl_largo > 6:
                rengl_largo = 6
            res = res + ('%.6s' % str(rengl))
            VACIO = 8 - rengl_largo
            res = res + (" " * VACIO)
        res = res + "\n"

    return res


'''
def Imprimir_Tabla(Tabla,n,m,faseDoble,H,Resultados,regPivote):
    texto = str(Tabla) + str(n) + str(m), str(faseDoble), str(H), str(Resultados)+ str(regPivote)
    return texto
'''

# Función que imprime la solución final de la matriz, también comprueba si la respuesta es degenerada


def impr_sol():
    if flagDeg:
        out.write(""+"\n")
        print("")
        out.write("Solución Degenerada"+"\n")
        print("Solución Degenerada")
    if extra_sols:
        out.write(""+"\n")
        print("")
        out.write("Solución Multiple"+"\n")
        print("Solución Multiple")
    if not extra_sols and not flagDeg:
        print("")
        out.write(""+"\n")
        out.write("Solución"+"\n")
        print("Solución")
    print("")
    out.write(""+"\n")
    out.write("Valor de las variables:"+"\n")
    print("Valor de las variables:")
    res = {}
    # Encuentra las variables
    for column in matriz[0]:
        if column[0] == "x" or column[0] == "s" or column[0] == "r":
            res[column] = 0

    # Encuentra las variables
    for fila in matriz[1:]:
        if fila[0][0] in ["x", "U", "r", "s"]:
            res[fila[0]] = fila[-1]

    if optimizacion == "min" and metodo != 0:
        res["U"] *= -1
    #Imprime variables
    for variable in sorted(res.keys()):
        out.write(variable + " = " + str(res[variable])+"\n")
        print(variable + " = " + str(res[variable]))

    out.write("Valor óptimo de U es: "+"\n")
    print("Valor óptimo de U es: ")
    out.write("U = " + str(res["U"])+"\n")
    print("U = " + str(res["U"]))
    if metodo != 2:
        out.close()

# Función encargada de resolver la matriz mediante el metodo de la gran M

# Esta función se usa para encontrar el número 1 en la misma columna de M para hacer M 0.


def encontrar_fila(column):
    i = 0
    while(i < len(matriz)):
        if matriz[i][column] == 1:
            break
        i += 1
    return i


# Esta función se utiliza para mostrar las operaciones para hacer M 0.

def conv_m_ceros():
    if optimizacion == "max":
        j = 1
        while(j < len(matriz[1])):
            matriz[1][j] *= -1
            j += 1
    out.write(""+"\n")
    out.write(matriz_string()+"\n")
    print("")
    print(matriz_string())
    countA = bVariables+dVariables+1
    while(countA < len(matriz[0])-1):
        fila = encontrar_fila(countA)
        multiplier = -matriz[1][countA]
        i = 1
        while(i < len(matriz[0])):
            matriz[1][i] = matriz[fila][i] * multiplier + matriz[1][i]
            i = i + 1
        countA += 1
    inic_simplex()


# Metodo 2 fases

# Esta función se utiliza para trabajar sobre la primera fase del método de dos fases, fija la primera
# fila girando a cero los valores necesarios y luego aplica simplex y verifica el resultado final
# de la fase para comprobar si puede continuar o no a la segunda fase.


def PrimeraFase():
    global dVariables
    conv_r_ceros()
    j = 1
    while(j < len(matriz[1])):
        matriz[1][j] *= -1
        j += 1
    inic_simplex()
    if matriz[1][-1] == 0:
        SegundaFase()
    else:
        out.write("No es posible solucionar este problema.")
        print("No es posible solucionar este problema.")


# Esta función se utiliza para encontrar las variables artificiales y agrega las filas en las que se encuentran
# la primera fila de la respuesta, esto es necesario para la segunda fase del método de dos fases


def conv_r_ceros():
    i = 2
    while(i < len(matriz)):
        if(matriz[i][0][0] == 'r'):
            j = 1
            while(j < len(matriz[0])):
                matriz[1][j] = matriz[1][j] + matriz[i][j]
                j += 1
        i += 1


# Esta función se utiliza para trabajar sobre la segunda fase del método de dos fases, transforma la
# matriz eliminando las variables artificiales y colocando la primera línea original en la matriz.
# Posteriormente busca los valores que tiene que convertir a cero y aplica simplex para obtener el resultado final.
# respuesta.
'''
def Restricciones(Tabla,fase_Doble,m,n):
    
    if fase_Doble==1:
        Zmin = sorted(Tabla[0])
    else:
        Zmin = [Tabla[0][n+(2*m)]]
        
    return Zmin
'''


def SegundaFase():
    global dVariables, bVariables
    i = 0
    while(i < len(matriz)):
        j = 0
        while(j < dVariables):
            matriz[i].pop(bVariables + dVariables + 1)
            j += 1
        i += 1

    i = 1
    while(i <= bVariables):
        matriz[1][i] = -1*float(Lineas[1][i-1])
        i += 1

    i = 2
    while(i < len(matriz)):
        j = 1
        multiplier = abs(matriz[1][matriz[i].index(1)])
        while(j < len(matriz[1])):
            matriz[1][j] = round(
                round(matriz[i][j] * multiplier, 2) + matriz[1][j], 2)
            j += 1
        i += 1
    j = 1
    while(j < len(matriz[1])):
        matriz[1][j] *= -1
        j += 1
    print(matriz_string())
    inic_simplex()


# Funcion que calcula al menos una solucion extra

def soluciones_extra():
    global extra_sols
    for i in range(bVariables+1, len(matriz[1])):
        if matriz[1][i] == 0:
            extra_sols = True


def sacar_parametros(matriz):
    #E: La matriz del archivo de configuracion
    #S: La matriz sin los parametros de la primer linea
    u = matriz[0]
    resultado = matriz[1:]
    resultado = resultado+[u]
    return resultado


def convertir_dual(matriz):
    #E: La matriz dual
    #S: saca la funcion objetivo U
    swapU = sacar_parametros(matriz[1:])
    return swapU


def sacar_restricciones(matriz):
    #E: La matriz
    #S: La matriz pero sin la columna de los signos de restriccion
    largo = len(matriz)
    for i in range(0, largo-1):
        # Para agarrar solo la penultima columna de las restricciones
        tmp = matriz[i][-1]
        matriz[i] = matriz[i][:-2]+[tmp]

    return matriz


def agregar_nuevas_restricciones(matriz, restricciones):
    #E: La matriz, las muevas restricciones a cambiar para el problema dual
    #S: La matriz con los nuevos signos de restriccion
    largo = len(matriz)
    for i in range(0, largo):
        tmp1 = matriz[i][-1:]
        tmp2 = matriz[i][:-1]
        matriz[i] = tmp2+[restricciones[i]]+tmp1

    return matriz


def transpuesta(matriz_primalX):
    #E: La matriz primal a convertir
    #S: La nueva matriz dual (transpuesta de primal)
    resultado = [[matriz_primalX[j][i] for j in range(
        len(matriz_primalX))] for i in range(len(matriz_primalX[0]))]
    return resultado


def problema_dual(matriz_primal):
    #E: Recibe la matriz primal
    # S: La matriz convertida a dual para aplicar algun metodo

    print('Matriz primal: \n', matriz_primal, '\n')

    # Saca el signo de restriccion
    signo_restriccion = matriz_primal[2][len(matriz_primal[2])-2]
    signo_restriccion_nuevo = ' '

    if signo_restriccion == '<=':
        signo_restriccion_nuevo = '>='
    else:
        signo_restriccion_nuevo = '<='

    print('Signo restriccion: ', signo_restriccion)
    print('Signo restriccion nuevo: ', signo_restriccion_nuevo, '\n')
    matriz_dual = matriz_primal

    params = matriz_dual[0]  # Se guardan los parametros
    u = matriz_dual[1]  # Se guarda la funcion U de la matriz primal
    matriz_dual = convertir_dual(matriz_dual)
    matriz_dual = sacar_restricciones(matriz_dual)
    cont = 0
    # Diferencia del tamano de columnas
    diferencia = (len(matriz_dual[1]))-(len(u))
    agregarAU = len(matriz_dual)
    print('Len diferencia: ', diferencia)
    while (cont <= diferencia-1):
        matriz_dual[agregarAU-1].append('0')
        cont += 1
        print(cont)

    matriz_dual = transpuesta(matriz_dual)

    # Se guarda la nueva funcion objetico del problema dual
    w = matriz_dual[(len(matriz_dual)-1)]

    # Se guarda la matriz dual sin la funcion objetivo
    matriz_dual_sinW = matriz_dual[:-1]

    varDecision = params[2]
    restricciones = params[3]
    # Intercambiar restricciones y variables de decision para W
    params[2] = restricciones
    params[3] = varDecision

    restricciones_signo = []
    cant_restricciones = params[3]
    print('Cantidad restrcciones nuevas: ', cant_restricciones)
    cant = 1
    # Para sacar la nueva cant de restricciones que va tener el problema dual
    while cant <= int(cant_restricciones):
        restricciones_signo.append(signo_restriccion_nuevo)
        cant += 1

    # Se agregan las nuevas restricciones a la matriz
    matriz_dual = agregar_nuevas_restricciones(
        matriz_dual_sinW, restricciones_signo)

    # Se agrega la fila con la funcion objetivo w al inicio de la matriz
    matriz_dual = [w]+matriz_dual

    print('\n Matriz Dual Resultante: \n', matriz_dual)
    matrizResultante_Dual = [params]+matriz_dual

    print('\n Matriz Dual Resultante: \n', matriz_dual)

    return matrizResultante_Dual

# Funcion main que recibe  métodos utilizados en este proyecto con Gran M, Dos Fases y Dual,
# indicados en el archivo de configuración con los indices 1 para la gran M, 2 para
# Dos Fases, y 3 para Dual.


if metodo == 0:
    crearMatriz()
    inic_simplex()
elif metodo == 1:
    crearMatriz()
    conv_m_ceros()
elif metodo == 2:
    crearMatriz()
    PrimeraFase()
# elif metodo ==3:
    problema_dual(Lineas)

"""
A= restricciones
z función objetivo
n= número de variables
m= número de restricciones
b= lado derecho
h= símbolos
1 si es maximizar y 2 si es minimizar
"""
