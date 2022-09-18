import pandas as pds
import datetime
import numpy as np
import time
import preprocess

def windowed(X, window):
    '''
    Using stride tricks to create a windowed view on the original
    data.
    '''
    shape = int((X.shape[0] - window) + 1), window, X.shape[1]
    strides = (X.strides[0],) + X.strides
    X_windowed = np.lib.stride_tricks.as_strided(X, shape=shape, strides=strides)
    return X_windowed

def geteventhours(crosslist,years):
    hours = []
    for y in years:
        for m in range(1,13):
            for d in range(1,32):
                for h in range(1,24):
                    crossings = [x for x in crosslist if ((x.crosstime.month == m) & (x.crosstime.day == d) & (x.crosstime.year == y)& (x.crosstime.hour == h))]
                    if len(crossings) != 0:
                        hours.append(datetime.datetime(y,m,d,h))
    return hours

import window as wdw

def createwindows(crosslist,x,y,window,years, weight,test):
    y['timestamp']=y.index
    
    eventdays = geteventhours(crosslist,years)
    
    x_windowed = []
    i=True
    c = 1
    
    for day in eventdays:
        print('finished ' + str(np.floor(c/len(eventdays)*100)) + '%', end='\r')
        data = x[(x.index.month == day.month) & (x.index.day == day.day) & (x.index.year == day.year)& (x.index.hour == day.hour)]
#        print(data)
        targets = y[(y.index.month == day.month) & (y.index.day == day.day) & (y.index.year == day.year)&(y.index.hour == day.hour)]
        #print(targets)
        c = c+1
        try:
            dataw = windowed(data.values, window=window)
            for w in dataw:
                x_windowed.append(w.tolist())
            targetsw = np.ravel(targets.values[int(window/2)-1:-int(window/2)])
            if i == True:
                y_windowed = np.array(targetsw)
                i = False
            else:
                y_windowed = np.concatenate((y_windowed,targetsw))
        except:
            pass
    
    print('windowing done')
    
    y_r = y_windowed.reshape((-1,2))
    y_df = pds.DataFrame(index=y_r[:,1],data=y_r[:,0])
    if weight is True:
        weights = preprocess.get_weights(np.squeeze(y_df), 10)
        return np.array(x_windowed),y_r[:,0].astype(np.float64),weights
    else:
        if test is True:
            return np.array(x_windowed),y_r[:,0].astype(np.float64),y_df
        else:
            return np.array(x_windowed),y_r[:,0].astype(np.float64)
        
    
def createtest(crosslist,x,y,window,years):
    eventdays = []
    y['timestamp']=y.index
    
    for j in years:
        for m in range(1,13):
            for d in range(1,32):
                crossings = [x for x in crosslist if ((x.crosstime.month == m) & (x.crosstime.day == d) & (x.crosstime.year == j))]
                if len(crossings) != 0:
                    eventdays.append(datetime.datetime(j,m,d))
                    
    
    
    x_windowed = []
    i=True
    c = 1
    
    for day in eventdays:
        print('finished ' + str(np.floor(c/len(eventdays)*100)) + '%', end='\r')
        data = x[(x.index.month == day.month) & (x.index.day == day.day) & (x.index.year == day.year)]
        targets = y[(y.index.month == day.month) & (y.index.day == day.day) & (y.index.year == day.year)]
        c = c+1
        try:
            dataw = windowed(data.values, window=window)
            for w in dataw:
                x_windowed.append(w.tolist())
            targetsw = np.ravel(targets.values[int(window/2)-1:-int(window/2)])
            if i == True:
                y_windowed = np.array(targetsw)
                i = False
            else:
                y_windowed = np.concatenate((y_windowed,targetsw))
        except:
            pass
        
    print('windowing done')
    
    y_r = y_windowed.reshape((-1,2))
    y_df = pds.DataFrame(index=y_r[:,1],data=y_r[:,0])
    return np.array(x_windowed),y_r[:,0].astype(np.float64),y_df


def createrandomwindows(x,y,window,eventhours):
    y['timestamp']=y.index
    
    x_windowed = []
    i=True
    c = 1
    
    for hour in eventhours:
        print('finished ' + str(np.floor(c/len(eventhours)*100)) + '%', end='\r')
        data = x[(x.index.month == hour.month) & (x.index.day == hour.day) & (x.index.year == hour.year)& (x.index.hour == hour.hour)]
#        print(data)
        targets = y[(y.index.month == hour.month) & (y.index.day == hour.day) & (y.index.year == hour.year)&(y.index.hour == hour.hour)]
        #print(targets)
        c = c+1
        try:
            dataw = windowed(data.values, window=window)
            for w in dataw:
                x_windowed.append(w.tolist())
            targetsw = np.ravel(targets.values[int(window/2)-1:-int(window/2)])
            if i == True:
                y_windowed = np.array(targetsw)
                i = False
            else:
                y_windowed = np.concatenate((y_windowed,targetsw))
        except:
            pass
    
    print('windowing done')
    
    y_r = y_windowed.reshape((-1,2))
    y_df = pds.DataFrame(index=y_r[:,1],data=y_r[:,0])
    return np.array(x_windowed),y_r[:,0].astype(np.float64)

def createrandomtest(x,y,window,eventhours):
    y['timestamp']=y.index
    
    x_windowed = []
    i=True
    c = 1
    
    for hour in eventhours:
        print('finished ' + str(np.floor(c/len(eventhours)*100)) + '%', end='\r')
        data = x[(x.index.month == hour.month) & (x.index.day == hour.day) & (x.index.year == hour.year)& (x.index.hour == hour.hour)]
#        print(data)
        targets = y[(y.index.month == hour.month) & (y.index.day == hour.day) & (y.index.year == hour.year)&(y.index.hour == hour.hour)]
        #print(targets)
        c = c+1
        try:
            dataw = windowed(data.values, window=window)
            for w in dataw:
                x_windowed.append(w.tolist())
            targetsw = np.ravel(targets.values[int(window/2)-1:-int(window/2)])
            if i == True:
                y_windowed = np.array(targetsw)
                i = False
            else:
                y_windowed = np.concatenate((y_windowed,targetsw))
        except:
            pass
    
    print('windowing done')
    
    y_r = y_windowed.reshape((-1,2))
    y_df = pds.DataFrame(index=y_r[:,1],data=y_r[:,0])
    return np.array(x_windowed),y_df
