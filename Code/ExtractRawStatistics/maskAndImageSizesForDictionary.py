# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 16:41:34 2023

@author: lgxsv2
"""

import skimage.io as io
from mask_image import getMask
from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


fp = r'D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023'

def createDict(fp):
    c1 = []
    c2 = []
    c3 = []
    for i in range(35):

        if i >=10:
            ds = 'DS_'+str(i)+'*.tif'
        else:
            ds = 'DS_0'+str(i)+'*.tif'
        v = getvals(i, fp, ds)
        c1.append(ds)
        c2.append(v[0])
        c3.append(v[1])
        
    df = pd.DataFrame({'id':c1, 'imsize':c2, 'masksize':c3})
        
    return df
    
def getvals(i, fp, ds):
    
    
    fp = os.path.join(fp, ds)
    if i == 34:
        imNumber = 1
    elif i == 33:
        imNumber = 11
    elif i == 24:
        imNumber = 2
    elif i == 22:
        imNumber = 3
    elif i == 32:
        imNumber = 13
        
    else: 
        imNumber = 0 
        
    m = getMask(fp, imNumber=imNumber)
    figure(m, fp)

    imsize = m.shape[0]*m.shape[0]
    masksize = np.sum(m)
    return imsize, masksize

def figure(m, fp):
    # im = io.imread(glob(fp)[0])
    plt.figure()
    plt.imshow(m)
    plt.title(fp)
    

#%%
df = createDict(fp)
#%%
# save this boi
df['id'] = df['id'].str[:5]

path = r"F:\GeomorphologyPaper\DataFolder\dictionaries\channelSizes.csv"
df.to_csv(path)
