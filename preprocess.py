import pandas as pds
import pickle
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from numpy.lib.stride_tricks import as_strided

def get_weights(serie, bins):
    a, b = np.histogram(serie, bins=bins)
    weights = 1/(a[1:]/np.sum(a[1:]))
    weights = np.insert(weights, 0,1)
    weights_Serie = pds.Series(index = serie.index, data=1)
    for i in range(1, bins):
        weights_Serie[(serie>b[i]) & (serie<b[i+1])] = weights[i]
    return weights_Serie

def windowed(X, window):
    '''
    Using stride tricks to create a windowed view on the original
    data.
    '''
    shape = int((X.shape[0] - window) + 1), window, X.shape[1]
    strides = (X.strides[0],) + X.strides
    X_windowed = np.lib.stride_tricks.as_strided(X, shape=shape, strides=strides)
    return X_windowed

def getyeardata(years,data):
    for i, year in enumerate(years):
        if i == 0:
            result = data[data.index.year == year]
        else:
            result = pds.concat([result, data[data.index.year == year]], sort=True)
    return result.sort_index()

def getdatas(train,test,val,data_scaled,truelabel,truelabel2=None):
    X_test = getyeardata(test,data_scaled)
    Y_test = getyeardata(test,truelabel)
    
    X_val = getyeardata(val,data_scaled)
    Y_val = getyeardata(val,truelabel)
    
    X_train = getyeardata(train,data_scaled)
    Y_train = getyeardata(train,truelabel)
    
    if truelabel2 is not None:
        ind_test = getyeardata(test,truelabel2)
        ind_train = getyeardata(train,truelabel2)
        ind_val = getyeardata(val,truelabel2)
    
        return X_test, Y_test, X_val, Y_val, X_train, Y_train, ind_test,ind_train,ind_val
    else:
        return X_test, Y_test, X_val, Y_val, X_train, Y_train