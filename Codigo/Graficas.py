from tkinter import Y
import pandas as pd
import numpy as np
from cmath import nan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
from Inumet import Datos_Inumet

def leer_csv(mes):
    #Funcion que abre los archivos CSV
    with open("Resultados/mes " + mes + "/Acumulado diario.csv", encoding="utf-8") as data:
        data =  pd.read_csv(data, encoding="utf-8")
    return data

def cant_de_dias(data):
    fechas = data["Fecha"]
    fechas.drop(fechas.tail(5).index, inplace=True)
    return(fechas.count())

def color_grafica(multi):
    #Funcion que devuelve un color distinto en hexadecimal para cada equipo
    if multi == 0:
        color = "#000000"
    elif multi == 1:
        color = "#0000ff"
    elif multi == 2:
        color = "#00ff00"
    elif multi == 3:
        color = "#2DCB5F"
    elif multi == 4:
        color = "#CF9909"
    elif multi == 5:
        color = "#19C6E9"
    elif multi == 6:
        color = "#A2D9CE"
    elif multi == 7:
        color = "#E91968"
    elif multi == 8:
        color = "#C8AFB9"
    elif multi == 9:
        color = "#E919BD"
    elif multi == 10:
        color = "#007124"
    elif multi == 11:
        color = "#D0A6FF"
    elif multi == 12:
        color = "#936200"
    elif multi == 13:
        color = "#FFA07A"
    elif multi == 14:
        color = "#BDC3C7"
    elif multi == 15:
        color = "#F9E79F" 
    elif multi == 16:
        color = "#E8DAEF"
    elif multi ==17:
        color = "#580065"
    else:
        color = "#ff0000"
    return color

def nombre_abreviado(Nombre):
    #Funcion que pasas el nombre del equipo y devuelve el nombre abreviado
    if Nombre == "Areas_Verdes":
        return "AV"
    elif Nombre == "Lucas_Piriz":
        return "LP"
    elif Nombre == "Museo_Blanes":
        return "MB"
    elif Nombre == "PAGRO":
        return "PA"
    elif Nombre == "CCZ7":
        return "CCZ7"
    elif Nombre == "Casavalle":
        return "PCV"
    elif Nombre == "Giraldez":
        return "PGZ"
    elif Nombre == "La_Paloma":
        return "PLP"
    elif Nombre == "Evaristo_Ciganda":
        return "EC"
    elif Nombre == "Jardín_348":
        return "J348"
    elif Nombre == "Lixiviados":
        return "PL"
    elif Nombre == "Anexo":
        return "AN"
    elif Nombre == "Punta_Carretas":
        return "PC"
    elif Nombre == "CCZ9":
        return "CCZ9"
    elif Nombre == "Colón":
        return "CN"
    elif Nombre == "CCZ18":
        return "CCZ18"
    elif Nombre == "Caif":
        return "CA"
    elif Nombre == "Miguelete":
        return "MI"
    else:
        return "INUMET"
    
def mes_nombre(numero):
    #Funcion que pasas el numero del mes y devuelve el nombre
    if numero == "1":
        return ("Enero")
    elif numero == "2":
        return ("Febrero")
    elif numero == "3":
        return ("Marzo")    
    elif numero == "4":
        return ("Abril")    
    elif numero == "5":
        return ("Mayo")    
    elif numero == "6":
        return ("Junio")    
    elif numero == "7":
        return ("Julio")    
    elif numero == "8":
        return ("Agosto")    
    elif numero == "9":
        return ("Setiembre")    
    elif numero == "10":
        return ("Octubre")
    elif numero == "11":
        return ("Noviembre")    
    else:        
        return ("Diciembre")

