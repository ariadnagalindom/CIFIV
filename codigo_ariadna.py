# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:19:29 2019

@author: Ariadna
"""
#importamos librerias 
import pandas as pd
from mylib import mylib
import seaborn as sns
import matplotlib.pyplot as plt
#%% importamos la base de datos 
data= pd.read_excel('file:///C:/Users/Ariadna/Desktop/CIFIV/Copia de M9 M2 AIW segmentation September WD4 - Oscar(2091).xlsx', 
                    sheet_name= 'Raw data 8XX')
#removemos las columnas vacias 
data.drop(data.iloc[:, 30:57], inplace = True, axis = 1)
sns.heatmap(data.isnull(),yticklabels=False, cbar=False,cmap='Blues_r')#vemos los datos faltantes 
#%% columnas con los parámetros 
drop_columns= ['Year', 'Imt_Name', 'Iot_Name', 'SRC', 'Segment', 'Quarter', 
               'FAMILY', 'Month','OCC','Major_Minor', 'Maj', 'Minor','Ctrynum','Cost']
datan=data.drop(drop_columns,axis=1)
#limpiamos
#datan=datan.replace(['M90','M20','M23','M22','M24','M95','M91'], 
#                    ['000M90','000M20','000M23','000M22','000M24','000M95','000M91'])
datan.Leru=datan.Leru.fillna('000')
#creamos un reporte de los datos que vamos a analizar
reporte=mylib.dqr(data)
#Dashboard
sns.heatmap(datan.isnull(),yticklabels=False, cbar=False,cmap='copper')
#%% DataFrame con las columnas relacionadas con dinero
finance= pd.DataFrame(data={'LC':data.LC,
                            'Maj':data.Maj,
                            'Minor':data.Minor,
                            'Cost':data.Cost})
sns.heatmap(finance.notnull(),yticklabels=False, cbar=False,cmap='autumn_r' )
#%% Analizamos maj-min
#dependiente=LC
#independiente=maj, min, cost
#gráfica para ver 
sns.set(style='whitegrid')
sns.pairplot(finance, hue= 'LC', palette='Accent',kind='scatter', diag_kind='auto', dropna=True)
#%% comparamos las columnas Pillar vs. Family
pf= pd.DataFrame()
pf['pillar']=data.Pillar
pf['family']= data.FAMILY#TRUVENM8 

#sns.heatmap(pf.notnull().loc[0:300] )
reporte_pf= mylib.dqr(pf)
#%%
#sns.set(style='whitegrid')
sns.relplot(x='pillar', y='family',hue='pillar',data=pf,legend='brief',height=15, aspect=1)
#demostramos gráficamente que son iguales 
#%% Vemos la desigualdad entre las columnas Pillar y Family
pf = pf.fillna(0)
pf['Desigualdad']= 0
for k in range(len(pf)):
    if pf.iloc[k,0] == pf.iloc[k,1]:
        pass
    else:
        pf.iloc[k,2]='WARNING'
    
#%% comparamos OCC OCC_Desc 
occ= pd.DataFrame()
occ['OCC']=data.OCC
occ['OCC_D']= data.OCC_Desc
occ=occ.replace('UN', 'UNASSIGNED')
sns.relplot(x='OCC', y='OCC_D', hue='OCC', data=occ, legend='full',height=15, aspect=1)
#%% Desigualdad entre OCC y OCC_Desc
occ['Desigualdad']= 0
for k in range(len(occ)):
    if occ.iloc[k,0] == occ.iloc[k,1]:
        pass
    else:
        occ.iloc[k,2]='WARNING'
        
#%encontramos que estas columnas son iguales, por lo tanto una de estas viene sobrando en cada uno de los casos
#en pillar= PATIENTSAFTY, mientras en family= WPS-EXP en OCC hay claves, por lo tanto nos vamos a quedar con los nombres (OCC_Desc) 

#%% comparamos county vs. Ctrynum y similares 
countries= pd.DataFrame()
countries['Country']= data.Country
countries['Num']= data.Ctrynum
countries['lot']= data.Iot_Name
countries['lmt']= data.Imt_Name

#%% money
money= pd.DataFrame()
money['cost']=data.Cost
#money['maxmin']=data.Major_Minor #la eliminamos para que no sea repetitivo
money['max']=data.Maj
money['min']=data.Minor
money['LC']= data.LC
money=money.fillna('00')
#Sabemos que estas columnas tienen cierta relación y por esto las agrupamos
#cluster?

#LC = pd.DataFrame()

#%% Limpiar colu
#rellenar Leru con 000
 #%% Comenzamos con el analisis 
 # Creamos DataFrame para colocar el resultado de la segmentación 
segmentation= pd.DataFrame()

# Leru 
