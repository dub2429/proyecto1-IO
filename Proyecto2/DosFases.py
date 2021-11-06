
import math 
import numpy as np




#renglonPresentacion construye el i-esimo renglon da la tabla simplex
def construccionRenglon(matrizActividades,vecDispo,n,m,I,faseDoble):
    """
    Se inicializa el renglon co un primer elemento 0 
                    => (0)
    """
    renglon=[0]
    """
    Se agrega n veces el i-esimo elemento del I-esimo renglón de la matriz 
    de actividades 
    """
    for i in range(n):
        renglon.append(matrizActividades[I][i])
    """
    Se agregan m ceros después de los n elementos agregados y un 1 en la posicion I
    """
    
    for i in range(faseDoble):
        for j in range(m):
            if I==j:
                if faseDoble==1:
                    renglon.append(1)
                else:
                    if i==0:
                        renglon.append(-1)
                    else:
                        renglon.append(1)
            else:
                renglon.append(0)
    
    renglon.append(vecDispo[I])
    return renglon
    
#Construccion de la tabla del metodo simplex
def construccionTabla(matrizActividades,Zopt,n,m,vecDispo,faseDoble):
    Tabla=[]
    """
    Se agrega el primer renglón con la cantidad de restricciones que existe
    """
    renglon=[1]
    if faseDoble==1:
        for i in range(n):
            renglon.append(-Zopt[i])
        for i in range((m)+1):
            renglon.append(0)
        Tabla.append(renglon)
    else:
        for i in range(n):
            renglon.append(0)
        for i in range((m)):
            renglon.append(0)
        for i in range((m)):
            renglon.append(1)
        renglon.append(0)
        Tabla.append(renglon)   
    """ 
    Se agrega el i-esimo renglón con m ceros al final y 1 en la i-esima posicion 
    despues del n-simo termino y un cero en la primera posicion
    """
    for i in range(m):
        Tabla.append(construccionRenglon(matrizActividades,vecDispo,n,m,i,faseDoble)) 

    return Tabla
 
def Ajustar(matrizActividades,vecDispo,iguales,n,m,faseDoble):
    AUXmatrizActividades=[]
    AUXvecDispo=[]
    AUXm=m
    for i in range(m):
        if iguales[i]==0:
            auxmatrizActividades=[]
            for j in range(n):
                auxmatrizActividades.append(-matrizActividades[i][j])
            AUXvecDispo.append(-vecDispo[i])
            AUXmatrizActividades.append(auxmatrizActividades)
            auxmatrizActividades=[]
            for j in range(n):
                auxmatrizActividades.append(matrizActividades[i][j])
            AUXvecDispo.append(vecDispo[i])
            AUXmatrizActividades.append(auxmatrizActividades)
            AUXm=m+1                
        elif iguales[i]== -1:
            if faseDoble == 1:
                AUXmatrizActividades.append(matrizActividades[i])
                AUXvecDispo.append(vecDispo[i])
            else:
                for j in range(n):
                    AUXmatrizActividades.append(-matrizActividades[i][j])
                    AUXvecDispo.append(-vecDispo[i])
        elif iguales[i] == 1:
            if faseDoble == 2:
                AUXmatrizActividades.append(matrizActividades[i])
                AUXvecDispo.append(vecDispo[i])
            else:
                for j in range(n):
                    AUXmatrizActividades.append(-matrizActividades[i][j])
                    AUXvecDispo.append(-vecDispo[i])            
        
    return AUXmatrizActividades, AUXvecDispo,AUXm
    

def inicializaSimplex(matrizActividades,Zopt,n,m,vecDispo,iguales,faseDoble):
    
    ResultadoTexto=[]        
    """
    Se le cambian todas las igualdades por dos desigualdades y m aumenta en 1
    por cada cambio
    """
    matrizActividades,vecDispo,m=Ajustar(matrizActividades,vecDispo,iguales,n,m,faseDoble)
    """
    Se toman los valores de la matriz de actividades, el vector de disponibilidad
    y la función objetivo para construir la tabla simplex
    """
    Tabla=construccionTabla(matrizActividades,Zopt,n,m,vecDispo,faseDoble)
    
    if faseDoble==1:
        return Simplex(Tabla, n, m,faseDoble,ResultadoTexto)
    else:
        return DobleFase(Tabla, n, m,faseDoble,Zopt,ResultadoTexto)


def Imprimir_Tabla(Tabla,n,m,faseDoble,H,Resultados,regPivote):
    texto = str(Tabla) + str(n) + str(m), str(faseDoble), str(H), str(Resultados)+ str(regPivote)
    return texto

def Restricciones(Tabla,fase_Doble,m,n):
    
    if fase_Doble==1:
        Zmin = sorted(Tabla[0])
    else:
        Zmin = [Tabla[0][n+(2*m)]]
        
    return Zmin

