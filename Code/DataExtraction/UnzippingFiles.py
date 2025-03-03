# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:25:34 2023
Script from RiverTwin useful functions altered to fit M river data. 
Readme that explains naming convention in:
    _missioncontrol folder/datamanagement file

@author: lgxsv2
"""


import os
import zipfile
import glob


#%%

def host_unzip(ds='DS_13', year='2023',zipfolder=r'D:\GeomorphologyPaper\DataFolder\Imagery\zips', 
              verbose=False, destination=r'D:\GeomorphologyPaper\DataFolder\Imagery\rawImages'):
    '''
    

    Parameters
    ----------
    ds : TYPE, str
        DESCRIPTION. The default is 'DS_13'.
    year : TYPE, str
        DESCRIPTION. The default is '2023'.
    zipfolder : path
        DESCRIPTION. The default is r'F:\GeomorphologyPaper\DataFolder\zips'.
    verbose : binary, 
        DESCRIPTION. The default is False.
    destination : path, optional
        DESCRIPTION. The default is r'F:\GeomorphologyPaper\DataFolder\rawImages'.

    Returns
    -------
    opens zip renames files and saves them in corrosponding folder,
    hide folders you do not want extracted.

    '''
    ziplist = findZips(ds, year, zipfolder, verbose)
    
    for i in ziplist:
        extraction(i, ds, year, destination, verbose)
        if verbose:
            print('zip file done: ', str(i))
    print('Complete')
            
            
            
#%%
def findZips(ds, year, zipfolder, verbose):
    # folder structure:
    # zipfolder-> year -> zip files (probably by month) that start with DS_XX
    # This lists them for later use
    search_path = os.path.join(zipfolder, str(year), f"{ds}*.zip")
    list_of_files = glob.glob(search_path)
    if verbose: 
        print(len(list_of_files))
    return list_of_files





        
#%%
def extraction(path, ds, year, destination, verbose):
    
        with zipfile.ZipFile(path, "r") as zf:
            # lists all tifs that aren't udm2 
            tifs = [file for file in zf.namelist() if file.lower().endswith("composite.tif")]
            
            for i in tifs:
                rename(i,ds,year, destination, zf)
                if verbose:
                    print(str(i) + ' done')
            
            
            
#%%

def rename(i,ds, year, destination, zf):
    fn = ds+'_'+i.split('_')[0].replace("-","")+'.tif'
    if i.split('_')[0][:4]!=year:
        fn = os.path.basename(zf.filename)[:14]+'.tif'
    path = os.path.join(destination, year)
    output = os.path.join(path, fn)
    # doesnt have year or ds
    with open(output, "wb") as otf:
        otf.write(zf.read(i))

#%%
# host_func(verbose=True)





