# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:50:14 2024

@author: lgxsv2
"""

import module
import F1Funcs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import os
import pandas as pd
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
from skimage import io 
import glob
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import cv2


# %%

# get percentage of actual channel that is land
# y = (y/int(num.iloc[0]))*100
def remove_specal(im, kernel_size=3):
    '''
    uses morphological operators from image processing
    Parameters
    ----------
    im : array
    kernel_size : int, optional
        kernal for operator. The default is 3.

    Returns
    -------
    output : TYPE
        DESCRIPTION.

    '''
    #reverse image because dilation works on one class primarily 
    # our method seems to bleed land into water therefore this is the way we want it 
    im_reversed = 1-im 
    
    # needs to be this format for cv2
    input_im = im_reversed.astype('uint8')
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # dilution = cv2.dilate(input_im, kernel)
    output = cv2.morphologyEx(input_im,cv2.MORPH_OPEN, kernel)
    
    return output



def getMask(fp, imNumber=0):
    
    im = glob.glob(fp)[imNumber]
    im = io.imread(im)
    
    im2 = 1-im
    
    s = [[1,1,1],[1,1,1],[1,1,1]] # so can be diagonally connected 
    label, nfeatures = ndimage.label(im2, structure=s)
    
    sizes = np.bincount(label.ravel())

    # Create a dictionary to map label IDs to their corresponding sizes
    label_sizes = {i: size for i, size in enumerate(sizes)}
    sorted_labels = sorted(label_sizes.keys(), key=lambda k: label_sizes[k], reverse=True)
    # sorted_dict = dict(sorted(label_sizes.items(), key=lambda item: item[1], reverse=True))
    # sorted_vals = list(sorted_dict.values())
   
    # Create a new  image where labels are ordered by size
    ranked = np.zeros_like(label)
    for new_label, old_label in enumerate(sorted_labels, start=1):
        ranked[label == old_label] = new_label
    ranked[ranked!=1]=0
    
    mask = remove_specal(ranked, kernel_size=18)
    
    return mask

#%%
ds = "DS_03*.tif"
fp = r'D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023'
plt.close('all')

fp = os.path.join(fp, ds)
# <22 im number is 0

mask = getMask(fp, 0)

def figure(m, fp):
    # im = io.imread(glob(fp)[0])
    plt.figure()
    plt.imshow(m)
    plt.title(fp)
    
figure(mask, fp)

def normIm(fp, imNumber=0):
    im = glob.glob(fp)[imNumber]
    im = io.imread(im)
    plt.figure()
    plt.title('unmasked water mask')
    plt.imshow(im)
    plt.show()
    return im 
    
im = normIm(fp, 0)
    
#%%
fp_mask = r"D:\GeomorphologyPaper\Analysis\Figures\2024_01_03\FTemp-flowDiagram\parts\mask.tif"
io.imsave(fp_mask, mask)   
fp_im = r"D:\GeomorphologyPaper\Analysis\Figures\2024_01_03\FTemp-flowDiagram\parts\im.tif"
io.imsave(fp_im, im)      