# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:30:18 2024

@author: lgxsv2
"""

from skimage import io as IO
import os
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
from F_impacts import calculateCenterline
import F_impacts
import module
m20 = r"D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023"
CL = r"D:\GeomorphologyPaper\Analysis\Figures\2024_03_01\F4-impacts\locatedImages\CL"
raw = r"D:\GeomorphologyPaper\DataFolder\Imagery\rawImages\2023\done"


im_ls = ['DS_18_20230702', 'DS_18_20230830', 'DS_18_20231029']
#%%
for i in im_ls:
    # get mask
    im_fn = os.path.join(m20, (i+'.tif'))
    im = IO.imread(im_fn)
    
    ex = calculateCenterline(im)
    # F_impacts.testPlotFunc(ex[0])
    # print max width - scale we think already taken into account
    print(i, ': ', ex[1].max())
    
    # save centerline
    fn = os.path.join(CL, ('CL_lost_'+i+'.tif'))
    IO.imsave(fn, ex[0])
    
    # save distance map
    fn = os.path.join(CL, ('dist_lost_'+i+'.tif'))
    IO.imsave(fn, ex[1])
#%%

for i in im_ls:
    # get CL stats and re save without lost
    fn_in = os.path.join(CL, ('CL_lost_'+i+'.tif'))
    fn_raw = os.path.join(raw, (i+'.tif'))
    out = os.path.join(CL, ('CL_'+i+'.tif'))
    
    module.tifProjection(fn_in, fn_raw, out)
    
    # get dist stats and re save without lost
    fn_in = os.path.join(CL, ('dist_lost_'+i+'.tif'))
    fn_raw = os.path.join(raw, (i+'.tif'))
    out = os.path.join(CL, ('dist_'+i+'.tif'))
    
    module.tifProjection(fn_in, fn_raw, out)

    
    