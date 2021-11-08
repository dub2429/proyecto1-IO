import sys
import random

'''
Generar archivo mochila, recibe el nombre de archivo, capacidad de la mochila, numero de elementos, minimo peso esperado,
maximo peso esperado, minimo beneficio esperado, maximo beneficio esperado, minima cantidad esperada, maxima cantidad
esperada, todos estos anteriores esperados para cada articulo. Devuelve un txt con la cantidad de elementos que se indiquen
y las caracteristicas mencionadas. 
'''
def generar_archivo_mochila(archivo,w,n,minPeso,maxPeso,minBeneficio,maxBeneficio,minCantidad,maxCantidad):
    salida = open(archivo, "x")
    salida.write(w+"\n")
    while(n > 0):
        peso = random.randint(minPeso,maxPeso)
        beneficio = random.randint(minBeneficio,maxBeneficio)
        cantidad = random.randint(minCantidad,maxCantidad)
        elemento = str(peso) + "," + str(beneficio) + "," +str(cantidad)+"\n"
        salida.write(elemento)
        n-=1
    salida.close()

'''
Generar archivo alineamiento, recibe el nombre del archivo para el txt, el largo de la hilera 1 y el largo de la hilera2,
devuelve un txt con dos hileras con las letras A,T,C,G acomodadas aleatoriamente con el largo indicado en la entrada.
'''

'''Main es el controlador, que de acuerdo a la entrada, llama a los metodos indicados por el usuario en terminal'''
def main():
    if sys.argv[1] == "1":
        generar_archivo_mochila(sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9]),int(sys.argv[10]))
        print("Archivo creado correctamente.")
    else:
        print("Problema no encontrado")
main()