def Simplex(Tabla,n,m,faseDoble,ResultadoTexto):
    B=[]
    auxB=[]
    auxZ=[]
    Resultados=[]

        
    for i in range(m+1):
        Resultados.append(0)        
    Zmin =Restricciones(Tabla,1,m,n)
    for i in range(m):
        auxz=[]
        for j in range((m)+n+1):
            auxz.append(0)
        auxZ.append(auxz)
    H=0
    AuxTabla=[]
    for i in range(m+1):
        auxTabla=[]
        for j in range((m)+n+2):
            auxTabla.append(str(Tabla[i][j]))
        AuxTabla.append(auxTabla)
    ResultadoTexto=Imprimir_Tabla(Tabla,n,m,1,H,Resultados,-1)
    while Zmin[0] < 0:
        auxB=[]
        B=[]
        TablaControl=[]
        for i in range(m+1):                      
            auxTabla=[]
            for j in range(n+(m)+2):
                auxTabla.append(Tabla[i][j])                
            TablaControl.append(auxTabla)
        if Zmin[0] == Tabla[0][n+(m)+1]:
            aux1=Zmin[1]
        else:
            aux1=Zmin[0]
        for i in range(n+m+1):
            if Tabla[0][i]== aux1:
                colPivote = i
                break
        auxM=0
        for i in range(m+1):
            if i!=0:
                if Tabla[i][colPivote]>0:  
                    B.append(Tabla[i][(m)+n+1]/Tabla[i][colPivote])
                else:
                    B.append(math.inf)
                
                auxM=auxM+1
         
        auxB=sorted(B)
        if auxB[0]==math.inf:
            return auxB
        
        for i in range(auxM):
            if B[i] == auxB[0]:
                    regPivote=i+1
                    
        Resultados[regPivote]= colPivote   

        auxReg=Tabla[regPivote][colPivote]
        for i in range(n+(m)+2):
            Tabla[regPivote][i]=Tabla[regPivote][i]/auxReg
            
        for i in range(m+1):
            auxSimplex =Tabla[i][colPivote]
            for j in range(n+(m)+2):
                if i != regPivote:
                    Tabla[i][j]=Tabla[i][j]-(auxSimplex*Tabla[regPivote][j])
        Zmin = Restricciones(Tabla,1,m,n)
        H=H+1
        control=0
        for i in range(m+1):
            for j in range(n+(m)+2):
                if TablaControl[i][j]!=Tabla[i][j]:
                    control=1
        ResultadoTexto=Imprimir_Tabla(Tabla,n,m,1,H,colPivote,regPivote)
        if control == 0:
            break
        if H == 100:
            break   
        
    Xi=[]
    for i in range(n):
        Xi.append(0)
    
    
    for i in range(m+1):
            if Resultados[i]!=0 and Resultados[i] < n+1 :
                Xi[Resultados[i]-1]=Tabla[i][n+m+1]                                         
    ResultadoTexto=Imprimir_Tabla(Tabla,n,m,1,H,Resultados,-1)
    
    if faseDoble==1:
        return Xi,Tabla[0][n+m+1],ResultadoTexto
    else:
        return Xi,-Tabla[0][n+m+1],ResultadoTexto

