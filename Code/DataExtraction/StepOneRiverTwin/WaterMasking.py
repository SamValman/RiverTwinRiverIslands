# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:23:44 2023


This file uses the water mask developed in the RSE paper:
    it does this to create water masks of the PS images on the M river.
@author: lgxsv2
"""
# use env x for this 
import tensorflow as tf
import os
import glob
import pandas as pd
from skimage import io
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

os.chdir(r'D:\GeomorphologyPaper\Analysis\DataExtraction\StepOneRiverTwin')
from RiverTwinWaterMask import RiverTwinWaterMask

#%%
def save(P3,outfp):
    # change path to output model folder

    io.imsave(outfp, P3[2], check_contrast=False)

# %%
def extractWaterMask(ds='DS_13', year='2023', path=r"D:\GeomorphologyPaper\DataFolder\Imagery\rawImages", model=r"D:\BackUp_RM\Code\RiverTwin\ZZ_Models\M20\model", verbose=False ):
    fp = os.path.join(os.path.join(path, year), (ds+'*.tif'))
    for i in glob.glob(fp):
        newpath = os.path.join(os.path.dirname(path), 'm20Masks')
        outfp = os.path.join(os.path.join(newpath, year), os.path.basename(i))
        if os.path.exists(outfp):
            continue
        else:
            if verbose:
                print(str(i))
            P3 = RiverTwinWaterMask(image_fp=i, tileSize=20, model=model, output='')
            save(P3,outfp)


#%%
# extractWaterMask(ds='DS_13', year='2023')


