# coding: utf-8
import pandas as pd
#import seaborn as sns
#from sklearn.preprocessing import StandardScaler
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.metrics import mean_squared_error, r2_score
#from sklearn.model_selection import cross_val_score

import numpy as np

df = pd.read_csv("CSV/SantaMaria/SantaMariaPOWER.csv", delimiter=',')
df_sojaSM = pd.read_csv("CSV/SantaMaria/soja_Santa_Maria_1974_2018.txt", sep="\t")

print("Prépartion du dataset... ")

Mai15OY = int(365/2 - 30)
if df.LAT[0]<0 :
    Mai15OY = 365-31-30-31
Mai15OY

def get_AnneeCouvree(dataframe):
    return (dataframe.YEAR[len(dataframe)-1] - dataframe.YEAR[0]) 

def definir_periode_dataset(date_deb, dataframe, temp_point, incidence = 0):
    date_deb = date_deb - incidence                                         
	#Déterminer l'incidence à quelques jours
    
    ind = 0                                                                 #Indice TAB
    AnneeCouvree = get_AnneeCouvree(dataframe)                              #Nombre d'année couvrée 2021 - 1984?
    temp_sol = [0] * AnneeCouvree                                           #Initialisation Tableau
    
    i = 0
    while i < len(dataframe)-1:                                            #Parcours du data frame
        if(dataframe.DOY[i]>date_deb):                                     
			#Si le jour couvrant l'année en cours correspond à la première quinzaine de Mai
            temp_sol[ind] = temp_sol[ind] + dataframe.TS[i]                #On additionne la température

        if(temp_sol[ind]>=temp_point):                                     #Si la température arrive à un total de 1400 degrée 
            temp_sol[ind] = i+7 + incidence                                
			#On récupère l'indice de fin afin de préparer la découpe du df + une semaine
            while(dataframe.DOY[i]>date_deb):                             
				#On s'arrête ici, nous devons alors nous déplacer vers la nouvelle année
                i = i+1 
            if (ind+1) < AnneeCouvree:                                     
				#La dernière année sera bien traité, mais nous devons bloquer l'accès afin d'éviter quelconque débordement d'indice 
                ind = ind + 1  

        i = i+1
    return temp_sol


periode = definir_periode_dataset(Mai15OY, df, 1400)

def decoupe_dataset(dataframe, periode):
    begin = dataframe.DOY==Mai15OY
    first_index = dataframe[begin].index

    i = 0
    df_ = pd.DataFrame(index=dataframe.index, columns=dataframe.columns)
    df_ = df_.fillna(0)

    for end_index in periode:
        df_[first_index[i]:end_index]=dataframe[first_index[i]:end_index]
        i = i+1
    
    df_ = df_[(df_.T != 0).any()] #avoid 0 value on full line
    return df_

df_ = decoupe_dataset(df, periode)

def imputeColumns(dataset):
    """ Pour chacune des colonnes du dataset,
        mise à jour des valeurs < par la moyenne de ses valeurs non nulles.
    """
    # liste des colonnes qui seront traitées
    columnsToImpute=['PRECTOT', 'WS2M', 'T2MDEW','RH2M', 'T2M_MAX', 'T2M_MIN' ,'T2M', 'ALLSKY_TOA_SW_DWN', 'ALLSKY_SFC_SW_DWN', 'TS']

    for c in columnsToImpute:
        avgOfCol=dataset[dataset[c]>=0][[c]].mean()
        dataset[c]=np.where(dataset[[c]]>=0,dataset[[c]],avgOfCol)

imputeColumns(df_)

df_=df_.drop(columns=['LAT','LON', 'DOY'], axis =1 )

selection = df_sojaSM.Annee<1984
index2Remove = df_sojaSM[selection].index
df_sojaSM=df_sojaSM.drop(index2Remove)

X_VAL = df_[df_.YEAR==2019]


selection = df_.YEAR>2018
index2Remove = df_[selection].index
df_=df_.drop(index2Remove)

