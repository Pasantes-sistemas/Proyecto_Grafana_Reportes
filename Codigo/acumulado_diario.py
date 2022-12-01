import pandas as pd
import numpy as np

def diario_acumulado(ar_acumulado, archivo, nombre):
    #* Mientras este en el mismo dia, me quedo con el maximo acumulado de ese dia
    #* Luego agrego los dias sin datos y asi con cada columna
    #* Al final tambien agrego los contadores
    cantfilas = archivo["Fecha"].count() 
    ar = pd.DataFrame({nombre : []})
    dato_max = 0

    for i in range(cantfilas):
        if i != 0:
            fecha_actual = pd.to_datetime(archivo["Fecha"][i])
            fecha_anterior = pd.to_datetime(archivo["Fecha"][i - 1])
        else:
            fecha_actual = pd.to_datetime(archivo["Fecha"][i])
            fecha_anterior = fecha_actual
        fecha_anterior = fecha_anterior.date()
        fecha_actual = fecha_actual.date()
        
        if (fecha_actual == fecha_anterior):
            if archivo["Dato acumulado"][i] != "Na":
                if archivo["Dato acumulado"][i] != "Outliers":
                    dato_actual = pd.to_numeric(archivo["Dato acumulado"][i])
                    if (dato_max < dato_actual):
                        dato_max = dato_actual
        else:
            nuevafila = pd.DataFrame({nombre: [dato_max]})
            ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
            dato_max = 0
            if archivo["Dato acumulado"][i] != "Na":
                if archivo["Dato acumulado"][i] != "Outliers":
                    dato_actual = pd.to_numeric(archivo["Dato acumulado"][i])
                    dato_max = dato_actual
                
    nuevafila = pd.DataFrame({nombre: [dato_max]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)

    #* Agrego dias sin datos
    if pd.to_numeric(archivo["Cantidad de dias sin datos"][0]) != 0:
        cantfilas = ar[nombre].count()
        cont = archivo["Fecha sin dato"].count() 
        for i in range(cont):
            no_encontre = True
            j = 0
            while (j != cantfilas) and (no_encontre):
                fecha_actual = pd.to_datetime(ar_acumulado["Fecha"][j])
                fecha_actual = fecha_actual.date()
                fecha_sin_dato = pd.to_datetime(archivo["Fecha sin dato"][i])
                fecha_sin_dato = fecha_sin_dato.date()
                if fecha_sin_dato == fecha_actual:
                    ar[nombre][j] = np.nan
                    no_encontre = False
                j = j + 1
    
    nuevafila = pd.DataFrame({nombre: [""]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
    nuevafila = pd.DataFrame({nombre: [nombre]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
    
    nuevafila = pd.DataFrame({nombre: [archivo["Cantidad de dias con lluvia" ][0]]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
    nuevafila = pd.DataFrame({nombre: [archivo["Cantidad de dias sin lluvia" ][0]]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
    nuevafila = pd.DataFrame({nombre: [archivo["Cantidad de dias sin datos"][0]]})
    ar = pd.concat([ar, nuevafila], sort=False, ignore_index=True)
    
    ar_acumulado = pd.concat([ar_acumulado, ar], axis=1, ignore_index=False, sort=False)
    return ar_acumulado

def acumulado_diario(mes_num):
    #region AbroArchivos
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Áreas_Verdes.csv", encoding="utf-8") as Áreas_Verdes:
        Areas_Verdes =  pd.read_csv(Áreas_Verdes, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Lucas_Piriz.csv", encoding="utf-8") as Lucas_Piriz:
        Lucas_Piriz =  pd.read_csv(Lucas_Piriz, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Museo_Blanes.csv", encoding="utf-8") as Museo_Blanes:
        Museo_Blanes =  pd.read_csv(Museo_Blanes, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/PAGRO.csv", encoding="utf-8") as PAGRO:
        PAGRO =  pd.read_csv(PAGRO, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/CCZ7.csv", encoding="utf-8") as CCZ7:
        CCZ7 =  pd.read_csv(CCZ7, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Casavalle.csv", encoding="utf-8") as Casavalle:
        Casavalle =  pd.read_csv(Casavalle, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Giraldez.csv", encoding="utf-8") as Giraldez:
        Giraldez =  pd.read_csv(Giraldez, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/La_Paloma.csv", encoding="utf-8") as La_Paloma:
        La_Paloma =  pd.read_csv(La_Paloma, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Jardín_348.csv", encoding="utf-8") as Jardín_348:
        Jardín_348 =  pd.read_csv(Jardín_348, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Lixiviados.csv", encoding="utf-8") as Lixiviados:
        Lixiviados =  pd.read_csv(Lixiviados, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Pluviometro/Evaristo_Ciganda.csv", encoding="utf-8") as Evaristo_Ciganda:
        Evaristo_Ciganda =  pd.read_csv(Evaristo_Ciganda, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/Anexo.csv", encoding="utf-8") as Anexo:
        Anexo =  pd.read_csv(Anexo, encoding="utf-8")
        
    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/Punta_Carretas.csv", encoding="utf-8") as Punta_Carretas:
        Punta_Carretas =  pd.read_csv(Punta_Carretas, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/CCZ9.csv", encoding="utf-8") as CCZ9:
        CCZ9 =  pd.read_csv(CCZ9, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/Colón.csv", encoding="utf-8") as Colón:
        Colon =  pd.read_csv(Colón, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/CCZ18.csv", encoding="utf-8") as CCZ18:
        CCZ18 =  pd.read_csv(CCZ18, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/Caif.csv", encoding="utf-8") as Caif:
        Caif =  pd.read_csv(Caif, encoding="utf-8")

    with open("Resultados/mes " + mes_num + "/Resultado_Estaciones/Miguelete.csv", encoding="utf-8") as Miguelete:
        Miguelete =  pd.read_csv(Miguelete, encoding="utf-8")

    #endregion


    cantfilas = Areas_Verdes["Fecha"].count() - 1
    fecha_ini = pd.to_datetime(Areas_Verdes["Fecha"][0])
    fecha_fin = pd.to_datetime(Areas_Verdes["Fecha"][cantfilas])
    fecha_ini = fecha_ini.date()
    fecha_fin = fecha_fin.date()

    rangofechas = pd.date_range(fecha_ini, fecha_fin)
    i = 0
    ar_acumulado = pd.DataFrame({"Fecha" : []})
    #* Agrego la columna de fecha
    while (rangofechas[i] != fecha_fin):
        nuevafila = pd.DataFrame({"Fecha": [rangofechas[i]]})
        ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)
        i = i + 1
    nuevafila = pd.DataFrame({"Fecha": [rangofechas[i]]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)

    nuevafila = pd.DataFrame({"Fecha": [""]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)

    nuevafila = pd.DataFrame({"Fecha": [""]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)

    nuevafila = pd.DataFrame({"Fecha": ["Cantidad de dias con lluvia"]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)
    nuevafila = pd.DataFrame({"Fecha": ["Cantidad de dias sin lluvia"]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)
    nuevafila = pd.DataFrame({"Fecha": ["Cantidad de dias sin datos"]})
    ar_acumulado = pd.concat([ar_acumulado, nuevafila], sort=False, ignore_index=True)



    #region ejecuto funciones
    ar_acumulado = diario_acumulado(ar_acumulado, Areas_Verdes, "Areas_Verdes")
    ar_acumulado = diario_acumulado(ar_acumulado, Lucas_Piriz, "Lucas_Piriz")
    ar_acumulado = diario_acumulado(ar_acumulado, Museo_Blanes, "Museo_Blanes")
    ar_acumulado = diario_acumulado(ar_acumulado, PAGRO, "PAGRO")
    ar_acumulado = diario_acumulado(ar_acumulado, CCZ7, "CCZ7")
    ar_acumulado = diario_acumulado(ar_acumulado, Casavalle, "Casavalle")
    ar_acumulado = diario_acumulado(ar_acumulado, Giraldez, "Giraldez")
    ar_acumulado = diario_acumulado(ar_acumulado, La_Paloma, "La_Paloma")
    ar_acumulado = diario_acumulado(ar_acumulado, Evaristo_Ciganda, "Evaristo_Ciganda")
    ar_acumulado = diario_acumulado(ar_acumulado, Jardín_348, "Jardín_348")
    ar_acumulado = diario_acumulado(ar_acumulado, Lixiviados, "Lixiviados")
    ar_acumulado = diario_acumulado(ar_acumulado, Anexo, "Anexo")
    ar_acumulado = diario_acumulado(ar_acumulado, Punta_Carretas, "Punta_Carretas")
    ar_acumulado = diario_acumulado(ar_acumulado, CCZ9, "CCZ9")
    ar_acumulado = diario_acumulado(ar_acumulado, Colon, "Colón")
    ar_acumulado = diario_acumulado(ar_acumulado, CCZ18, "CCZ18")
    ar_acumulado = diario_acumulado(ar_acumulado, Caif, "Caif")
    ar_acumulado = diario_acumulado(ar_acumulado, Miguelete, "Miguelete")
    #endregion

    i = 0
    while (ar_acumulado["Fecha"][i] != fecha_fin):
        fecha = pd.to_datetime(ar_acumulado["Fecha"][i])
        fecha = fecha.date()
        ar_acumulado["Fecha"][i] = fecha
        i = i + 1
    fecha = pd.to_datetime(ar_acumulado["Fecha"][i])
    fecha = fecha.date()
    ar_acumulado["Fecha"][i] = fecha

    #Exporto archivo
    ar_acumulado.to_csv("Resultados/mes " + mes_num + "/Acumulado diario.csv", encoding="utf-8")     

