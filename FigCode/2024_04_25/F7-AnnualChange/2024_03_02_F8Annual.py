# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:39:26 2024

@author: lgxsv2
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.dates as mdates



os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
import module
#%%


def organiseDate(df):
    df['date'] = df['date'].astype(str).str[-4:]  # get monthday
    df['date'] = pd.to_datetime(df['date'], format='%m%d', errors='coerce')
    # df['month_day'] = df['date'].dt.strftime('%m%d')
    df = df.sort_values(by="date")

    return df






#%% Pannel Function 


def F8AnnualChange(years, ls_ds, dirs=r"D:\GeomorphologyPaper\DataFolder\Products\dimensions_fullYear"):
    
    
    # set up figure with two pannels:
        #1. DS 13 each year overlapping (Blues..)
        #2. ls_ds (the five ds') continues record 2021 - 2023
    fig, ax = plt.subplots(2,1)
    
    
    
    
    ###########################################################################
    # Part 1 : DS_13 annual 2016-2023
    ###########################################################################

    # years are set 
    P1years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    P1d = {'2016':'springgreen', '2017':'aquamarine', '2018':'darkcyan', '2019':'royalblue', '2020':'blue', '2021':'navy', '2022':'grey','2023':'black' }

    # for each year 
    for year in P1years:        
        #find csv
        csv = os.path.join(r"D:\GeomorphologyPaper\DataFolder\Products\dimensions_drySeason", ("DS_13"+'_' + str(year)+'.csv'))
        df = pd.read_csv(csv)
        # convert to %
        df = module.convertBase0(df, 'DS_13', dirs)
        # make dates roll together
        df = organiseDate(df)
    
        # plot 
        c = P1d[year]
        ax[0].plot(df.date,df.base, label=year, c=c) # +', '
        print(f"year: {year}, max val: {max(df.base)}")
        print(f"year: {year}, end val: {df.base.iloc[-1]}")

    # write legend and set lenght y axis
    ax[0].legend(ncol=len(years))
    ax[0].set_ylabel('Island coverage (%)')
    ax[0].yaxis.set_label_coords(-0.05, 0)
    
    


    ###########################################################################
    # Part 2 : 5 DS 2021-2023
    ###########################################################################
    d = {'DS_01':'aquamarine', 'DS_13':'darkcyan', 'DS_14':'royalblue', 'DS_24':'blue', 'DS_34':'navy'}
    for ds in ls_ds:
        dsdf=pd.DataFrame()
        for year in years:
            # get fp
            fp = os.path.join(dirs,(ds+'_'+year+'.csv') )
            # get df
            df = pd.read_csv(fp)
            # turn df to percentages
            df = module.convertBase0(df, ds, dirs)
            print(len(df))
            # need to put these dfs together to print as one. 
            dsdf = pd.concat([dsdf, df])
        # sort dates
        dsdf['date'] = dsdf['date'].astype(str)
        # base func is set to monthDay so extra args for YYYYMMDD
        dsdf = module.organiseDate(dsdf, '%Y%m%d', False)
        # plot 
        smooth = dsdf['base'].rolling(window=2).mean()

        c = d[ds]
        ax[1].plot(dsdf.date, smooth, label=('Ds '+str(ds[-2:])), color=c)
    ax[1].legend()
    # ax[1].set_ylabel('Relative island change (%)')
    ax[1].set_xlabel('Date')

    






    ax[1].text(-0.039, 0.9, 'b)', transform=ax[1].transAxes, ha='center')
    ax[0].text(-0.039, 0.9, 'a)', transform=ax[0].transAxes, ha='center')
    
            
    # ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    # ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    tick_labels = ['Jul', 'Aug', 'Sep', 'Oct']
    tick_locs = pd.date_range(start='1900-07-01', end='1900-10-31', freq='MS')

    ax[0].set_xticks(tick_locs)
    ax[0].set_xticklabels(tick_labels)
    plt.show()
    
#%% Run Pannel 

years=['2023', '2022', '2021']  
ls_ds=['DS_01', 'DS_13', 'DS_14', 'DS_24', 'DS_34']
F8AnnualChange(years=years, ls_ds=ls_ds)


#%%
    # for ds in ls_ds:
        
    #     for year in years:
    #         # get fp
    #         fp = os.path.join(dirs,(ds+'_'+year+'.csv') )
    #         # get df
    #         df = pd.read_csv(fp)
    #         # turn df to percentages
    #         df = module.convertBase0(df, ds)
    #         df = organiseDate(df)
    #         # symbol 
            
    #         # symbol = d_symbol[year]
    #         # color 
    #         color = d_color[year]
    #         # plot 
    #         ax[1].plot(df.date, df.base, c=color, label=year)
    #         line, = ax[1].plot(df.date, df.base, c=color)  # marker=symbol
    #         lines.append(line)# marker=symbol