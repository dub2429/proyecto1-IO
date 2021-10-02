#PROYECTO 1 del curso de Investigación de operaciones
#Instituto Tecnológico de Costa Rica
#Estudiantes: Erick Blanco, David Umaña, Fabián Vives
#Profesor: Carlos gamboa
#Método SIMPLEX

import sys
import numpy as np
from collections import defaultdict


# Función que abre el archivo para obtener la información de las matrices.

def abrir_archivo(file_name):
    archivo = open(file_name, 'r')
    Lineas = archivo.readlines()
    i = 0
    while(i<len(Lineas)):
        Lineas[i] = [int(e) if e.isdigit() else e for e in Lineas[i].split(',')]
        i+=1
    return Lineas



# Variables a utilizar

sols_extra = False 
flagDeg = False

# -h es un parámetro de ingreso opcional
# python solver.py [-h] archivo.txt

if sys.argv[1] == "-h":
    print("El archivo de código fuente a ejecutarse debe llamarse simplex.py \n")
    print("Para ejecutarlo:python simplex.py [-h] (archivo).txt")
    Lineas = abrir_archivo(sys.argv[2])
    out = open("out_"+sys.argv[2], 'w')
else:
    Lineas = abrir_archivo(sys.argv[1])
    out = open("out_"+sys.argv[1], 'w')
    
metodo = Lineas[0][0]
optimizacion = Lineas[0][1]
aVariables = 0  
dVariables = 0
bVariables = Lineas[0][2]
restricciones = int(Lineas[0][3])
matriz = []
degenerada = 0
divisiones = []