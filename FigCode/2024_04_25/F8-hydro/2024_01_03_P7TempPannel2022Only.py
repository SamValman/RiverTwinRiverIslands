# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:49:51 2023

@author: lgxsv2
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import os 
from scipy import stats
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable


# pannel with just 2022 data 
# edit this after 
#%% same df building products
def sortGuage(fp):
    df_og = pd.read_csv(fp)
    
    # month year and each day of the month (MS access probly)
    cols = ['Data', 'Cota01', 'Cota02', 'Cota03',
    'Cota04', 'Cota05', 'Cota06', 'Cota07', 'Cota08', 'Cota09', 'Cota10',
    'Cota11', 'Cota12', 'Cota13', 'Cota14', 'Cota15', 'Cota16', 'Cota17',
    'Cota18', 'Cota19', 'Cota20', 'Cota21', 'Cota22', 'Cota23', 'Cota24',
    'Cota25', 'Cota26', 'Cota27', 'Cota28', 'Cota29', 'Cota30', 'Cota31']
    df = df_og[cols]
    df = df.rename(columns={'Data':'date'} )
    
    
    # limit date to 2021 to 2023
    df = df[df['date'].str.slice(start=-2).isin(['23','22','21'])]
    # remove doubles
    df = df.drop_duplicates(['date'])
    
    # dt the first column
    # covers old version which was the b y 
    try:
        df['date'] = pd.to_datetime(df['date'], format='%b-%y') # wrong here 
    except:
        df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y")  

    # Melt makes it two cols for output df 
    odf = pd.melt(df, id_vars=['date'], var_name='day', value_name='value')

    # new "date" column by combining "date" and "day" 
    odf['day'] = odf['day'].str.extract('(\d+)')  # Extract day from column header
    odf['date'] = odf['date'] + pd.to_timedelta(odf['day'].astype(int) - 1, unit='D')

    # Drop "day" column
    odf = odf.drop('day', axis=1)

    # order by date
    df = odf.sort_values(by='date')
    df = df.dropna()
    
    
    return df




def combineDischargeAndIslands(guage, years=[], ds_ls=['DS_01','DS_13', 'DS_14', 'DS_24', 'DS_34'], path=r'D:\GeomorphologyPaper\DataFolder\Products\dimensions_fullYear'):
    ls_dfs = []
    for year in years:
        for ds in ds_ls:
            fp = os.path.join(path, (f"{ds}_{year}.csv"))
            df = pd.read_csv(fp)
            df = df[['date','area']]
            df['id']=ds
            ls_dfs.append(df)
    df = pd.concat(ls_dfs, ignore_index=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # join based on date
    df = pd.merge(df, guage, on='date', how='left')
    
    return df


#%%
# this code is written out twice here - if I get a chance I will programme properly
# - not currently a priority
def convertBase0(df):
    dictionary = pd.read_csv(r"D:\GeomorphologyPaper\DataFolder\Products\dictionaries\channelSizes.csv")
    newdf = pd.DataFrame()
    for i in df.id.unique():
        tdf = df[df['id']==i].copy()
        num = dictionary[dictionary['id']==i]['imsize']
        y = tdf.area

        y = (y/int(num.iloc[0]))*100
        y = y - y.iloc[0]
        tdf.loc[:, 'base'] = y # just sets the base col as new y
        newdf = pd.concat([newdf,tdf])
    return newdf


def PannelF7(df):
    
    
    fig, ax = plt.subplots(2,1, sharex=True)
    ############################# AX 0:  all data #############################
    df1 = df.copy()
    
    # set color labels
    # Create a color map based on dates
    df1['month'] = df1['date'].dt.month


    # get base compared to first measure
    df1 = convertBase0(df1)    
    # put into vars
    x = df1.value
    y = df1.base
   # plot on ax0
    sc = ax[0].scatter(x, y, c=df1['month'], cmap='viridis') #label=df1.i
    
    # # trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    # #add trendline to plot
    ax[0].plot(x, p(x), color='black')     
    # r^2
    rsq, pval = stats.pearsonr(x,y)
    
    # put in box 
    textstr = '\n'.join((
        r'$r^2=%.2f$' % (rsq**2, ),
        r'$p=%.2f$' % (pval, )))
    props = dict( facecolor='None', alpha=0.5)
    upper = y.max()-0.001
    ax[0].text(1450, upper, textstr, fontsize=14,
    verticalalignment='top', bbox=props)  #### here might be an issue
    # ax[0].legend()

    
    divider = make_axes_locatable(ax[0])

    # Append an axis for the color bar on the right
    cax = divider.append_axes("right", size="5%", pad=0.05)

    # Add the colorbar to the cax axis
    cbar = plt.colorbar(sc, cax=cax, orientation='vertical', label='Date')
    cbar.set_label('Month')
    
    
    
    ############################# AX 1:  split into sections ##################

    
    # ax[1]
    for i in df.id.unique():
        tdf = df1[df1['id']==i]
 
        x = tdf.value
        y = tdf.base
        
        #get a line 
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        # plot a line
        plt.plot(x, p(x)) # , width=2)
        
        # get stats per group
        rsq, pval = stats.pearsonr(x,y)
        
        # just print for now 
        textstr = 'DS '+str(i[-2:]) +' r$^2$: '+str(round((rsq*rsq),2))+' , p: '+ str(round(pval,2))

        
        # plot this
        ax[1].scatter(x,y, label=textstr)
        

        
        # base.extend(list(y))            
    ax[1].legend()
    
    
    
    # all labels
    ax[1].set_xlabel('Discharge (height at guage)')
    ax[0].set_ylabel('Island coverage (%)')
    ax[1].set_ylabel('Island coverage (%)')
    ax[1].text(-0.05, 0.92, 'b)', transform=ax[1].transAxes, ha='center')
    ax[0].text(-0.05, 0.94, 'a)', transform=ax[0].transAxes, ha='center')
    
    plt.show()
            
            

plt.close('all')



#%%
fp = r"D:\GeomorphologyPaper\Analysis\Figures\2024_04_25\F8-hydro\guageCSVs\15400000_Cotas_2024_formatted.csv"

guage = sortGuage(fp)
df1 = combineDischargeAndIslands(guage,['2023','2022', '2021'] )
df1 = df1.dropna()
PannelF7(df1)

# fp = r"D:\GeomorphologyPaper\Analysis\Figures\2024_04_25\F8-hydro\guageCSVs\15400000_Cotas.csv"
# guage = sortGuage(fp)
# df = combineDischargeAndIslands(guage,['2022', '2021'] )
# PannelF7(df)



#%%
# alternative r2 
# pause at line 114 and run this code:
# df1 = df1[df1['id']!='DS_34']
# x = df1.value
# y = df1.base
# rsq, pval = stats.pearsonr(x,y)

# # put in box 
# textstr = '\n'.join((
#     r'$r^2=%.2f$' % (rsq**2, ),
#     r'$p=%.2f$' % (pval, )))