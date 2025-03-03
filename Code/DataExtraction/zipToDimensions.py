# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:16:55 2023

This script was written to take data from the start to the finish ready for csv level analysis

@author: lgxsv2
"""
###############################################################################
# Important VARS ***
# ds = 'DS_01'
import gc
gc.collect()
year = '2020'
import os


for y in ['2023']:
    year = y
    for i in [1,34]:
        if i >=10:
            ds = 'DS_'+str(i)
        else:
            ds = 'DS_0'+str(i)
    
        # os.chdir(r'D:\GeomorphologyPaper\Analysis\DataExtraction')
        # from UnzippingFiles import host_unzip
    
        # host_unzip(ds=ds, year=year, verbose=True)
    
    
        os.chdir(r'D:\GeomorphologyPaper\Analysis\DataExtraction\StepOneRiverTwin')
        from WaterMasking import extractWaterMask
    
        extractWaterMask(ds=ds, year=year, verbose=True)
    
    #%%
    # os.chdir(r'F:\GeomorphologyPaper\Analysis\pluto')

    # from Fyearlyislandstats import yearlyisland_statistics

    # yearlyisland_statistics(ds=ds,year=year, verbose=True)    
#%%
###############################################################################


#restarting 5 because it's taking too long..
# import gc
# gc.collect()
# ds = 'DS_05'
# os.chdir(r'F:\GeomorphologyPaper\Analysis\StepOneRiverTwin')
# from WaterMasking import extractWaterMask

# extractWaterMask(ds=ds, year=year)









 # probably need os.chdir(r'F:\GeomorphologyPaper\Analysis\StepOneRiverTwin')
#  os.chdir(r'F:\GeomorphologyPaper\Analysis\DataExtraction')
# from UnzippingFiles import host_unzip

# host_unzip(ds=ds, year=year, verbose=True)

# #%%
# os.chdir(r'F:\GeomorphologyPaper\Analysis\StepOneRiverTwin')
# from WaterMasking import extractWaterMask

# extractWaterMask(ds=ds, year=year)

# #%%
# os.chdir(r'F:\GeomorphologyPaper\Analysis\pluto')

# from Fyearlyislandstats import yearlyisland_statistics

# yearlyisland_statistics(ds=ds,year=year, verbose=True)