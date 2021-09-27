# -*- coding: utf-8 -*-
"""Covid 19 data analysis using EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12_PDFVXi9zjrg0kkkK4EgbSYLGfBZ-CU

#Manipulating the data
"""

import pandas as pd
import numpy as np
import seaborn as sns

"""#Visualizing the data"""

import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot

"""#Dataprep library"""

from dataprep.eda import *
from dataprep.datasets import load_dataset
from dataprep.eda import create_report

"""#For Machine Learning Algorithms"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn import ensemble
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import metrics

"""#https://www.kaggle.com/c/covid19-global-forecasting-week-5/data

For downloading the datasets

#Loading the data
"""

df=pd.read_csv('train.csv')

test=pd.read_csv('test.csv')

sub=pd.read_csv('submission.csv')

"""#Data analysis"""

df

df.shape

df.isnull().sum()

df.info()

df.head()

fig = plt.figure(figsize = (45,30))
fig = px.pie(df, names = 'Country_Region', values = 'TargetValue', color_discrete_sequence = px.colors.sequential.RdBu, hole = 0.4)
fig.update_traces(textposition = 'inside')
fig.show()

"""#Checking the data types in datasets"""

df.dtypes.value_counts().plot.pie(explode=[0.1,0.1,0.1],autopct='%1.1f%%',shadow=True)
plt.title('Data type');

df.describe(include='all')

"""#Finding the missing values

**In train data**
"""

missing = df.isnull().sum()
missing_percentage = df.isnull().sum()/df.shape[0]*100

dic = {
    'mising':missing,
    'missing_percentage %':missing_percentage
    }
frame=pd.DataFrame(dic)
frame

"""**In test data**"""

missing = test.isnull().sum()
missing_percentage = test.isnull().sum()/df.shape[0]*100

dic = {
    'mising':missing,
    'missing_percentage %':missing_percentage
    }
frame=pd.DataFrame(dic)
frame

"""**In submission data**"""

sub

"""#Data Visualization"""

sns.barplot(y = 'TargetValue', x='Target', data = df)
plt.show()

sns.barplot(x = 'Target', y= 'Population', data = df)
plt.show()

df.hist(figsize=(15,15),edgecolor='black')

grouped_data = df.groupby('Country_Region').sum()
top_10_pop_countries=grouped_data.nlargest(10, 'Population')['TargetValue']

top_10_pop_countries

fig = px.bar(x = top_10_pop_countries.index, y = top_10_pop_countries.values, title='Top 10 most populous countries versus number of covid cases', labels = dict(x='Countries', y='Number of Covid-19 Cases'))
fig.show()

df.info()

"""**County data**"""

plot(df.County)

plt.figure(figsize=(30,9))
county_plot=df.County.value_counts().head(100)
sns.barplot(county_plot.index,county_plot)
plt.xticks(rotation=90)
plt.title('County count');

"""**Province State**"""

plot(df.Province_State)

plt.figure(figsize=(30,9))
Province_State_plot=df.Province_State.value_counts().head(100)
sns.barplot(Province_State_plot.index,Province_State_plot)
plt.xticks(rotation=90)
plt.title('Province State count');

"""**Country Region**"""

plot(df.Country_Region)

plt.figure(figsize=(30,9))
Country_Region_plot=df.Country_Region.value_counts().head(30)
sns.barplot(Country_Region_plot.index,Country_Region_plot)
plt.xticks(rotation=90)
plt.title('Country Region count');

"""#Using Date for cases"""

df['Date'] = pd.to_datetime(df['Date'])
test['Date'] = pd.to_datetime(test['Date'])

date_grouped_data = df.groupby('Date').sum()
fig = px.line(x=date_grouped_data.index, y = date_grouped_data['TargetValue'], title = 'Growth of number of COVID-19 cases over time', labels = dict(x='Date', y = 'Number of Coivd-19 Cases'))
fig.show()

last_date = df.Date.max()
df_countries = df[df['Date']==last_date]
df_countries = df_countries.groupby('Country_Region', as_index=False)['TargetValue'].sum()
df_countries = df_countries.nlargest(10,'TargetValue')
df_trend = df.groupby(['Date','Country_Region'], as_index=False)['TargetValue'].sum()
df_trend = df_trend.merge(df_countries, on='Country_Region')
df_trend.rename(columns={'Country_Region':'Country', 'TargetValue_x':'Cases'}, inplace=True)

px.line(df_trend, x='Date', y='Cases', color='Country', title='COVID19 Total Cases growth for top 10 worst affected countries')

"""#Data preprocessing"""

df.info()

df = df.drop(['County','Province_State','Country_Region','Target'],axis=1)
test = test.drop(['County','Province_State','Country_Region','Target'],axis=1)
df