cmp = df_sojaSM.index[0]
for r in df_.index:
    if df_.YEAR[r] != df_sojaSM.Annee[cmp]:
        cmp = cmp+1
        
    if df_.YEAR[r] == df_sojaSM.Annee[cmp]:
        df_.at[r, 'Productivite (kg/ha)'] = df_sojaSM.at[cmp, 'Productivite (kg/ha)']
        df_.at[r, 'Production (t)'] = df_sojaSM.at[cmp, 'Production (t)']
        df_.at[r, 'surface (ha)'] = df_sojaSM.at[cmp, 'Production (t)']
		

	
cmp = df_sojaSM.index[0]
firstYear = True
for r in df_.index:
    if firstYear :
        df_.at[r, 'Coeff_prod'] = 0 ##Année ref

    if df_.YEAR[r] != df_sojaSM.Annee[cmp]:
        cmp = cmp+1
        firstYear = False
    
    if df_.YEAR[r] == df_sojaSM.Annee[cmp] and firstYear == False:
        coef_prod = (df_sojaSM.at[cmp, 'Productivite (kg/ha)']/df_sojaSM.at[cmp-1, 'Productivite (kg/ha)'])
        df_.at[r, 'Coeff_prod'] = coef_prod


moylast5Y = 0
cmp = 0
for r in df_.index:
    if df_.YEAR[r] > (df_.YEAR.max() - 10):
        cmp=cmp+1
        moylast5Y = moylast5Y + df_.Coeff_prod[r]
		
moylast5Y = moylast5Y/cmp

cmp = X_VAL.index[0]
size = len(X_VAL)
for i in range(cmp, cmp+size):
    X_VAL.at[i, "Coeff_prod"]=moylast5Y
X_VAL.to_csv("2019Soja_SM.csv", index=False)

df_.to_csv("Soja_SM_prepared.csv", index=False)

###################################################################
###################################################################



df = pd.read_csv("CSV/Campos/CamposNovosPOWER.csv", delimiter=',')
df_sojaSM = pd.read_csv("CSV/Campos/soja_Campos_Novos_1974_2018.txt", sep="\t")

print("Prépartion du dataset... ")


periode = definir_periode_dataset(Mai15OY, df, 1400)


df_ = decoupe_dataset(df, periode)


imputeColumns(df_)

df_=df_.drop(columns=['LAT','LON', 'DOY'], axis =1 )

selection = df_sojaSM.Annee<1984
index2Remove = df_sojaSM[selection].index
df_sojaSM=df_sojaSM.drop(index2Remove)

X_VAL = df_[df_.YEAR==2019]


selection = df_.YEAR>2018
index2Remove = df_[selection].index
df_=df_.drop(index2Remove)

cmp = df_sojaSM.index[0]
for r in df_.index:
    if df_.YEAR[r] != df_sojaSM.Annee[cmp]:
        cmp = cmp+1
        
    if df_.YEAR[r] == df_sojaSM.Annee[cmp]:
        df_.at[r, 'Productivite (kg/ha)'] = df_sojaSM.at[cmp, 'Productivite (kg/ha)']
        df_.at[r, 'Production (t)'] = df_sojaSM.at[cmp, 'Production (t)']
        df_.at[r, 'surface (ha)'] = df_sojaSM.at[cmp, 'Production (t)']
		

	
cmp = df_sojaSM.index[0]
firstYear = True
for r in df_.index:
    if firstYear :
        df_.at[r, 'Coeff_prod'] = 0 ##Année ref

    if df_.YEAR[r] != df_sojaSM.Annee[cmp]:
        cmp = cmp+1
        firstYear = False
    
    if df_.YEAR[r] == df_sojaSM.Annee[cmp] and firstYear == False:
        coef_prod = (df_sojaSM.at[cmp, 'Productivite (kg/ha)']/df_sojaSM.at[cmp-1, 'Productivite (kg/ha)'])
        df_.at[r, 'Coeff_prod'] = coef_prod


moylast5Y = 0
cmp = 0
for r in df_.index:
    if df_.YEAR[r] > (df_.YEAR.max() - 10): 
        cmp=cmp+1
        moylast5Y = moylast5Y + df_.Coeff_prod[r]
		
moylast5Y = moylast5Y/cmp

cmp = X_VAL.index[0]
size = len(X_VAL)
for i in range(cmp, cmp+size):
    X_VAL.at[i, "Coeff_prod"]=moylast5Y
X_VAL.to_csv("2019Soja_CN.csv", index=False)

df_.to_csv("Soja_CN_prepared.csv", index=False)


