import pandas as pds
import datetime
import numpy as np
import math
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


class Crossing:
    
    def __init__(self,crosstime):
        
        self.crosstime = crosstime
        
    def __eq__(self, other, diff = 30):
        '''
        return True if time difference < diff
        '''
        return crossdiff(self,other)<datetime.timedelta(seconds = diff)
    
    def plot_similaritymap(self, data, delta, i, prediction):
        return plot_similaritymap(data, self.crosstime, delta, i, prediction)
    
    def plot_cross(self,data,delta,label,pred):
        return plot_cross(data,self.crosstime,delta,label,pred)
        

def plot_cross(data, crosstime, delta, label,pred):

    sns.set_style('darkgrid')
    sns.set_context('paper')
    
    n_plots = 3
    ns = [311,312,313]
    if pred is not None:
        n_plots +=1
        ns = [411,412,413,414]
    if label is not None:
        n_plots +=1
        ns = [511,512,513,514,515]    
        
    fig=plt.figure(figsize=(12,6))
   
    data = data[crosstime-datetime.timedelta(minutes=delta):crosstime+datetime.timedelta(minutes=delta)]

    
    
    
    ax1 = plt.subplot(ns[0])
    plt.title('Bow Shock Crossing - '+crosstime.strftime("%Y-%b-%d %H:%M"))
    ax1.plot_date(data.index, data['b_gse_x'],'-r',label='Bx',linewidth=0.5)
    ax1.plot_date(data.index, data['b_gse_y'],'-g',label='By',linewidth=0.5)
    ax1.plot_date(data.index, data['b_gse_z'],'-b',label='Bz',linewidth=0.5)
    ax1.plot_date(data.index, data['b_abs'],'-k',label='Btotal',lw=0.5)
    
     #plot vertical line
    ax1.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('B [nT]')
    plt.legend(loc=3,ncol=4,fontsize=8)
     
    try:
        ax1.set_ylim(-np.nanmax(data['b_abs'])-5,np.nanmax(data['b_abs'])+5)
    except:
        pass
    
    ax2 = plt.subplot(ns[1]) 

    ax2.plot_date(data.index, data['vel_gse_x'],'-r',label='Vx',linewidth=0.5)
    ax2.plot_date(data.index, data['vel_gse_y'],'-g',label='Vy',linewidth=0.5)
    ax2.plot_date(data.index, data['vel_gse_z'],'-b',label='Vz',linewidth=0.5)
    ax2.plot_date(data.index, data['v_abs'],'-k',label='Vtotal',lw=0.5)
    
     #plot vertical line
    ax2.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('V [km/s]')
    plt.legend(loc=3,ncol=4,fontsize=8)
     
    try:
        ax2.set_ylim(-np.nanmax(data['v_abs'])-50,np.nanmax(data['v_abs'])+50)
    except:
        pass
    
    ax3 = plt.subplot(ns[2])
                      
    ax3.plot_date(data.index, data['dens'],'-r',label='N',linewidth=0.5)

    ax3.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('N [cm-3]')
    plt.legend(loc=3,ncol=4,fontsize=8)
    
    try:
        ax3.set_ylim(-np.nanmax(data['dens'])-5,np.nanmax(data['dens'])+5)
    except:
        pass
    
    if label is not None:
        
        try:
            
            label = label[crosstime-datetime.timedelta(minutes=delta):crosstime+datetime.timedelta(minutes=delta)]
        except:
            return
        
        ax4 = plt.subplot(ns[3])

        #try:
        ax4.plot_date(label.index,label['0'],linewidth=0.5)
        #except:
         #   pass
        try:
        
            ax4.plot(label.index, label['0'],linewidth=0.5)
        except:
            pass
    
        try:
            ax4.plot(label.index, label['label'],linewidth=0.5)
            
        except:
            pass
        ax4.set_ylim(-0.5,1.5)
        plt.ylabel('label')
        
    if pred is not None:
        
        ax5 = plt.subplot(ns[4], sharex = ax1)

        try:
            pred = pred[crosstime-datetime.timedelta(minutes=delta):crosstime+datetime.timedelta(minutes=delta)]
            ax5.plot(pred.index, pred['pred'],linewidth=0.5)
            
        except:
            return
        ax5.set_ylim(-0.5,1.5)
        plt.ylabel('prediction')
     
    
    

        
    plt.tight_layout()
    plt.show()
    
        
def crossdiff(crossing1, crossing2):
    '''return the time difference between two crossings as a timedelta'''
    delta = crossing1.crosstime - crossing2.crosstime
    return abs(delta)

def get_crosslist(path, sc, years):
    
    crosslistdf = pds.read_csv(path, sep=" ", header = None)
    crosslistdf.set_index(0,  inplace=True)
    crosslistdf.index.name = None
    crosslistsc = crosslistdf[crosslistdf.index == sc]
    crosslists = crosslistsc[1].values.tolist()
    crosslist = []
    for i in crosslists:
        cross = datetime.datetime.strptime(i, "%Y-%m-%dT%H:%M:%S")
        if cross.year in years:
            crosslist.append(Crossing(datetime.datetime(cross.year,cross.month,cross.day,cross.hour,cross.minute)))
    return crosslist

