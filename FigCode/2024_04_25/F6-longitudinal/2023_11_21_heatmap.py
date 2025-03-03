# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:40:13 2023

@author: lgxsv2
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from matplotlib.colors import Normalize

#%%  Create dataframe with relevant information. 
def csv(dirs=r'F:\GeomorphologyPaper\XPlane\dimensions\*2023.csv'):
    '''
    gets percentage change relative to image area.
    takes mean and max
    currently only 2023
    
    mean is skewed by what results we have and when

    '''
    dictionary = pd.read_csv(r"F:\GeomorphologyPaper\DataFolder\dictionaries\channelSizes.csv")
    
    #lists to add to 
    ids = []
    maxs = []
    means = []
    
    
    
    for fp in glob.glob(dirs):
        df = pd.read_csv(fp)
        df = df[pd.to_numeric(df['area'], errors='coerce').notnull()]
        y = df['area'].astype(int)
        
        
        ds = os.path.basename(fp)[:5]
        num = dictionary[dictionary['id'] == ds]['imsize']
        y = (y / int(num.iloc[0])) * 100
        y = y - y.iloc[0]
        
        maximum = y.max()
        mean = y.mean()
        
        
        ids.append(ds)
        maxs.append(maximum)
        means.append(mean)
    df = pd.DataFrame({'id':ids, 'maximum':maxs, 'mean':means})
    df.to_csv(r'F:\GeomorphologyPaper\XPlane\heatmap\initalcsv.csv')
    return df 
        
        

#%%
def simplisticHeatMapPannel(dffp=r"D:\GeomorphologyPaper\DataFolder\Products\heatmap\initalcsv.csv"):
    
    df = pd.read_csv(dffp)
    
    vals = list(df['maximum'])

    vals = np.array([vals])
    fig, ax = plt.subplots(2,1)
    ax[0].pcolor(vals)
    
    b = ax[0].pcolormesh(vals, cmap='viridis', shading='auto')
    
    ax[1].plot(df.id, df.maximum, marker='o', linestyle='-')#, color='viridis', marker='o', linestyle='-')
   
    plt.colorbar(b, label='Max deposition (%) rank', ax=ax[0])

    # Add labels and title
    ax[1].set_xlabel('Downstream ->')
    ax[1].set_ylabel('Max deposition (%)')
    ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation='vertical')
    c = ax[1].pcolormesh(vals, cmap='viridis', shading='auto')
    plt.colorbar(c, label='Max deposition (%) rank', ax=ax[1])

    # Show the plotb 
    plt.tight_layout() 
    plt.show()
    return df


def simplisticHeatMapCombined(dffp=r"D:\GeomorphologyPaper\DataFolder\Products\heatmap\initalcsv.csv"):
    
    df = pd.read_csv(dffp)
    
    vals = list(df['maximum'])

    vals = np.array([vals])
    fig, ax = plt.subplots(1,1)
    ax.set_xlabel('Downstream ->')
    ax.set_ylabel('Max island coverage (%)')


    ax.plot(df.id, df.maximum, linestyle='-', c='lightgrey', zorder=0)
    ax.scatter(df.id, df.maximum, marker='o', cmap='viridis', c=vals,alpha=1 )

    c = ax.pcolormesh(vals, cmap='viridis', shading='auto')
    plt.colorbar(c, label='Max relative island size rank', ax=ax)
    
    
    # ax.set_xticklabels(ax.get_xticklabels(), rotation='vertical')
    ax.set_xticklabels(np.arange(len(df)), rotation='vertical')

    ax.axvline(x=18.5, color='tan', alpha=0.5, linestyle='-', linewidth=5, label='Aripuan\u00E3')
    ax.axvline(x=5.5, color='darkkhaki', alpha=0.5, linestyle='-', linewidth=5, label = 'Ji-Paran\u00E3')
    
    ax.legend(title='Tributary positions')
    # Show the plotb 
    plt.tight_layout() 
    plt.show()
    return df
plt.close('all')
df = simplisticHeatMapCombined()
    

#%%
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.cm import ScalarMappable
# from matplotlib.colors import Normalize

# def simplisticHeatMapCombined(dffp=r"D:\GeomorphologyPaper\DataFolder\Products\heatmap\initalcsv.csv"):
#     df = pd.read_csv(dffp)
    
#     vals = list(df['maximum'])
#     vals = np.array([vals])
    
#     fig, ax = plt.subplots(1, 1)
    
#     # Create a ScalarMappable to map values to colors consistently
#     norm = Normalize(vmin=vals.min(), vmax=vals.max())
#     sm = ScalarMappable(cmap='viridis', norm=norm)
#     sm.set_array([])

#     # Plot the line with color mapping
#     line = ax.plot(df['id'], df['maximum'], marker='o', linestyle='-', c=sm.to_rgba(vals[0]))[0]
    
#     # Add colorbar using the ScalarMappable
#     cbar = plt.colorbar(sm, ax=ax, label='Max deposition (%) rank')

#     # Set labels and title
#     ax.set_xlabel('Downstream ->')
#     ax.set_ylabel('Max relative island size (%)')

#     # Rotate x-axis tick labels vertically
#     ax.set_xticklabels(ax.get_xticklabels(), rotation='vertical')

#     # Show the plot
#     plt.tight_layout() 
#     plt.show()
    
#     return df

# plt.close('all')
# df = simplisticHeatMapCombined()
