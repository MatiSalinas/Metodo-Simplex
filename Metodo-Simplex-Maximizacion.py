
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
def crear_tabla(variables,restricciones):
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
    
    for i in range(2 + variables + restricciones):
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

def encontrar_columna_pivote(lista):
    menor = lista[0][1]
    columnaPivote = 1
    for i in range(variables):
        if menor > lista[0][i+1]:
            menor = lista[0][i+1]
            columnaPivote = i + 1
    if menor > 0:
        return "Terminado"
    return columnaPivote

def encontrar_fila_pivote(columna_pivote,lista):
    menor = 999999999999999
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
        filaNueva.append(numero*(1/elementoPivote))

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
                filaAux.append(lista[i][j]) 
                
            else:
                valorNuevo = lista[i][j] + operador * filaNueva[j]
                filaAux.append(valorNuevo)
        lista2.append(filaAux)
    return lista2, variablesSalida

tabla1,variablesEntrada1 =crear_tabla(variables,restricciones)
print('Tabla1')
imprimir_tabla(tabla1,variablesEntrada1)

columna1 = encontrar_columna_pivote(tabla1)
fila1 = encontrar_fila_pivote(columna1,tabla1)
elemento1 = tabla1[fila1][columna1]
tabla2,variablesEntrada2 = nueva_tabla(columna1,fila1,elemento1,tabla1,variablesEntrada1)

print("Tabla 2")
imprimir_tabla(tabla2,variablesEntrada2)
columna2 = encontrar_columna_pivote(tabla2)
fila2 = encontrar_fila_pivote(columna2,tabla2)
elemento2 = tabla2[fila2][columna2]

tabla3,variablesEntrada3 = nueva_tabla(columna2,fila2,elemento2,tabla2,variablesEntrada2)

print("Tabla 3")
imprimir_tabla(tabla3,variablesEntrada3)

