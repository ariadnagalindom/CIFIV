# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:19:29 2019

@author: Ariadna
"""
#importamos librerias 
import pandas as pd
from mylib import mylib
#%% importamos la base de datos 
data= pd.read_excel('file:///C:/Users/Ariadna/Desktop/CIFIV/Copia de M9 M2 AIW segmentation September WD4 - Oscar(2091).xlsx', 
                    sheet_name= 'Raw data 8XX')
#removemos las columnas vacias 
data.drop(data.iloc[:, 30:], inplace = True, axis = 1)
#%% columnas con la misma información
#data=data.drop(['Year', 'Segment', 'Quarter', 'Month', 'FAMILY','OCC', 'Major_Minor'], axis=1)
#creamos un reporte de los datos que vamos a analizar
reporte=mylib.dqr(data)

#%% comparamos las columnas Pillar vs. Family
pf= pd.DataFrame()
pf['pillar']=data.Pillar
pf['family']= data.FAMILY#TRUVENM8 

reporte_pf= mylib.dqr(pf)

for k in range(0, len(pf)):
    if k in pf['pillar']==pf['family']:
        pass
    else:
        pf['reporte']='warning'
    
#%% comparamos OCC OCC_Desc 
occ= pd.DataFrame()
occ['OCC']=data.OCC
occ['OCC_D']= data.OCC_Desc

'''
encontramos que estas columnas son iguales, por lo tanto
una de estas viene sobrando en cada uno de los casos
en pillar= PATIENTSAFTY, mientras en family= WPS-EXP 
en OCC hay claves, por lo tanto nos vamos a quedar con los nombres (OCC_Desc) 
'''
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
'''
Sabemos que estas columnas tienen cierta relación y por esto las agrupamos
'''
#cluster?
#%% Limpiar columna SegCalc
def replace_text(x, to_replace, replacement):
    try:
        x=x.replace(to_replace, replacement)
    except:
        pass
    return x

data['SegCalc']= data.SegCalc.apply(replace_text, args= ('000',''))
#rellenar Leru con 000
 #%% Comenzamos con el analisis 
 # Creamos DataFrame para colocar el resultado de la segmentación 
segmentation= pd.DataFrame()

# Leru 
