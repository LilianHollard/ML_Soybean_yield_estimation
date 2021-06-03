import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class AnneeRef:        
    def __init__(self, Annee, Dataframe):
        self.Annee = Annee
        self.df_ = pd.DataFrame()
        self.df_ = self.df_.append(Dataframe[Dataframe.YEAR==(Annee-1)], ignore_index=True)
        self.df_.loc[self.df_.YEAR==(Annee-1), "YEAR"]=Annee
        self.DOY = 0
    
    def put_back_year(self):
        self.df_.YEAR=self.Annee

    def change_YEAR(self, year):
        self.Annee = year
        self.put_back_year()
    
    def change_CoeffProd(self, new_coeff):
        self.df_.Coeff_prod = new_coeff
        
    def addRow(self, row):
        for columns in row:
            self.df_.loc[self.DOY, columns] = row[columns].values
        self.DOY = self.DOY + 1
        
    def addRowIncomplete(self, row):
        for columns in row:
            if(row[columns].values != NaN):
                self.df_.loc[self.DOY, columns] = row[columns].values
        self.DOY = self.DOY + 1

    def slight_mean(self, Annee, Dataframe):
        size_df = len(self.df_)
        size_param = len(Dataframe[Dataframe.YEAR==Annee])
        if(size_df<size_param):
            for i in range(0, size_df):
                df1 = pd.DataFrame()
                df1 = df1.append(Dataframe[Dataframe.YEAR==Annee], ignore_index=True)
                self.df_.loc[i]=self.df_.loc[i].add(df1.loc[i], fill_value=0)
                self.df_.loc[i] = self.df_.loc[i].div(2)
        else:
            for i in range(0, size_param):
                df1 = pd.DataFrame()
                df1 = df1.append(Dataframe[Dataframe.YEAR==Annee], ignore_index=True)
                self.df_.loc[i]=self.df_.loc[i].add(df1.loc[i], fill_value=0)
                self.df_.loc[i] = self.df_.loc[i].div(2)
    
        self.put_back_year()
            
    
    def historical_average(self, Dataframe):
        startPoint = self.df_.YEAR[self.df_.YEAR.index[0]]
        endPoint = self.df_.YEAR[self.df_.YEAR.idxmax()]
        selection = self.df_.YEAR==startPoint
        for i in range(startPoint, endPoint):
            Year = int(self.df_[selection].iloc[0].YEAR)
            self.slight_mean(Year, self.df_)