def lluvias_historicas(mes):
    #Funcion que lee el archivo donde se encuentran los percentiles historios (Constantes) y devuelve una lista con los percentiles del mes que se paso
    data = pd.read_excel("Codigo/Lluvias_historicas/Lluvias historicas.ods")
    
    columnas = data.columns
    columnas = ["0" , "1" ]
    data.columns = columnas
    
    if mes == "1":
        percentil_25 = round(data["1"][0], 1)
        percentil_50 = round(data["1"][1], 1)
        percentil_75 = round(data["1"][2], 1)
        percentil_100 = round(data["1"][3], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "2":
        percentil_25 = round(data["1"][6], 1)
        percentil_50 = round(data["1"][7], 1)
        percentil_75 = round(data["1"][8], 1)
        percentil_100 = round(data["1"][9], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "3":
        percentil_25 = round(data["1"][12], 1)
        percentil_50 = round(data["1"][13], 1)
        percentil_75 = round(data["1"][14], 1)
        percentil_100 = round(data["1"][15], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "4":
        percentil_25 = round(data["1"][18], 1)
        percentil_50 = round(data["1"][19], 1)
        percentil_75 = round(data["1"][20], 1)
        percentil_100 = round(data["1"][21], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "5":
        percentil_25 = round(data["1"][24], 1)
        percentil_50 = round(data["1"][25], 1)
        percentil_75 = round(data["1"][26], 1)
        percentil_100 = round(data["1"][27], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "6":
        percentil_25 = round(data["1"][30], 1)
        percentil_50 = round(data["1"][31], 1)
        percentil_75 = round(data["1"][32], 1)
        percentil_100 = round(data["1"][33], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "7":
        percentil_25 = round(data["1"][36], 1)
        percentil_50 = round(data["1"][37], 1)
        percentil_75 = round(data["1"][38], 1)
        percentil_100 = round(data["1"][39], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "8":
        percentil_25 = round(data["1"][42], 1)
        percentil_50 = round(data["1"][43], 1)
        percentil_75 = round(data["1"][44], 1)
        percentil_100 = round(data["1"][45], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "9":
        percentil_25 = round(data["1"][48], 1)
        percentil_50 = round(data["1"][49], 1)
        percentil_75 = round(data["1"][50], 1)
        percentil_100 = round(data["1"][51], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "10":
        percentil_25 = round(data["1"][54], 1)
        percentil_50 = round(data["1"][55], 1)
        percentil_75 = round(data["1"][56], 1)
        percentil_100 = round(data["1"][57], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "11":
        percentil_25 = round(data["1"][60], 1)
        percentil_50 = round(data["1"][61], 1)
        percentil_75 = round(data["1"][62], 1)
        percentil_100 = round(data["1"][63], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    if mes == "12":
        percentil_25 = round(data["1"][66], 1)
        percentil_50 = round(data["1"][67], 1)
        percentil_75 = round(data["1"][68], 1)
        percentil_100 = round(data["1"][69], 1)
        lista = [percentil_25, percentil_50, percentil_75, percentil_100]
    return lista
        
def Grafica_doble_masa():
    #Funcion para calcular la grafica de doble masa
    directorios = os.listdir("Dato meses")
    data = leer_csv(directorios[0]) #Leo los datos de inumet de cada mes
    inumet = Datos_Inumet(directorios[0])
    
    data = pd.concat([inumet, data], axis=1, ignore_index=False, sort=False)
    NombresColumnas = data.columns.tolist()
    NombresColumnas.pop(1) #saco la columna de indices
    NombresColumnas.pop(1) #saco la columna de fechas
    fig = plt.figure(figsize=[20,10])
    #Creo una lista con los nombre de los equipos y leo el archivo de acumulado de cada mes, y en cada entrada de la lista voy sumando cuanto fue el valor de cada dia, es decir, que voy haciendo el acumulado en el cuatrimestre de cada equipo
    for k in range(len(NombresColumnas)):
        cantidad_de_dias_totales = 0
        ejeY = []
        ejeX = []
        total = 0
        for i in range(len(directorios)):
            data = leer_csv(directorios[i])
            inumet = Datos_Inumet(directorios[i])
            
            data = pd.concat([inumet, data], axis=1, ignore_index=False, sort=False)
            NombresColumnas = data.columns.tolist()
            NombresColumnas.pop(1) #saco la columna de indices
            NombresColumnas.pop(1) #saco la columna de fechas
            cantidad_de_dias= cant_de_dias(data)
            cantidad_de_dias_totales = cantidad_de_dias + cantidad_de_dias_totales
            ejeX = list(range(1, cantidad_de_dias + 1))
            
            for j in range(cantidad_de_dias):
                if not(pd.isnull(data[NombresColumnas[k]][j])):
                    total = total + float(data[NombresColumnas[k]][j])
                else:
                    total = total + 0
                total = round(total, 2)
                ejeY.append(total)
        #Luego de tener la lista armada con el acumuulado de cada equipo en el cuatrimestre, lo grafico
        ejeX = list(range(1, cantidad_de_dias_totales + 1))
        fig = plt.rcParams["figure.figsize"] = (20, 10)
        fig = plt.plot(ejeX, ejeY, color_grafica(k))
    
    fig = plt.legend(labels = NombresColumnas)
    fig = plt.xlabel("Días")
    fig = plt.ylabel("mm")
    fig = plt.xticks(range(0, cantidad_de_dias_totales + 1, 5))
    fig = plt.grid(True, axis=Y)
    fig = plt.savefig("Informe/Graficas/Grafica doble masa.jpg")
    
def Grafica_acumulado_diario(mes):
    #Funcion para calcular la grafica de Acumulado mensual
    data = leer_csv(mes)
    inumet = Datos_Inumet(mes)
    
    data = pd.concat([inumet, data], axis=1, ignore_index=False, sort=False)
    NombresColumnas = data.columns.tolist()
    NombresColumnas.pop(1) #saco la columna de indices
    NombresColumnas.pop(1) #saco la columna de fechas
    cantidad_de_dias= cant_de_dias(data)
    
    ejeX = list(range(1, cantidad_de_dias + 1))
    fig = plt.figure(figsize=[12,8])
    for j in range(len(NombresColumnas)):
        ejeY = []
        for i in range(cantidad_de_dias):
            if data[NombresColumnas[j]][i] != np.nan:
                ejeY.append(float(data[NombresColumnas[j]][i]))
            else:
                ejeY.append(nan)
        fig = plt.rcParams["figure.figsize"] = (12,8)
        fig = plt.plot(ejeX, ejeY, color_grafica(j))
    
    fig = plt.legend(labels = NombresColumnas)
    fig = plt.xlabel("Dias")
    fig = plt.ylabel("mm")
    fig = plt.xticks(ejeX)
    fig = plt.grid(True, axis=Y)
    fig = plt.savefig("Informe/Graficas/Grafica acumulado diario mes " + mes + ".jpg")
    
def Grafica_Acumulados_mensuales(mes):
    #Funcion para calcular la grafica de Acumulado mensual
    data = leer_csv(mes)
    inumet = Datos_Inumet(mes)
    
    data = pd.concat([data, inumet], axis=1, ignore_index=False, sort=False)
    NombresColumnas = data.columns.tolist()
    
    NombresColumnas.pop(0) #saco la columna de indices
    NombresColumnas.pop(0) #saco la columna de fechas
    cantidad_de_dias= cant_de_dias(data)
    fig = plt.figure(figsize=[12,8])
    ejeX = NombresColumnas
    width = 0.7
    for i in range(len(NombresColumnas)):
        lluvia_total = 0
        for j in range(cantidad_de_dias):
            lluvia_total = lluvia_total + float(data[NombresColumnas[i]][j])
        fig = plt.rcParams["figure.figsize"] = (12, 8)
        fig = plt.bar(nombre_abreviado(NombresColumnas[i]), lluvia_total, width, color = "gray")
    referencias = lluvias_historicas(mes)
    
    for j in range(len(referencias)):
        #Agrego los percentiles del mes
        fig = plt.axhline(y=referencias[j], xmin=0, xmax=1, color = color_grafica(j + 1))
    
    fig = plt.legend(labels = ["Percentil 25%", "Percentil 50%", "Percentil 75%", "Percentil 100%" , mes_nombre(mes)])
    fig = plt.xlabel(" ")
    fig = plt.ylabel("mm")
    fig = plt.savefig("Informe/Graficas/Grafica acumulado mensual mes " + mes + ".jpg")
    