def DobleFase(Tabla, n, m,faseDoble,Zopt,ResultadoTexto):
    B=[]
    auxB=[]
    auxZ=[]
    Resultados=[]
    for i in range(m+1):
        Resultados.append(0) 
    
    Zmin = Restricciones(Tabla,1,m,n)
    if Zmin[0]<0:
        zero=1
    else:
        zero=0
    
    
    Zmin = Restricciones(Tabla,faseDoble,m,n)
    
    for i in range(m+1):
        for j in range(n+(2*m)+2):
            if i!=0:
                Tabla[0][j]=Tabla[0][j] - Tabla[i][j]

    
    for i in range(m):
        auxz=[]
        for j in range((faseDoble*m)+n+1):
            auxz.append(0)
        auxZ.append(auxz)
    H=0
    AuxTabla=[]
    for i in range(m+1):
        auxTabla=[]
        for j in range((m*faseDoble)+n+2):
            auxTabla.append(str(Tabla[i][j]))
        AuxTabla.append(auxTabla)    
    ResultadoTexto=Imprimir_Tabla(Tabla,n,m,faseDoble,H,Resultados,-1)
    while Zmin[0] != 0 or zero==1:
        auxB=[]
        B=[]
        TablaControl=[]
        for i in range(m+1):                      
            auxTabla=[]
            for j in range(n+(2*m)+2):
                auxTabla.append(Tabla[i][j])                
            TablaControl.append(auxTabla)
        
        aux = Restricciones(Tabla,1,m,n)
        if aux[0] == Tabla[0][n+(2*m)+1]:
            aux[0]=aux[1]

        for i in range(n+m):
            if Tabla[0][i]==aux[0]:
                colPivote = i
                break
        auxM=0
        for i in range(m+1):
            if i!=0:
                if Tabla[i][colPivote] > 0:  
                    B.append(Tabla[i][(faseDoble*m)+n+1]/Tabla[i][colPivote])
                else:
                    B.append(math.inf)
                
                auxM=auxM+1
         
        auxB=sorted(B)
         
        if auxB[0]==math.inf:
            return auxB
        
        for i in range(auxM):
            if B[i] == auxB[0]:
                    regPivote=i+1
        
        Resultados[regPivote]= colPivote            
        auxReg=Tabla[regPivote][colPivote]
        for i in range(n+(faseDoble*m)+2):
            Tabla[regPivote][i]=Tabla[regPivote][i]/auxReg
            
        for i in range(m+1):
            auxSimplex =Tabla[i][colPivote]
            for j in range(n+(faseDoble*m)+2):
                if i != regPivote:
                    Tabla[i][j]=Tabla[i][j]-(auxSimplex*Tabla[regPivote][j])
        aux = Restricciones(Tabla,1,m,n)
        if aux[0]<0:
            zero=1
        else:
            zero=0        
        Zmin = Restricciones(Tabla,faseDoble,m,n)
        H=H+1
        control=0
        for i in range(m+1):
            for j in range(n+(m*2)+2):
                if TablaControl[i][j]!=Tabla[i][j]:
                    control=1
        if control == 0:
            break
        if H == 100:
            break
                               
    AUXtabla=[] 
    for i in range(m+1):                      
        auxTabla=[]
        for j in range(n+(2*m)+2):
            if j < n+m+1:
                if i==0:
                    if j<n+1:
                        if j ==0:
                            auxTabla.append(1)
                        else:
                            auxTabla.append(Zopt[j-1])
                    else:
                         auxTabla.append(0)
                else:
                    auxTabla.append(Tabla[i][j])
        if i !=0 :            
            auxTabla.append(Tabla[i][n+(2*m)+1])
        else:
            auxTabla.append(0)
        AUXtabla.append(auxTabla)
    ResultadoTexto=Imprimir_Tabla(Tabla,n,m,faseDoble,H,Resultados,regPivote)
    
    for i in range(n+1):
        aux=-AUXtabla[0][i]
        for j in range(n+m+2):
            if i!=0:
                AUXtabla[0][j]=AUXtabla[0][j]+(aux*AUXtabla[i][j])
            
        
    ResultadoTexto=Imprimir_Tabla(Tabla,n,m,faseDoble,H,Resultados,-1)
    return Simplex(AUXtabla, n, m,faseDoble,ResultadoTexto)




def leerDocumento():
    #S: Llama a la función donde se crea la matriz iniciar
    #document = sys.argv[1]
    #print(sys.argv[1])
    with open(str("archivo1.txt")) as documento:
        contenido = documento.read()
    arreglo = contenido.split("\n")
    arregloMatriz = []
    for i in range(len(arreglo)):
        arregloMatriz.append(arreglo[i].split(","))
    return arregloMatriz

datosDocumento = leerDocumento()

#print(datosDocumento)
z = []
m = int(datosDocumento[0][3])
n = int(datosDocumento[0][2])
for i in range(len(datosDocumento[1])):
    z.append(float(datosDocumento[1][i]))

A = []
y = 2
while y < len(datosDocumento):
    temporal = []
    for i in range(len(datosDocumento[y])-2):
        temporal.append(float(datosDocumento[y][i]))
    
    A.append(temporal)
    #print(A)
    y += 1

y = 2  
b = []
while y < len(datosDocumento):
    b.append(float(datosDocumento[y][len(datosDocumento[y])-1]))
    #print(b)
    y += 1

y = 2  
h = []


while y < len(datosDocumento):
    #print(datosDocumento[y][len(datosDocumento[y])-2])
    if datosDocumento[y][len(datosDocumento[y])-2] == "=<" or datosDocumento[y][len(datosDocumento[y])-2] == "<=" or datosDocumento[y][len(datosDocumento[y])-2] == "=":
        h.append(1)
    elif datosDocumento[y][len(datosDocumento[y])-2] == "=>" or datosDocumento[y][len(datosDocumento[y])-2] == ">=":
        h.append(1)
    #print(h)
    y += 1
    
a=inicializaSimplex(A,z,n,m,b,h,2)
print(a)

"""
A= restricciones
z función objetivo
n= número de variables
m= número de restricciones
b= lado derecho
h= símbolos
1 si es maximizar y 2 si es minimizar
"""
