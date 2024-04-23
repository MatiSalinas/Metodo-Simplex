
variables = int(input("Cuantas variables tiene la funcion objetivo?\n"))


restricciones = int(input("Cuantas restricciones hay?\n"))

# MAX
# Z = 3"X1"+2"X2"+5"X3"
# R1 X1 + 2X2 + X3 <= 430
# R2 3X1 + 0X2 + 2X2 <= 460
# R1 X1 + 4X2 + 0X3<= 420 


#        Z  |   X1  |   X2  |   X3  |   S1  |   S2  |   S3  |   R
#
#    Z   1  |   -3  |   -2  |   -5  |   0   |   0   |   0   |   0
#   S1   0  |   1   |   2   |   1   |   1   |   0   |   0   |   430
#   S2   0  |   3   |   0   |   2   |   0   |   1   |   0   |   460
#   S3   0  |   1   |   4   |   0   |   0   |   0   |   1   |   420
def crear_tabla(variables,restricciones): # pide los datos de cada variable y armamos una tabla como la de arriba
    tabla = []
    filas = []
    for i in range(1 + restricciones): 
        if i == 0:
            filas.append("Z")
            print('Datos Fila Z')
        else:
            filas.append(f"S{i}")
            print(f"Datos fila S{i}")
        arreglo = []
        for j in range(2 + variables + restricciones):
            if j == 0:
                valorZ = float(input("Ingrese el valor de Z\n"))
                arreglo.append(valorZ)
            elif j <= variables:
                variableX = float(input(f"Ingrese el valor de X{j}\n"))
                arreglo.append(variableX)
            elif j < (1 + variables + restricciones):
                variableS = float(input(f"Ingrese el valor de la variable de holgura S{j-variables}\n"))
                arreglo.append(variableS)
            else:
                r = float(input(f"Ingrese el valor resultado\n"))
                arreglo.append(r)
        tabla.append(arreglo)
    return tabla,filas
    



def imprimir_tabla(lista,filas):
    cadena = ""
    
    for i in range(2 + variables + restricciones): #imprimimos los headers de las columnas
        if i == 0:
            cadena +=  f"   Z      |"
        elif i>0 and i<= variables:
            cadena +=  f"   X{i}  |"
        elif i != len(lista[0])-1:
            cadena += f"    S{i-variables}    |"
        else:
            cadena +=  f"    R  |"
    print(cadena)
    for i,arreglo in enumerate(lista):
        cadena = f"{filas[i]}"
        for numero in arreglo:
            cadena +=  f"   {numero:.1F}  |"
        print(cadena)
        


lista = []

def encontrar_columna_pivote(lista,modo="max"):
    mayor = lista[0][1]
    menor = lista[0][1]
    columnaPivote = 1
    if modo == 'max': # buscamos en las variables el menor numero negativo
        for i in range(variables):
            if menor > lista[0][i+1]:
                menor = lista[0][i+1]
                columnaPivote = i + 1
        if menor >= 0:
            return "Terminado"
        return columnaPivote
    elif modo == 'min': #buscamos el mayor numero positivo
        for i in range(variables):
            if mayor < lista[0][i+1]:
                mayor = lista[0][i+1]
                columnaPivote = i + 1    
        if mayor == 0:
            return "Terminado"
        return columnaPivote

def encontrar_fila_pivote(columna_pivote,lista):
    menor = 999999999999999 #declaramos menor y fila pivote para poder accederlos dentro del for
    filaPivote= 1
    for i in range(1,restricciones+1):
        if lista[i][columna_pivote]>0:
            resultadoCoeficientes = lista[i][-1] / lista[i][columna_pivote]
            if menor > resultadoCoeficientes:
                filaPivote = i
                menor = resultadoCoeficientes
    return filaPivote


def nueva_tabla(columnaPivote,filaPivote,elementoPivote,lista,variablesEntrada):
    filaNueva = []
    variablesSalida = variablesEntrada.copy()
    for numero in lista[filaPivote]:
        filaNueva.append(numero*(1/elementoPivote)) # la fila nueva de entrada

    lista2 = []
    for i,arreglo in enumerate(lista):
        filaAux = []
        operador = arreglo[columnaPivote] * -1
        if i == filaPivote:
            lista2.append(filaNueva)
            variablesSalida[i] = f"X{columnaPivote}"
            continue
        for j,numero in enumerate(arreglo):
            if operador ==0:
                filaAux.append(lista[i][j]) #si la variable ya es 0, entonces pasamos la fila tal cual esta
                
            else:
                valorNuevo = lista[i][j] + operador * filaNueva[j] #Calculamos los nuevos valores de las filas
                filaAux.append(valorNuevo)
        lista2.append(filaAux)
    return lista2, variablesSalida

def resolver(tabla,variables,i,modo = 'max'):
    print(f'Tabla {i}')
    imprimir_tabla(tabla,variables)
    columna1 = encontrar_columna_pivote(tabla,modo=modo)
    if columna1 == 'Terminado' or i>5:
        print('Solucion final')
        return
    else:
        fila1 = encontrar_fila_pivote(columna1,tabla)
        elemento1 = tabla[fila1][columna1]
        tabla2,variablesEntrada2 = nueva_tabla(columna1,fila1,elemento1,tabla,variables)
        i += 1
        resolver(tabla2,variablesEntrada2,i,modo) #Funcion recursiva para resolver la tabla por completo


tabla1,variablesEntrada1 =crear_tabla(variables,restricciones)
resolver(tabla1,variablesEntrada1,1,modo='min')

