# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 11:25:21 2023

@author: lgxsv2

# calling this F1 but currently has the CWT results in as well 
"""
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib as mpl

def getSlope(df, resample=False):
    '''
    resamples,interpolates then calculates derivitives of the slope
    may need previous resampling.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    slope : TYPE
        DESCRIPTION.

    '''
    x = df.set_index('date')
    d = df.date
    if resample:
        x = x.resample('D').interpolate()
        d = x.index
    # GET A df for 
    slope = pd.Series(np.gradient(x.base), d, name='slope')

    return slope

#%%
def resample(df):
    df = df[['date', 'base']]
    start_date = pd.to_datetime('2023-07-01')
    end_date = pd.to_datetime('2023-10-31')

    # Example: Resample to a common time grid (daily in this case)
    common_time_grid = pd.date_range(start=start_date, end=end_date, freq='D')
    df_resampled = df.set_index('date').reindex(common_time_grid).interpolate(method='linear')
    df_resampled = df_resampled.reset_index()
    df_resampled.rename(columns={'index': 'date'}, inplace=True)

    return df_resampled
#%%
def makeColorbar(axs, ax, cmap, ls_ds, label='Distance downstream (rank)'):  
    if axs:
        # cax = ax[axs].inset_axes([1.05, 0, 0.05, 1])  # Define the colorbar axes position
        ax[axs].xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
        ax[axs].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax[axs].set_ylabel('Slope derivative') 

        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=len(ls_ds)))
        sm.set_array([])  # You need to set an array for the ScalarMappable

    # Add colorbar 
        # cbar = plt.colorbar(sm, cax=cax, label=label)
        cbar = plt.colorbar(sm, ax=ax[axs], label=label)        

                
    else:
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.ylabel('Slope derivitive') 
    
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=len(ls_ds)))
        sm.set_array([])  # You need to set an array for the ScalarMappable
        
         # Add colorbar 
        cbar = plt.colorbar(sm, label=label)
    return cbar