def get_crosslistngu(path, years):
    
    crosslistdf = pds.read_csv(path,index_col=0)
    crosslistdf['cross']=pds.to_datetime(crosslistdf['cross'])
    crosslists = crosslistdf['cross'].tolist()
    crosslist = []
    for i in crosslists:
        if i.year in years:
            crosslist.append(Crossing(i))
    return crosslist

def crossdifffromlist(ref_event, event_list):
    '''
    return the list of the time difference between a crossing and the elements of
    a crosslist
    '''
    return [crossdiff(ref_event, elt) for elt in event_list]

def isInList(ref_event, event_list, diff):
    '''
    returns True if delta less than diff for atleast one crossing
    '''
    return min(crossdifffromlist(ref_event,event_list)) < datetime.timedelta(minutes = diff)
    

def crossingsperyear(crosslist,years):
    for year in years:
        print(str(year) + ': '+str(len([x for x in crosslist if (x.crosstime.year==year)])))
    #ax.set_title('Number of Events in Eventlists')
    
    
def plot_results(data, label,pred,testhour):

    sns.set_style('darkgrid')
    sns.set_context('paper')
    
    n_plots = 3
    ns = [311,312,313]
    if pred is not None:
        n_plots +=1
        ns = [411,412,413,414]
    if label is not None:
        n_plots +=1
        ns = [511,512,513,514,515]    
        
    fig=plt.figure(figsize=(12,6))
    
    predind = pred[(pred.index.year == testhour.year)&(pred.index.month==testhour.month)&(pred.index.day==testhour.day)&(pred.index.hour==testhour.hour)].index
    pred = pred.loc[predind]
    data = data.loc[predind]
    label = label.loc[predind]
        
    ax1 = plt.subplot(ns[0])
    #plt.title('Bow Shock Crossing - '+crosstime.strftime("%Y-%b-%d %H:%M"))
    ax1.plot_date(data.index, data['b_gse_x'],'-r',label='Bx',linewidth=0.5)
    ax1.plot_date(data.index, data['b_gse_y'],'-g',label='By',linewidth=0.5)
    ax1.plot_date(data.index, data['b_gse_z'],'-b',label='Bz',linewidth=0.5)
    ax1.plot_date(data.index, data['b_abs'],'-k',label='Btotal',lw=0.5)
    
     #plot vertical line
    #ax1.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('B [nT]')
    plt.legend(loc=3,ncol=4,fontsize=8)
     
    try:
        ax1.set_ylim(-np.nanmax(data['b_abs'])-5,np.nanmax(data['b_abs'])+5)
    except:
        pass
    
    ax2 = plt.subplot(ns[1]) 

    ax2.plot_date(data.index, data['vel_gse_x'],'-r',label='Vx',linewidth=0.5)
    ax2.plot_date(data.index, data['vel_gse_y'],'-g',label='Vy',linewidth=0.5)
    ax2.plot_date(data.index, data['vel_gse_z'],'-b',label='Vz',linewidth=0.5)
    ax2.plot_date(data.index, data['v_abs'],'-k',label='Vtotal',lw=0.5)
    
     #plot vertical line
    #ax2.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('V [km/s]')
    plt.legend(loc=3,ncol=4,fontsize=8)
     
    try:
        ax2.set_ylim(-np.nanmax(data['v_abs'])-50,np.nanmax(data['v_abs'])+50)
    except:
        pass
    
    ax3 = plt.subplot(ns[2])
                      
    ax3.plot_date(data.index, data['dens'],'-r',label='N',linewidth=0.5)

    #ax3.plot_date([crosstime,crosstime],[-500,500],'-k',linewidth=1)  
    
    plt.ylabel('N [cm-3]')
    plt.legend(loc=3,ncol=4,fontsize=8)
    
    try:
        ax3.set_ylim(-np.nanmax(data['dens'])-5,np.nanmax(data['dens'])+5)
    except:
        pass
    
    if label is not None:
        
        ax4 = plt.subplot(ns[3])

        #try:
        ax4.plot_date(label.index,label['0'],linewidth=0.5)
        #except:
         #   pass
        try:
            ax4.plot(label.index, label['0'],linewidth=0.5)
        except:
            pass
    
        try:
            ax4.plot(label.index, label['label'],linewidth=0.5)
            
        except:
            pass
        ax4.set_ylim(-0.5,1.5)
        plt.ylabel('label')
        
    if pred is not None:
        
        ax5 = plt.subplot(ns[4], sharex = ax1)

        try:
            ax5.plot(pred.index, pred['pred'],linewidth=0.5)
            
        except:
            pass
        ax5.set_ylim(-0.5,1.5)
        plt.ylabel('prediction')
     
    
    

        
    plt.tight_layout()
    plt.show()