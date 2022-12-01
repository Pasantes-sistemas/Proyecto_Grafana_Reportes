import pandas as pd
import datetime as dt
import numpy as np
import os

def Procesamiento(ar, Nombre_fin, Columna):
    #TODO: Funcion para depurar los datos crudos
    #region SECTION Seccion 1:
    #* En esta seccion se eliminan todas las filas que no contengan datos (datos vacios), 
    #* ya que, como en los archivos con los datos crudos se encuentras todos los equipos juntos, 
    #* en un intervalo de 5 min cada equipo tiene su propio dato con su repectiva hora y fecha, 
    #* lo que crea un monton de datos vacios que molestan para trabajar, por esto primero se eliminan
    
    CantFilas = ar["Fecha"].count()
    #* Creo una tabla donde guardo los datos luego de eliminar los vacios
    ardepurado = pd.DataFrame({"Fecha" : [], "Dato acumulado" : []})
    ar[Columna] = round(ar[Columna], 2)
    
    tresmin = dt.timedelta(minutes=3)
    #* Paso la columna fecha a tipo datetime y lo guardo en fechatiempo
    fechatiempo = pd.to_datetime(ar["Fecha"])
    hay_que_eliminar = True
    
    #TODO: For que saca los datos nulos extra y guarda las filas con datos en ardepurado
    for i in range(CantFilas - 1): 
        if hay_que_eliminar:
            resta = fechatiempo[i + 1] - fechatiempo[i] 
            if pd.isnull(ar[Columna][i]):
                #* Si entre una fila y otra hay mas datos vacios los elimino
                if (resta < tresmin):
                    x=9
                else:
                    nuevafila = pd.DataFrame({"Fecha": [ar["Fecha"][i]], "Dato acumulado": [np.NaN]})
                    ardepurado = pd.concat([ardepurado, nuevafila], sort=False, ignore_index=True)
            else:
                if (resta < tresmin):
                    #* Copio las filas que hay datos
                    if pd.isnull(ar[Columna][i+1]):
                        hay_que_eliminar = False
                nuevafila = pd.DataFrame({"Fecha": [ar["Fecha"][i]], "Dato acumulado": [ar[Columna][i]]})
                ardepurado = pd.concat([ardepurado, nuevafila], sort=False, ignore_index=True)
        else:
            hay_que_eliminar = True
    
    #* Me falta pasar la ultima fila
    if hay_que_eliminar:
        if pd.isnull(ar[Columna][i + 1]):
            nuevafila = pd.DataFrame({"Fecha": [ar["Fecha"][i + 1]], "Dato acumulado": [np.NaN]})
            ardepurado = pd.concat([ardepurado, nuevafila], sort=False, ignore_index=True)
        else:
            nuevafila = pd.DataFrame({"Fecha": [ar["Fecha"][i + 1]], "Dato acumulado": [ar[Columna][i + 1]]})
            ardepurado = pd.concat([ardepurado, nuevafila], sort=False, ignore_index=True)

    #endregion

    #region SECTION Seccion 2:
    #* En esta seccion se van a agregar los datos Na cuando haya datos vacios o saltos temporales de mas de 10 minutos sin dato

    #*Creo una nueva tabla para guardar los datos con los na incluidos
    CantFilas = ardepurado["Fecha"].count()
    arNa = pd.DataFrame({"Fecha" : [], "Dato acumulado" : []})
    
    #* Paso la columna fecha a tipo datetime y lo guardo en fechatiempo
    fechatiempo = pd.to_datetime(ardepurado["Fecha"])

    #* Defino las variables temporales 
    diesmin = dt.timedelta(minutes=10 , seconds=59)
    cincomin = dt.timedelta(minutes=5)
        
    for i in range(CantFilas - 1):
        #* Diferencia temporal entre el dato actual y el siguiente
        resta = fechatiempo[i + 1] - fechatiempo[i] 

        #* Crea una fila al final de arNa con el dato de la fila i de archivo
        nuevafila = pd.DataFrame({"Fecha": [ardepurado["Fecha"][i]], "Dato acumulado": [ardepurado["Dato acumulado"][i]]})
        arNa = pd.concat([arNa, nuevafila], sort=False, ignore_index=True)
        
        cincominaux = dt.timedelta(minutes=5)
        if (resta > diesmin): 
            #* Si pasan mas de 10 min entre dos datos, lleno cada 5 min con Na 
            
            if (ardepurado["Dato acumulado"][i] > 50) or (ardepurado["Dato acumulado"][i] < 0):
                #* Cuando 50mm > datos o datos > 0 cambio el dato i copiado por Na ya que pasaron mas de 10 min y el dato es atipico
                arNa["Dato acumulado"][i] = "Na"
                
            resta = resta - cincomin
            while resta > cincomin:    
                #* Creo una nueva fila en arfin y le asigno en fecha: fechatiempo + 5 y en dato Na
                #* Mientras siga habiendo diferencia mayor a 5 min, resto 5 min a resta
                
                fechasum = cincominaux + fechatiempo[i]
                
                #* Agrego fila
                nuevafila = pd.DataFrame({"Fecha": [fechasum], "Dato acumulado": ["Na"]})
                arNa = pd.concat([arNa, nuevafila], sort=False, ignore_index=True)
                
                cincominaux = cincominaux + cincomin
                resta = resta - cincomin
                
    if not(pd.isnull(ardepurado["Dato acumulado"][i + 1])):
        #* Cuando sale del for le falta copiar siempre la ultima fila de ardepurado
        nuevafila = pd.DataFrame({"Fecha": [ardepurado["Fecha"][i + 1]], "Dato acumulado": [ardepurado["Dato acumulado"][i + 1]]})
        arNa = pd.concat([arNa, nuevafila], sort=False, ignore_index=True)
    else:
        nuevafila = pd.DataFrame({"Fecha": [ardepurado["Fecha"][i + 1]], "Dato acumulado": ["Na"]})
        arNa = pd.concat([arNa, nuevafila], sort=False, ignore_index=True)    


    CantFilas = arNa["Fecha"].count()
    for i in range(CantFilas): 
        #* Termino de poner los Na
        if pd.isnull(arNa["Dato acumulado"][i]):
            arNa["Dato acumulado"][i] = "Na"
    #endregion
    
    #region SECTION Seccion 3:
    #* En esta seccion, creo la columna dato instantaneo
    
    tiempo_reset_min = dt.time(hour=23, minute=55, second=59)   
    primer_dato = False
    datoref = 0
    arinst = pd.DataFrame({"Fecha" : [], "Dato acumulado" : [], "Dato instantaneo": []})
    
    for i in range(CantFilas):
        if arNa["Dato acumulado"][i] == "Na":
            #* Si el acumulado es Na lo dejo igual
            nuevafila = pd.DataFrame({"Fecha": [arNa["Fecha"][i]], "Dato acumulado": [arNa["Dato acumulado"][i]], "Dato instantaneo" : ["Na"]})
            arinst = pd.concat([arinst, nuevafila], sort=False, ignore_index=True) 
        else:
            if primer_dato:
                #* Variable de tiempo y hora de dato actual y siguiente
                fechai = pd.to_datetime(arNa["Fecha"][i])
                tiempoi = fechai.time()
                fechaiant = pd.to_datetime(arNa["Fecha"][i - 1])
                fechai = fechai.date()
                fechaiant = fechaiant.date()
                if (fechai == fechaiant) & (tiempoi < tiempo_reset_min):
                    #* Mientras se mantenga en el mismo dia y sea menor que las 23:55, hago la resta del acumulado actual menos el valor de referencia
                    datoinst = arNa["Dato acumulado"][i] - datoref
                    datoref = arNa["Dato acumulado"][i]
                elif (tiempoi > tiempo_reset_min) & (arNa["Dato acumulado"][i] == arNa["Dato acumulado"][i - 1]):
                    #* El elif se agrego ya que hay veces que no reinicia el contador de datos acumulados entre las 23:55 del dia actual y las 00:00 del siguiente dia
                    #* por lo tanto, este elif toma ese caso y le pone el mismo valor que el dato instantaneo anterior
                    datoinst = arinst["Dato instantaneo"][i - 1]
                else:
                    #* Cuando se reinicia el contador de acumulados cuando cambia de dia o pasan las 23:55, el primer dato del dia es el valor de referencia
                    datoinst = arNa["Dato acumulado"][i]
                    datoref = datoinst  
            else:
                #* Para el primer dato de la serie
                datoref = arNa["Dato acumulado"][i]
                datoinst = arNa["Dato acumulado"][i]
                primer_dato = True
                
            #* Agrego fila
            nuevafila = pd.DataFrame({"Fecha": [arNa["Fecha"][i]], "Dato acumulado": [arNa["Dato acumulado"][i]], "Dato instantaneo" : [round(datoinst, 2)]})
            arinst = pd.concat([arinst, nuevafila], sort=False, ignore_index=True)
    
    outliers = pd.DataFrame({"Outlier - fila": [], "Dato instantaneo": []})
    #* Saco los datos negativos y los que pasen los 50mm (outliers), ya que se consideran atipicos
    for i in range(CantFilas):
        if arinst["Dato instantaneo"][i] != "Na":
            if arinst["Dato instantaneo"][i] < 0:
                arinst["Dato instantaneo"][i] = 0
            if arinst["Dato instantaneo"][i] > 50:
                nuevo_outlier = pd.DataFrame({"Outlier - fila": [i], "Dato instantaneo": [arinst["Dato instantaneo"][i]]})
                outliers = pd.concat([outliers, nuevo_outlier], sort=False, ignore_index=True)
                arinst["Dato instantaneo"][i] = "Outliers"

    #endregion

    #region SECTION Seccion 4:
    #* En esta seccio, creo los contadores de dias con lluvia, dias sin lluvias y dias sin datos y los guardo en una columna nueva para cada dato

    Contadores = pd.DataFrame({"Cantidad de dias con lluvia": [0], "Cantidad de dias sin lluvia": [0], "Cantidad de dias sin datos": [0]})
    
    #* Cant de dias con lluvia
    #* Cuando el dato inst > 0,1 y != Na o hay acumulado, entonces hay lluvia
    cont_lluvias = 0
    veinticuatroh = dt.timedelta(days=1)
    fecha_ultima_lluvia = pd.to_datetime(arinst["Fecha"][0])
    fecha_ultima_lluvia = fecha_ultima_lluvia.date()
    fecha_ultima_lluvia = fecha_ultima_lluvia - veinticuatroh

    for i in range(CantFilas):
        fecha = pd.to_datetime(arinst["Fecha"][i])
        fecha = fecha.date()
        if arinst["Dato instantaneo"][i] != "Na":
            #* Si la fecha de la ultima lluvia es distinta a la actual y el dato es de lluvia, se suma 1 al contador
            if (arinst["Dato instantaneo"][i] == "Outliers"):
                if(fecha_ultima_lluvia != fecha):
                    cont_lluvias = cont_lluvias + 1
                    fecha_ultima_lluvia = fecha
            elif (arinst["Dato instantaneo"][i] > 0.1):
                if (fecha_ultima_lluvia != fecha):
                    cont_lluvias = cont_lluvias + 1
                    fecha_ultima_lluvia = fecha
    
    #* Cant de dia sin datos
    cont_no_dato = 0
    encontro_dato = False
    fecha_anterior = pd.to_datetime(arinst["Fecha"][0])
    fecha_anterior = fecha_anterior.date()
    fechas_sin_dato = pd.DataFrame({"Fecha sin dato": []})
    
    
    for i in range(CantFilas):
        fecha_actual = pd.to_datetime(arinst["Fecha"][i])
        fecha_actual = fecha_actual.date()
        if fecha_actual != fecha_anterior:
            #* Si cambio de dia y no encuentro dato (Encuentro dato = false), ahi se que en el dia anterior a la fecha actual no hubo dato
            #* Si encuentra un dato en el dia, no cuenta
            if not(encontro_dato):
                cont_no_dato = cont_no_dato + 1
                fechas_sin_d = fecha_actual + dt.timedelta(days=-1)
                nuevafecha = pd.DataFrame({"Fecha sin dato": [fechas_sin_d]})
                fechas_sin_dato = pd.concat([fechas_sin_dato, nuevafecha], sort=False, ignore_index=True) 
                encontro_dato = False
                fecha_anterior = fecha_actual
            else:
                encontro_dato = False
                fecha_anterior = fecha_actual
        if arinst["Dato instantaneo"][i] != "Na":
            encontro_dato = True
    if not(encontro_dato):
        #* Este if solo para el ultimo dato de la serie, si el ultimo dia de la serie no hay dato tambien suma 
        cont_no_dato = cont_no_dato + 1
        fechas_sin_d = fecha_actual
        nuevafecha = pd.DataFrame({"Fecha sin dato": [fechas_sin_d]})
        fechas_sin_dato = pd.concat([fechas_sin_dato, nuevafecha], sort=False, ignore_index=True) 
    
    #* Cant de dia sin lluvia
    #* Para saber este dato, total de dias - cantidad de dias sin datos - cantidad de dias con lluvia    
    fechainicial = pd.to_datetime(arinst["Fecha"][0])
    fechainicial = fechainicial.date()
    fechafinal = pd.to_datetime(arinst["Fecha"][CantFilas - 1])
    fechafinal = fechafinal.date()
    uno = dt.timedelta(days=1)
    cant_dias_totales = fechafinal - fechainicial + uno
    total = cant_dias_totales / dt.timedelta(days=1)
    
    #* Agrego los valores a Contadores
    Contadores["Cantidad de dias con lluvia"][0] = cont_lluvias
    Contadores["Cantidad de dias sin lluvia"][0] = total - cont_no_dato - cont_lluvias
    Contadores["Cantidad de dias sin datos"][0] = cont_no_dato

    #* Busco datos anomalos, > a 25mm en 5 min
    anomalo = pd.DataFrame({"Posicion del anomalo": []})
    for i in range(CantFilas):
        if (arinst["Dato instantaneo"][i] != "Na"):
            if  (arinst["Dato instantaneo"][i] != "Outliers"):
                if arinst["Dato instantaneo"][i] > 25:
                    nuevo_anomalo = pd.DataFrame({"Posicion del anomalo": [i]})
                    anomalo = pd.concat([anomalo, nuevo_anomalo], sort=False, ignore_index=True)
        
    #* Agrego las columnas nuevas a arinst
    arinst = pd.concat([arinst, Contadores], axis=1, ignore_index=False, sort=False)
    arinst = pd.concat([arinst, fechas_sin_dato], axis=1, ignore_index=False, sort=False)
    arinst = pd.concat([arinst, outliers], axis=1, ignore_index=False, sort=False)
    arinst = pd.concat([arinst, anomalo], axis=1, ignore_index=False, sort=False)
    #endregion
    
    # SECTION Exporto a un archivo
    arinst.to_csv(Nombre_fin, encoding="utf-8")     

