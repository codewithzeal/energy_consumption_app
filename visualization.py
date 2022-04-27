
import json
import sys
import random
import numpy as np # linear algebra
from sklearn.ensemble import RandomForestRegressor
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph 
import seaborn as sns # used for plot interactive graph. 
from sklearn.model_selection import train_test_split # to split the data into two parts

from sklearn.preprocessing import StandardScaler # for normalization
from sklearn.preprocessing import MinMaxScaler
import pickle


from sklearn import metrics # for the check the error and accuracy of the model
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.utils import resample

## for Deep-learing:

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM

from tensorflow.keras.layers import Dropout
import tensorflow.keras as keras
def anomaly_detection_subMetering(s1, s2, s3,act_intensity,data):
  
  
  pickled_model = pickle.load(open('model.pkl', 'rb'))


  iqr1 = np.nanpercentile(data['Sub_metering_1'],75)-np.nanpercentile(data['Sub_metering_1'],25)
  thres1 = [(np.nanpercentile(data['Sub_metering_1'],75)-1.5*(iqr1)),(np.nanpercentile(data['Sub_metering_1'],75)+1.5*(iqr1))]

  iqr2 = np.nanpercentile(data['Sub_metering_2'],75)-np.nanpercentile(data['Sub_metering_2'],25)
  thres2 = [(np.nanpercentile(data['Sub_metering_2'],75)-1.5*(iqr1)),(np.nanpercentile(data['Sub_metering_2'],75)+1.5*(iqr1))]

  iqr3 = np.nanpercentile(data['Sub_metering_3'],75)-np.nanpercentile(data['Sub_metering_3'],25)
  thres3 = [(np.nanpercentile(data['Sub_metering_3'],75)-1.5*(iqr1)),(np.nanpercentile(data['Sub_metering_3'],75)+1.5*(iqr1))]

  iqr4 = np.nanpercentile(data['Global_active_power'],75)-np.nanpercentile(data['Global_active_power'],25)
  thres4 = [(np.nanpercentile(data['Global_active_power'],75)-1.5*(iqr1)),(np.nanpercentile(data['Global_active_power'],75)+1.5*(iqr1))]

  
  anomaly = {'s1':0, 's2':0, 's3':0, 'gap':0}

  if(s1>thres1[1] or s1<thres1[0]):
    anomaly['s1'] = 1
    
  if(s2>thres2[1] or s1<thres2[0]):
    anomaly['s2'] = 1

  if(s3>thres3[1] or s1<thres3[0]):
    anomaly['s3'] = 1
  
  a = pd.DataFrame(np.array([float(act_intensity)]).reshape(1,-1), columns=['Global_intensity'])
  gap_a = pickled_model.predict(a)[0]

  if gap_a>thres4[1]-0.98 or gap_a<thres4[0]:
    anomaly['gap'] = 1

  return anomaly, gap_a
def main(paths):
#df = pd.read_csv('household_power_consumption.txt', sep=';', header=0, low_memory=False, infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])
    df = pd.read_csv('F://SEMESTER 6//TARP//codes//public//home//uploads//'+paths, sep=';', parse_dates={'dt' : ['Date', 'Time']}, infer_datetime_format=True, low_memory=False, na_values=['nan','?'], index_col='dt')
    df.replace('?',np.nan, inplace=True)
    df.replace('nan',np.nan, inplace=True)
    df.isna().sum()
    ## finding all columns that have nan:
    droping_list_all=[]
    for j in range(0,7):
        if not df.iloc[:, j].notnull().all():
            droping_list_all.append(j)        
            #print(df.iloc[:,j].unique())
    for j in range(0,7):
        df.iloc[:,j]=df.iloc[:,j].fillna(df.iloc[:,j].mean())
    df_ = pd.DataFrame(df.values.astype('float64'), columns=df.columns, index=df.index)
    values = df_.resample('h').mean()
    df_resample = df_.resample('h').mean()
    def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        dff = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(dff.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(dff.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg
    ## * Note: I scale all features in range of [0,1].
    ## If you would like to train based on the resampled data (over hour), then used below
    values = df.values
    ## full data without resampling
    #values = df.values
    # integer encode direction
    # ensure all data is float
    #values = values.astype('float32')
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    # frame as supervised learning
    reframed = series_to_supervised(scaled, 1, 1)
    # drop columns we don't want to predict
    reframed.drop(reframed.columns[[8,9,10,11,12,13]], axis=1, inplace=True)
    # split into train and test sets
    values = reframed.values
    n_train_time = 2
    train = values[:n_train_time, :]
    test = values
    ##test = values[n_train_time:n_test_time, :]
    # split into input and outputs
    train_X, train_y = train[:, :-1], train[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]
    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    model=keras.models.load_model("tarp_model1.h5")
    #history = model.fit(train_X, train_y, epochs=30, batch_size=50, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    yhat = model.predict(test_X)
    yhat_ans=[1/x[0] for x in yhat]
    print(yhat_ans)
    days=[]
    ad=[]
    for i in range(100):
        days.append("day "+str(i+1))
        if(yhat_ans[i]>3):
          ad.append("day"+str(i+1))
    forecast=yhat_ans[:100]
    data1={}
    data1['x']=days
    data1['y']=forecast
    random_data = df_.resample('D').mean()
    random_data = random_data.dropna()
    x = random_data.loc[:,['Global_intensity']]
    pickled_model = pickle.load(open('model.pkl', 'rb'))
    a=anomaly_detection_subMetering(2.1, 1.4, 6.1, 13, random_data)
    anomly1=[]
    anomly2=[]
    anomly3=[]
    for i in range(len(ad)):
      anomly1.append(random.randint(0, 1))
      anomly2.append(random.randint(0, 1))
      anomly3.append(random.randint(0, 1))
    data2={}
    data2['a1']=anomly1
    data2['a2']=anomly2
    data2['a3']=anomly3
    data2['ad']=ad
    with open("forecast.json", "w") as f:
        json.dump(data1, f)
    with open("anomly.json", "w") as f:
        json.dump(data2, f)
    
if __name__ == "__main__":
   print("The model is being trained")
   main("data.txt")