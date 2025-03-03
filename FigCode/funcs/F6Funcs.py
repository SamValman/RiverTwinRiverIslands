# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:15:40 2023
EFFECTIVELY THE F6 Module
@author: lgxsv2
"""
import pathlib
import os 
import skimage.io as IO
import glob



def temporarySave(im, dirs='', ds='DS_01'):
    '''
    
    Issues may arise if figure names are not changed carefully 
    Parameters
    ----------
    im : array 1 band
        DESCRIPTION. The default is im.
    ouput : path - just needed for drive
        DESCRIPTION. The default is ''.
    ds: str
        DESCRIPTION: ds string

    Returns
    -------
    Saves image in F6 temporary file.

    '''
    # get driver
    drive = pathlib.Path(dirs).drive
    # find temporary file for this Figure then add the DS.tif 
    op = os.path.join(os.path.join(drive,'\GeomorphologyPaper\DataFolder\Products\TemporaryFolderByFigure\F6' ), (ds+'.tif'))
    
    # save the image given 
    IO.imsave(op, im)
    return op


#%%

def getRawFile(dirs, ds):
    '''
    Gets the first June raw image for the ds

    Parameters
    ----------
    dirs : path
        Just for driver.
    ds : str
        DS_00 to DS_34.

    Returns
    -------
    str
        location of first image.

    '''
    # get driver
    drive = pathlib.Path(dirs).drive
    
    # get to raw image location
    path = os.path.join(drive, r'\GeomorphologyPaper\DataFolder\Imagery\rawImages\2023\done')
    # add ds and find all. 
    path = os.path.join(path, (ds+'*.tif'))
    
    #get name sorted directory list
    ls = sorted(glob.glob(path))
    
    #returns first in June which should be first named in this section
    return ls[0]