df.isnull().sum()

def create_features(df):
    df['day'] = df['Date'].dt.day
    df['month'] = df['Date'].dt.month
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['dayofyear'] = df['Date'].dt.dayofyear
    df['quarter'] = df['Date'].dt.quarter
    df['weekofyear'] = df['Date'].dt.weekofyear
    return df

def train_dev_split(df, days):
    date = df['Date'].max() - dt.timedelta(days=days)
    return df[df['Date'] <= date], df[df['Date'] > date]

test_date_min = test['Date'].min()
test_date_max = test['Date'].max()

def avoid_data_leakage(df, date=test_date_min):
    return df[df['Date']<date]

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day
df['Date']=pd.to_datetime(df['Date'])
test['Date']=pd.to_datetime(test['Date'])

test['Date']=test['Date'].dt.strftime("%Y%m%d")
df['Date']=df['Date'].dt.strftime("%Y%m%d").astype(int)

"""**split data**"""

predictors = df.drop(['TargetValue', 'Id'], axis=1)
target = df["TargetValue"]
X_train, X_test, y_train, y_test = train_test_split(predictors, target, test_size = 0.22, random_state = 0)

"""#RandomForestRegression"""

model = RandomForestRegressor(n_jobs=-1)
estimators = 100
model.set_params(n_estimators=estimators)

scores = []

pipeline = Pipeline([('scaler2' , StandardScaler()),('RandomForestRegressor: ', model)])
pipeline.fit(X_train , y_train)
prediction = pipeline.predict(X_test)

pipeline.fit(X_train, y_train)
scores.append(pipeline.score(X_test, y_test))

plt.figure(figsize=(8,6))
plt.plot(y_test,y_test,color='red')
plt.scatter(y_test,prediction,color='blue')
plt.xlabel('Actual Target Value',fontsize=15)
plt.ylabel('Predicted Target Value',fontsize=15)
plt.title('Random Forest Regressor (R2 Score= 0.95)',fontsize=14)
plt.show()

X_test

test.drop(['ForecastId'],axis=1,inplace=True)
test.index.name = 'Id'
test

y_pred2 = pipeline.predict(X_test)
y_pred2

predictions = pipeline.predict(test)
pred_list = [int(x) for x in predictions]
output = pd.DataFrame({'Id': test.index, 'TargetValue': pred_list})
print(output)

"""#XG booster regression

> Indented block


"""

import xgboost as xgb

xgbr= xgb.XGBRegressor(n_estimators=800, learning_rate=0.01, gamma=0, subsample=.7,
                       colsample_bytree=.7, max_depth=10,
                       min_child_weight=0, 
                       objective='reg:squarederror', nthread=-1, scale_pos_weight=1,
                       seed=27, reg_alpha=0.00006, n_jobs=-1)

xgbr.fit(X_train,y_train)

prediction_xgbr=xgbr.predict(X_test)

print('RMSE_XGBoost Regression=', np.sqrt(metrics.mean_squared_error(y_test,prediction_xgbr)))
print('R2 Score_XGBoost Regression=',metrics.r2_score(y_test,prediction_xgbr))

plt.figure(figsize=(8,6))
plt.scatter(x=y_test, y=prediction_xgbr, color='dodgerblue')
plt.plot(y_test,y_test, color='deeppink')
plt.xlabel('Actual Target Value',fontsize=15)
plt.ylabel('Predicted Target Value',fontsize=15)
plt.title('XGBoost Regressor (R2 Score= 0.89)',fontsize=14)
plt.show()

a=output.groupby(['Id'])['TargetValue'].quantile(q=0.05).reset_index()
b=output.groupby(['Id'])['TargetValue'].quantile(q=0.5).reset_index()
c=output.groupby(['Id'])['TargetValue'].quantile(q=0.95).reset_index()
a.columns=['Id','q0.05']
b.columns=['Id','q0.5']
c.columns=['Id','q0.95']
a=pd.concat([a,b['q0.5'],c['q0.95']],1)
a['q0.05']=a['q0.05'].clip(0,10000)
a['q0.5']=a['q0.5'].clip(0,10000)
a['q0.95']=a['q0.95'].clip(0,10000)
a['Id'] =a['Id']+ 1
a

sub=pd.melt(a, id_vars=['Id'], value_vars=['q0.05','q0.5','q0.95'])
sub['variable']=sub['variable'].str.replace("q","", regex=False)
sub['ForecastId_Quantile']=sub['Id'].astype(str)+'_'+sub['variable']
sub['TargetValue']=sub['value']
sub=sub[['ForecastId_Quantile','TargetValue']]
sub.reset_index(drop=True,inplace=True)
sub.head()

sub.to_csv("submission.csv",index=False)

