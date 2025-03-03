# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 09:28:57 2023

@author: lgxsv2
"""

import os

os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")

import F6Funcs
import module



def getImages(ds_ls=["DS_01", "DS_13", "DS_24", "DS_34"], dirs=r"D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023"):
    
    '''
     "DS_14" doesnt work
    '''
    
    
    for ds in ds_ls:
        
        #gets height of image
        im = module.getStackHeight(dirs, ds).astype(float)
        
        # saves the file temporarily
        fn_in = F6Funcs.temporarySave(im=im, dirs=dirs, ds=ds)
        
        # gets first image in June
        fn_raw = F6Funcs.getRawFile(dirs, ds)
        
        ## add location data and overwrites temporary file - only temporary because edited with QGIS
        im = module.tifProjection(fn_in, fn_raw=fn_raw, out=fn_in)



#%%
getImages()
    





