import sys
import numpy as np # linear algebra

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph 
import seaborn as sns # used for plot interactive graph. 
from sklearn.model_selection import train_test_split # to split the data into two parts

from sklearn.preprocessing import StandardScaler # for normalization
from sklearn.preprocessing import MinMaxScaler



from sklearn import metrics # for the check the error and accuracy of the model
from sklearn.metrics import mean_squared_error,r2_score

## for Deep-learing:

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM

from tensorflow.keras.layers import Dropout
import tensorflow.keras as keras
# %matplotlib inline
def mainp(paths):
#df = pd.read_csv('household_power_consumption.txt', sep=';', header=0, low_memory=False, infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])
    df = pd.read_csv('', sep=';', parse_dates={'dt' : ['Date', 'Time']}, infer_datetime_format=True, low_memory=False, na_values=['nan','?'], index_col='dt')
    df.head()
    df.shape
    df.dtypes
    #df.replace('?',np.nan, inplace=True)
    #df.replace('nan',np.nan, inplace=True)
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
    values = df_.resample('D').mean()
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
    values = df_resample.values 
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
    n_train_time = 2*365*24
    train = values[:n_train_time, :]
    test = values[n_train_time:, :]
    ##test = values[n_train_time:n_test_time, :]
    # split into input and outputs
    train_X, train_y = train[:, :-1], train[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]
    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    # We reshaped the input into the 3D format as expected by LSTMs, namely [samples, timesteps, features].
    model = Sequential()
    model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # fit network
    dict={}
    history = model.fit(train_X, train_y, epochs=30, batch_size=50, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    dict['loss']=history.history['loss']
    dict['val_loss']=history.history['val_loss']
    import json
    yhat = model.predict(test_X)
    test_X = test_X.reshape((test_X.shape[0], 7))
    # invert scaling for forecast
    inv_yhat = np.concatenate((yhat, test_X[:, -6:]), axis=1)
    inv_yhat = scaler.inverse_transform(inv_yhat)
    inv_yhat = inv_yhat[:,0]
    # invert scaling for actual
    test_y = test_y.reshape((len(test_y), 1))
    inv_y = np.concatenate((test_y, test_X[:, -6:]), axis=1)
    inv_y = scaler.inverse_transform(inv_y)
    inv_y = inv_y[:,0]
    aa=[x for x in range(200)]
    dict1={}
    dict1['x_values']=aa
    dict1['y1']=list(inv_y[:200])
    dict1['y2']=list(inv_yhat[:200])
    model.save("tarp_model1.h5")
    with open("prediction_visual.json", "w") as f:
        json.dump(dict1, f)
    with open("train_accuracy_visual.json", "w") as f:
        json.dump(dict, f)
    print("done")
if __name__ == "__main__":
   print("The model is being trained")
   mainp(sys.argv[1])