# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:28:37 2019

@author: danie
"""

import numpy as np
import pandas as pd
import scipy.spatial.distance as sc
from scipy.cluster import hierarchy
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mylib import mylib
#%% Importar los datos
data = pd.read_excel("file:///C:/Users/Ariadna/Desktop/CIFIV/Copia de M9 M2 AIW segmentation September WD4 - Oscar(2091).xlsx",sheetname="Raw data 8XX")#,index_col="Customer_number")
parametros = pd.read_excel("file:///C:/Users/Ariadna/Desktop/CIFIV/Copia de M9 M2 AIW segmentation September WD4 - Oscar(2091).xlsx",sheetname="Parametros")#,index_col="Customer_number")

#%% Quitar columnas vacías
data=data.iloc[:,:30]
parametros = parametros.iloc[2:,:3]
data=data.drop(["Year","Segment","Quarter","Month","ORDERNUM","Major_Minor","Iot_Name","Imt_Name","OCC","FAMILY","Country","Cost","SRC"],axis=1)
#Se eliminan las columnas de Year, Segment, Quarter, Month, ORDERNUM, Major_Minor, Iot_Name, Imt_Name 
#debido a que para el análisis no son necesarios.

#%% renombramos las columnas 
parametros=parametros.rename(columns={"Esta Sección se lee así… si A = B entonces C.":'A',
                                      "Unnamed: 1":'B',
                                      "Unnamed: 2":'C'})
#%% REPORTE DE CALIDAD DE LOS DATOS
def DQR(data):
    
    #%% Lista de variables que se encuentran en la base de datos
    columns = pd.DataFrame(list(data.columns.values) , columns = ["nombres"], index = list(data.columns.values))
    
    #%% Lista de tipos de variables
    data_types = pd.DataFrame(data.dtypes, columns = ["tipo"])
    
    #%% Lista de datos presentes
    present_values = pd.DataFrame(data.count(), columns = ["Datos presentes"])
    
    #%% Lista de datos faltantes
    miss_values = pd.DataFrame(data.isnull().sum() , columns = ["Datos faltantes"])
    
    #%% Lista de valores Unicos
    unique_values = pd.DataFrame(columns = ["Valores Unicos"])
    for col in list(data.columns.values):
        unique_values.loc[col] = [data[col].nunique()]
        
    #%% Lista de valores minimos
    min_values = pd.DataFrame(columns = ["Valores mínimos"])
    for col in list(data.columns.values):
        try:
            min_values.loc[col] = [data[col].min()]
        except:
            pass
    
    #%% Lista de valores maximos
    max_values = pd.DataFrame(columns = ["Valores maximos"])
    for col in list(data.columns.values):
        try:
            max_values.loc[col] = [data[col].max()]
        except:
            pass
    
    #%% Reporte final
    data_quality_report = columns.join(data_types).join(present_values).join(miss_values).join(unique_values).join(min_values).join(max_values)
    return data_quality_report

#%% Usar mi funcion
data_quality_report = mylib.dqr(data)

#%% Usar Customer_number como índice
#data.index=data.Customer_number
data=data.set_index("Customer_number")
#data.rename_axis("Customer_number",axis="index", inplace=True)

#%%Separando columna de resultados
resultados = data['Segmentation Offering']
data = data.iloc[:,:-1]
#limpiamos truven simpler
def replace_text(x,obje,repla):
    try:
        x=x.replace(obje,repla)
    except:
        pass
    return x
resultados = replace_text(resultados,'Truven simpler','Truven Simpler')

#%% Analizando los resultados
num_sementation=pd.value_counts(resultados)

#%%Funcion de normalizacion
def normalizar(x):
    return (x-x.mean())/x.std()
#%%Normalizando
#data['Ctrynum']=normalizar(data['Ctrynum'])
data['Maj']=normalizar(data['Maj'])
data['Minor']=normalizar(data['Minor'])

#%%Categorizando 
def categorizar(X):
    val_unic = np.array(X.unique())
    w = np.round(np.linspace(0,1,len(X.unique())),3)
    directorio = dict(zip(val_unic,w))
    return [directorio[item] for item in X]
#%%Aplicando formula
data['Work__'] = categorizar(data['Work__'])
data["OCC_Desc"] = categorizar(data["OCC_Desc"])    
data["PRODID"] = categorizar(data["PRODID"])
data["LDIV"] = categorizar(data["LDIV"])
data["LoB"] = categorizar(data["LoB"]) 
data["Pillar"] = categorizar(data["Pillar"]) 
data["Bmdiv"] = categorizar(data["Bmdiv"]) 
data["SegCalc"] = categorizar(data["SegCalc"])
data["Cust__"] = categorizar(data["Cust__"])
data["Leru"] = categorizar(data["Leru"])

#%%
reporte = mylib.dqr(data)

#%%Leyendo hoja de datos nuevamente
data_parametros = pd.read_excel("file:///C:/Users/Ariadna/Desktop/CIFIV/Copia de M9 M2 AIW segmentation September WD4 - Oscar(2091).xlsx",sheetname="Raw data 8XX")

#%%Generando nuevo dataframe con las columnas relevantes
data_parametros=data_parametros.iloc[:,:29]
data_parametros=data_parametros.drop(["Year","Segment","Quarter","Month","ORDERNUM","Maj","Minor","Iot_Name","Imt_Name","Country","Cost","SRC","LoB","Bmdiv","Ctrynum"],axis=1)
data_parametros=data_parametros.set_index("Customer_number")
#%%
reporte_parametros=mylib.dqr(data_parametros)

#%%Separando parametros repetidos de los parametros sin repetir
parametros_cuenta = pd.DataFrame(parametros['B'].value_counts())
parametros_r = parametros_cuenta[parametros_cuenta>=2].dropna()
parametros_r['B'] = parametros_r.index #repetidos
parametros_u = parametros_cuenta[parametros_cuenta==1].dropna() #unicos
parametros_u['B'] = parametros_u.index
#%%Creando el DataFrame de categorias y parametros
nombres_categorias = pd.DataFrame(resultados.unique())
nombres_columnas = pd.DataFrame(parametros.A.unique())
parametros_u['A'] = parametros_u['B']
parametros_u['C'] = parametros_u['B']
data_parametros['Offering'] = data_parametros['Work__']
#%%Generando parametros unics
for val in parametros_u['B']:
    parametros_u['A'][val]=parametros['A'][parametros['B']==val].item()
    parametros_u['C'][val]=parametros['C'][parametros['B']==val].item()
    
#%%Creando Diccionario
dic ={}
parametros = parametros.sort_values(by=['A'])
for i in parametros['A']:
    if i in dic:
        dic[i]=dict(zip(parametros['B'][parametros['A']==i],parametros['C'][parametros['A']==i]))
    else:
        dic[i]=dict(zip(parametros['B'][parametros['A']==i],parametros['C'][parametros['A']==i]))
        
#%%Iterando en el dataframe
for i in data_parametros.columns:
    if i in dic:
        data_parametros['Offering'] = data_parametros[i].map(dic[i])
    else:
        pass
#%%Evaluando resultados
w=np.linspace(0,len(data),len(data),dtype=int)
w = np.round(w,0)
resultados_prueba = pd.DataFrame(data_parametros['Offering'])
resultados = pd.DataFrame(resultados)
resultados_prueba = resultados_prueba.set_index(w)
resultados = resultados.set_index(w)
checks = 0
resultados_p=resultados_prueba.dropna()
ar1=np.array(resultados_p.index)
#%%Checando predicciones correctas, nans e incorrectas
for i in range(len(data)):
    if resultados_prueba.iloc[i,0] == resultados.iloc[i,0]:
            checks +=1
nans = resultados_prueba.isnull().sum().item()
wrongs = len(resultados_prueba)-nans-checks 
#%%lista con los indices de los parametros erroneos
eval1 = resultados_prueba['Offering'][resultados_prueba['Offering']!=resultados['Segmentation Offering']]
            







