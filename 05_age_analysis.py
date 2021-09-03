import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from scipy import stats

columns = ['screen_name','dale_chall_readability_score', 'flesch_kincaid', 'automated_readability', 'flesch_reading', 'coleman_liau_index']
average = ['dale_chall_readability_score', 'flesch_kincaid', 'automated_readability', 'flesch_reading', 'coleman_liau_index']


def calculate_age(df):
	current_year = 2020.0
	df = df.sort_values('screen_name')
	df['age'] = current_year - df['birth_year']
	return df


def strip_name(text):
	name = text.split("_",1)[1]
	removecsv = name.split(".",1)[0]
	return removecsv


def machine_learning(X, y):
	#y = y.astype('str')

	X_train, X_valid, y_train, y_valid = train_test_split(X,y)

	model = make_pipeline(
		StandardScaler(),
		RandomForestRegressor(max_depth=2, random_state=0)
		#KNeighborsClassifier(n_neighbors=10,weights='uniform',algorithm='auto',leaf_size=25)
		#RandomForestClassifier(n_estimators=200, max_depth=2 0, min_samples_leaf=7)
		)

	X_train = np.array(X_train).reshape(-1, 1)
	y_train = np.array(y_train).reshape(-1, 1)
	print(X_train)
	print(y_train)
	model.fit(X_train, y_train)
	
	X_predict = np.arange(99)
	X_predict = X_predict.astype('float')
	X_predict = np.array(X_predict).reshape(1, -1)
	X_predict = X_predict.transpose()

	predicted = model.predict(X_predict)
	return predicted


def main():
	user_data = pd.read_csv("users.csv")
	data = calculate_age(user_data)
	files = [i for i in os.listdir("Cleaned_user_tweets") if i.endswith("csv")]
	arr = []

	for file in files:
		df = pd.read_csv("Cleaned_user_tweets/"+str(file))
		user_name = strip_name(file)
		dale_ave = np.float(df['dale_chall_readability_score'].median())
		kincaid_ave = np.float(df['flesch_kincaid'].median())
		amr_ave = np.float(df['automated_readability'].median())
		reading_ave = np.float(df['flesch_reading'].median())
		coleman_ave = np.float(df['coleman_liau_index'].median())
		arr.append([user_name, dale_ave, kincaid_ave, amr_ave, reading_ave, coleman_ave])
	
	averages = pd.DataFrame(data=arr, index=None, columns=columns)
	merged_df = pd.merge(data, averages, on='screen_name')

	grouped_age = merged_df.groupby('age').mean()
	grouped_age = grouped_age.reset_index()

	print(grouped_age)
	x_val = np.array(grouped_age['age'])
	y_val = np.array([grouped_age['dale_chall_readability_score'], grouped_age['flesch_kincaid'], grouped_age['automated_readability'], grouped_age['flesch_reading'], grouped_age['coleman_liau_index']])
	X_val_predict = np.arange(99)

	for test in range(len(y_val)):
		plt.plot(x_val, y_val[test], label=average[test])
		plt.legend()
		plt.title('Age Vs Reading Level')
		plt.xlabel('Age')
		plt.ylabel('Reading Level Unit')
	#	plt.savefig(average[test]) 
		plt.show()

	##Machine learning to find more data points
	
	for predictions in range(len(y_val)):
		prediction = machine_learning(x_val, y_val[predictions])
		plt.plot(X_val_predict, prediction, label=average[predictions] + " prediction")
		plt.legend()
		#plt.axis([0, 100])
		plt.xlabel('Age')
		plt.ylabel('Reading Level Unit')
	#	plt.savefig(average[predictions] + "predictions") 
		plt.show()

	#Two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero, using Wald Test with t-distribution of the test statistic.
	#so we can conclude that the slope is non zero 

	slope, intercept, r_value, p_value_0, std_err = stats.linregress(x_val, y_val[0])
	slope, intercept, r_value, p_value_1, std_err = stats.linregress(x_val, y_val[1])
	slope, intercept, r_value, p_value_2, std_err = stats.linregress(x_val, y_val[2])
	slope, intercept, r_value, p_value_3, std_err = stats.linregress(x_val, y_val[3])
	slope, intercept, r_value, p_value_4, std_err = stats.linregress(x_val, y_val[4])

	#grouped_age['anova'] = grouped_age.flesch_kincaid.shift(-1)
	print(p_value_0, p_value_1, p_value_2, p_value_3, p_value_4)
if __name__ == '__main__':
	main()

