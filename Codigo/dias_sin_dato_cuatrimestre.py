import pandas as pd
import os

#Funcion que devuelve un excel con los dias sin dato por pluviometro de todo el cuatrimestre
def dias_sin_dato():
    num_mes = os.listdir("Dato meses")
    primera_carpeta = True
    for i in range(len(num_mes)):
        contenido = os.listdir("Resultados/mes " + num_mes[i])
        for archivo in contenido:
            #Voy al archivo de acumulado diario de cada mes, donde tengo los dias sin datos de ese mes ya contados
            #Y lo que hago es una lista con los nombres de cada pluviometro y los valores del primer mes
            #Y luego para los siguientes meses, voy recorriendo, sumando en cada uno y acumulando el total
            if  archivo.endswith('.csv') and archivo.startswith("Acumulado diario"):
                with open("Resultados/mes " + num_mes[i] + "/Acumulado diario.csv", encoding="utf-8") as archivo:
                    ar =  pd.read_csv(archivo, encoding="utf-8")
                    ar = ar.tail(1)
                    ar = ar.drop(["Unnamed: 0","Fecha"], axis=1)
                    if primera_carpeta:
                        NombresColumnas = ar.columns.tolist()
                        primera_carpeta= False
                        tabla_final = ar   
                    else:
                        for k in range(len(NombresColumnas)):
                            x = tabla_final[NombresColumnas[k]]
                            y = ar[NombresColumnas[k]]
                            x = int(float(x))
                            y = int(float(y))
                            tabla_final[NombresColumnas[k]] = x + y 
    #Exporto a un archivo CSV
    tabla_final.to_csv("Resultados/dias_sin_dato_cuatrimestre.csv", encoding="utf-8")
                           