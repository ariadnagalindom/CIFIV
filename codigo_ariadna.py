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

sns.heatmap(data.isnull(),yticklabels=False, cbar=False,cmap='copper').get_figure().savefig('hm_data.jpg',dpi=1000)#vemos los datos faltantes 
#%% columnas con los parámetros 
drop_columns= ['Year', 'Imt_Name', 'Iot_Name', 'SRC', 'Segment', 'Quarter', 
               'FAMILY', 'Month','Major_Minor', 'Maj', 'Minor','Ctrynum','Cost']
datan=data.drop(drop_columns,axis=1)
#limpiamos
#datan=datan.replace(['M90','M20','M23','M22','M24','M95','M91'], 
#                    ['000M90','000M20','000M23','000M22','000M24','000M95','000M91'])
datan.Leru=datan.Leru.fillna('000')
#creamos un reporte de los datos que vamos a analizar
reporte=mylib.dqr(data)

sns.heatmap(datan.isnull(),yticklabels=False, cbar=False,cmap='copper').get_figure().savefig('hm_datan.jpg',dpi=300)
#%% DataFrame con las columnas relacionadas con dinero
finance= pd.DataFrame(data={'LC':data.LC,
                            'Maj':data.Maj,
                            'Minor':data.Minor,
                            'Cost':data.Cost})

sns.heatmap(finance.isnull(),yticklabels=False, cbar=False,cmap='copper' ).get_figure()#.savefig('hm_finance.jpg',dpi=300)
#%% Analizamos maj-min
#dependiente=LC
#independiente=maj, min, cost
#gráfica para ver 
#sns.color_palette("tab20c", n_colors=20)
sns.set(style='whitegrid', font_scale=1.5, color_codes=True)#agregamos cuadricula a TODO en seaborn
sns.pairplot(finance, hue= 'LC',palette="tab20c",
             kind='scatter', dropna=True).savefig('finance_corr.jpg',dpi=300)
# la diágonal 
reporte_finance= mylib.dqr(finance)
#%% comparamos las columnas Pillar vs. Family
pf= pd.DataFrame()
pf['pillar']=data.Pillar
pf['family']= data.FAMILY#TRUVENM8 

reporte_pf= mylib.dqr(pf)

sns.set(style='whitegrid', palette='deep', font_scale=1, color_codes=True)
pf_chart=sns.relplot(x='pillar', y='family',hue='pillar',data=pf,
            height=5)
plt.xticks(rotation=90)
pf_chart.savefig('pillar_vs_family.jpg',dpi=300)
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
occ_chart=sns.relplot(x='OCC', y='OCC_D', hue='OCC',
            data=occ, legend='full',height=8, aspect=1)
plt.xticks(rotation=90)
occ_chart.savefig('occ.jpg',dpi=500)

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
l=pd.DataFrame()
l['lot']= data.Iot_Name
l['lmt']= data.Imt_Name

sns.relplot(x='lot', y='lmt', hue='lmt',
            data=l, legend='full',height=8, aspect=1.5).savefig('region_countries.jpg',dpi=500)
#Con esto encontramos qué países pertenecen a cada región, hay unas que solo tienen 1 país
#%%
countries= pd.DataFrame()
countries['country']=data.Country
countries['countrynum']=data.Ctrynum

plt.plot(countries.country, countries.countrynum)
sns.relplot(x='country', y='countrynum', hue='country',data=countries)#.savefig('country.jpg')#sort????
#%%
LS = pd.DataFrame()
LS['SRC']=data.SRC
LS['LC']=data.LC

sns.relplot(x='SRC', y='LC',hue='LC', data=LS)#.savefig('LC_vs_RSC.jpg',dpi=500)#cluster? hay 4 grupos 
#nel
#%%diferencias de segmentación
segmentacion=pd.DataFrame()
segmentacion['Segmentacion Ofrecida']=datan['Segmentation Offering']
segmentacion['Segmentacion Agregada']=datan.iloc[:,-1:]

datan=datan.replace('Truven simpler','Truven Simpler')

sns.set(style="whitegrid", palette="deep", color_codes=True)
seg_cahrt=sns.relplot(x='Segmentacion Ofrecida',y='Segmentacion Agregada', data=segmentacion)
plt.xticks(rotation=90)
seg_cahrt.savefig('segmentacion.jpg',dpi=300)
#%% OCC vs SegCalc
sns.relplot(x='OCC_Desc', y='SegCalc', hue='Segmentation Offering',
            data=datan, height=12,aspect=1 )#.savefig('Segcalc_OCC.jpg')
#%% Lob vs. OCC
sns.relplot(x='LoB', y='OCC_Desc', hue='Segmentation Offering',data=datan)#.savefig('lob_occ.jpg', dpi=300)
#%% Lob vs. LC
sns.relplot(x='LoB', y='LC', hue='Segmentation Offering',data=datan)
#%% OCC vs. Segmentation Offering
sns.relplot(x='Segmentation Offering', y='OCC_Desc', hue='Segmentation Offering',
            data=datan)