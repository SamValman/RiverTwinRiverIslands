# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 23:25:23 2023

@author: lgxsv2
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
import os

os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")

import Fims


def panelFim(driver='D:'): 
    gs = gridspec.GridSpec(2, 2)
    pl.figure()
    
    # bar one yearly DS_13 - just dry season
    ax = pl.subplot(gs[0, 0]) # row 0, col 0
    # use csvs in dryseason
    x,y = Fims.plotOne(driver)
    pl.bar(x, y, alpha=0.5, color='Darkgrey', label='DS 13 usable dry season images')
    ax.set_ylabel('Usable images')
    pl.legend()
    ax.text(-0.09, 0.94, 'a)', transform=ax.transAxes, ha='center')

    
    # bar two 2021 to 2023 - should I include the data that is now available for the rest of 2023
    ax = pl.subplot(gs[0, 1]) # row 0, col 1
    ax.set_ylabel('Usable images')
    ax.text(-0.1, 0.94, 'b)', transform=ax.transAxes, ha='center')

    # all year - use csv in fullyear
    x,yDry, yRest = Fims.plotTwo(driver)
    x = [str(i) for i in x]
    pl.bar(x, yDry, alpha=0.5, color='grey', label='Drought Season')
    pl.bar(x, yRest, alpha=0.6, color='black', label='rest of year', bottom=yDry)
    pl.legend(loc='lower left')
    
    
    # scatterdry season siz, image number, distance ds 
    ax = pl.subplot(gs[1, :]) # row 1, span all columns
    ax.text(-0.05, 0.94, 'c)', transform=ax.transAxes, ha='center')

    # only use csvs in xx. 
    x,y,z = Fims.plotThree(driver)



    pl.scatter(x,y, cmap='viridis', c=z)
    pl.xlabel('Usable images')
    pl.ylabel('Size of site (km$^2$)')
    clb = pl.colorbar()
    clb.set_label('Ranked distance downstream of AOI')
    ## we want a pannel of yearly images as we already have 
    ## then a number of images in and not in the right season. 
    # Do we include all the data - 2023 number of complete images, size of site c= distance downstream 
    


    # Show the plot
    plt.show()














#%%
plt.close('all')
panelFim()

#%%Get Stat

x,yDry, yRest = Fims.plotTwo(driver="D:")
for yr, dry, rest in zip(x,yDry, yRest):
    percent = (rest/(dry+rest))*100
    print(str(yr)+': '+str(percent))