def Procesamiento_datos_crudos(mes_num):
    
    #region AbroArchivos
    #TODO: Abro los archivos donde se encuentran las tablas con datos de grafana de pluviometros y estaciones
    #      Tambien nombro las columnas con sus nombres de identificacion
    contenido = os.listdir("Dato meses/" + mes_num)

    for archivo in contenido:
        if  archivo.endswith('.csv') and archivo.startswith("Pluviómetros"):
            with open("Dato meses/" + mes_num + "/" + archivo, encoding="utf-8") as archivoplu:
                archivopluv =  pd.read_csv(archivoplu, encoding="utf-8")
                #* Cambio el nombre de las columnas
                nombresCol = ["Fecha", "Lucas_Piriz","Museo_Blanes","PAGRO","CCZ7","Casavalle","Áreas_Verdes","Giraldez","La_Paloma","Jardín_348","Lixiviados","Evaristo_Ciganda"]  
                archivopluv.columns = nombresCol

    for archivoe in contenido:
        if  archivoe.endswith('.csv') and archivoe.startswith("Estaciones"):
            with open("Dato meses/" + mes_num + "/" + archivoe, encoding="utf-8") as archivoes:
                archivoest =  pd.read_csv(archivoes, encoding="utf-8")
                #* Cambio el nombre de las columnas
                nombresCol = ["Fecha", "Anexo","Punta_Carretas","CCZ9","Colón","CCZ18","Caif","Miguelete"]  
                archivoest.columns = nombresCol 

    #endregion
        
    #TODO: Creo directorios para los resultados en crudo
    if not(os.path.exists('Resultados')):
        os.mkdir("Resultados")
    if not(os.path.exists('Resultados/mes ' + mes_num)):
        os.mkdir('Resultados/mes ' + mes_num)
    if not(os.path.exists('Resultados/mes ' + mes_num + "/Resultado_Pluviometro")):
        os.mkdir("Resultados/mes " + mes_num + "/Resultado_Pluviometro")
    if not(os.path.exists("Resultados/mes " + mes_num + "/Resultado_Estaciones")):
        os.mkdir("Resultados/mes " + mes_num + "/Resultado_Estaciones")

    #TODO: Funcion que llama para cada pluviometro o estacion a la funcion procedimiento
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Lucas_Piriz.csv", "Lucas_Piriz")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Museo_Blanes.csv", "Museo_Blanes")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/PAGRO.csv", "PAGRO")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Casavalle.csv", "Casavalle")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Áreas_Verdes.csv", "Áreas_Verdes")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Giraldez.csv", "Giraldez")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/CCZ7.csv", "CCZ7")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/La_Paloma.csv", "La_Paloma")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Jardín_348.csv", "Jardín_348")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Lixiviados.csv", "Lixiviados")
    Procesamiento(archivopluv, "Resultados/mes " + mes_num + "/Resultado_Pluviometro/Evaristo_Ciganda.csv", "Evaristo_Ciganda")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/Anexo.csv", "Anexo")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/Punta_Carretas.csv", "Punta_Carretas")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/CCZ9.csv", "CCZ9")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/Colón.csv", "Colón")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/CCZ18.csv", "CCZ18")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/Caif.csv", "Caif")
    Procesamiento(archivoest, "Resultados/mes " + mes_num + "/Resultado_Estaciones/Miguelete.csv", "Miguelete")
                

   

