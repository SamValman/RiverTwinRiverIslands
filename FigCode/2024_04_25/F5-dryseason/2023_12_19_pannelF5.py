# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 23:55:57 2023

@author: lgxsv2
"""


import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib as mpl
import os
import pandas as pd 
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
import F1Funcs
import module
#%%
def FOne(ls_ds, dirs=r"D:\GeomorphologyPaper\DataFolder\Products\dimensions_drySeason"):
    """
    There a smoothing function that can be added from the archive/moduel of functions 

    Parameters
    ----------
    ls_ds : TYPE
        DESCRIPTION.
    dirs : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    
    fig, ax = plt.subplots(2,1)
    # top fig = percentages 
    
    
    
    # bottom fig = derivs
    cmap = plt.get_cmap('viridis')
    dfs = [] # for avg
    for cnumber, ds in enumerate(ls_ds):
        # get c map
        c = cmap(cnumber/len(ls_ds))
        
        
        # get the csv for 2023 dry season
        csv = os.path.join(dirs, (ds+'_2023.csv'))
        df = pd.read_csv(csv)
        df = df[df['area']!=0]
        
        
        # convert 
        df = module.convertBase0(df, ds)
        

        # sort date to dt
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        
        #plot percent 
        ax[0].plot(df.date, df.base, color=c)
        

        # dfs for average line
        df_r = F1Funcs.resample(df)
        df_r = F1Funcs.getSlope(df_r, resample=True).reset_index()
        dfs.append(df_r)
        
        df = F1Funcs.getSlope(df, resample=True)


        # plot deriv
        ax[1].plot(df.index,df, color=c, alpha=0.5)
    
    ax[1].text(-0.05, 0.93, 'b)', transform=ax[1].transAxes, ha='center')
    ax[0].text(-0.05, 0.96, 'a)', transform=ax[0].transAxes, ha='center')

    #the combined
    # F1Funcs.makeColorbar(axs=0, ax=ax, cmap=cmap, ls_ds=ls_ds)

    tot = pd.concat(dfs, ignore_index=True)
    # Group by 'date' and calculte the sum of 'base'
    tot = tot.groupby('date')['slope'].mean().reset_index()
    
    ax[1].plot(tot.date, tot.slope, color='black', label='Mean averaged derivatives')
    ax[1].legend()

    ax[1].set_xlabel('Date')
    F1Funcs.makeColorbar(axs=1, ax=ax, cmap=cmap, ls_ds=ls_ds)
    
    #cbar axis 1
    ax[0].set_ylabel('Island coverage (%)')
    ax[0].xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=len(ls_ds)))
    sm.set_array([])  # You need to set an array for the ScalarMappable
    
    
 # Add colorbar 
    cbar = fig.colorbar(sm,ax=ax[0], label='Distance downstream (rank)')

    
    plt.show()
    
#%%
plt.close('all')
ds = [ 'DS_00','DS_01', 'DS_02', 'DS_03','DS_04', 'DS_05','DS_06','DS_07','DS_08', 'DS_09', 'DS_10',
    'DS_11', 'DS_12', 'DS_13','DS_14', 'DS_15','DS_16','DS_17','DS_18',
    'DS_19','DS_20','DS_21','DS_22','DS_23', 'DS_24', 'DS_25', 'DS_26', 'DS_27', 'DS_28', 'DS_29', 
    'DS_30', 'DS_31', 'DS_32', 'DS_33', 'DS_34']
# ds = ['DS_22']
FOne(ls_ds=ds)
    