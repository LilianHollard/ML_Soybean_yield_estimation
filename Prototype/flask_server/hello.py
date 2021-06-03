from flask import Flask, render_template, request, send_file
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import Annee_Reference as af

import io
import base64
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


app = Flask(__name__)


columnsNamesArr = ['PRECTOT', 'T2M', 'ALLSKY_SFC_SW_DWN', 'T2MDEW', 'T2M_MIN', 'RH2M', 'YEAR', 'Coeff_prod']
def train_model(df_=pd.DataFrame()):
	df_features = df_[columnsNamesArr]
	df_labels = df_[['Productivite (kg/ha)']]

	X_train, X_test, y_train, y_test = train_test_split(df_features, df_labels, test_size=0.1, random_state=1)
	rf = RandomForestRegressor(max_depth=8, n_estimators=400, random_state=1)
	rf.fit(X_train, y_train.values.ravel())

	train_score = rf.score(X_train, y_train)
	print('train score = ',train_score )
	return rf

df_SM = pd.read_csv("CSV/prepared_csv/Soja_SM_prepared.csv", delimiter=',')
df_2019_SM = pd.read_csv("CSV/prepared_csv/2019Soja_SM.csv", delimiter=',')

df_CN = pd.read_csv("CSV/prepared_csv/Soja_CN_prepared.csv", delimiter=',')
df_2019_CN = pd.read_csv("CSV/prepared_csv/2019Soja_CN.csv", delimiter=',')

rf_SM = train_model(df_SM)
rf_CN = train_model(df_CN)

reference = af.AnneeRef(2019, df_SM)
reference.historical_average(df_SM)

referenceCN = af.AnneeRef(2019, df_CN)
referenceCN.historical_average(df_CN)

@app.route('/',methods=['POST'])
def get_form():
	var_res = pd.DataFrame(columns=columnsNamesArr)
	if request.method == 'POST':
		new_row = pd.DataFrame()
		for name in columnsNamesArr:
			if(name!="Coeff_prod"):
				if(request.form[name]!=''):
					var_res.loc[0, name] = request.form[name]

	var_res=var_res.dropna(axis="columns")

	city_ = request.form["city_"]
	if city_ == "santamaria":
		reference.addRow(var_res)
		print(reference.df_.head())
		reference.df_.to_csv("CSV/AnneeRef_csv/AF_SANTAMARIA.csv",index=False)
		value = rf_SM.predict(reference.df_[columnsNamesArr])[0]
	elif city_ == "camposnovos":
		referenceCN.addRow(var_res)
		print(referenceCN.df_.head())
		referenceCN.df_.to_csv("CSV/AnneeRef_csv/AF_CAMPOSNOVOS.csv",index=False)
		value = rf_CN.predict(referenceCN.df_[columnsNamesArr])[0]
		
	return '',200



#Bugs d'affichage
def do_plot(data):
	f, ax = plt.subplots(figsize=(3, 3))
	sns.relplot(x="YEAR", y="Productivite (kg/ha)", data=data)
	bytes_image = io.BytesIO()
	plt.savefig(bytes_image, format='png')
	bytes_image.seek(0)
	return bytes_image


@app.route('/plots/CAMPOSNOVOS/ProductionCN', methods=['GET'])
def correlation_matrix_():
    bytes_obj = do_plot(df_CN)
    
    return send_file(bytes_obj,
                     attachment_filename='plot_CN.png',
                     mimetype='image/png')

@app.route('/plots/SANTAMARIA/ProductionSM', methods=['GET'])
def correlation_matrix():
    bytes_obj = do_plot(df_SM)
    
    return send_file(bytes_obj,
                     attachment_filename='plot_SM.png',
                     mimetype='image/png')


@app.route('/')
def index():		
	X_VAL_Features = df_2019_SM[columnsNamesArr]
	value_SM = rf_SM.predict(X_VAL_Features)[0]
	cmp = df_2019_CN.index[0]
	size = len(df_2019_CN)
	for i in range(cmp, cmp+size):
		df_2019_CN.at[i, "Coeff_prod"]=4080/3300
		
	value_CN = rf_CN.predict(df_2019_CN[columnsNamesArr])[0]


	return render_template('index.html', prediction_SM=value_SM, prediction_CN=value_CN)#, tables=[last.to_html()], titles=columnsNames)

if __name__=="__main__":
	app.run(debug=True)