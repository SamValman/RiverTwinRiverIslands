# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:03:00 2023

@author: lgxsv2
"""


from skimage import io
import os
import pandas as pd
from scipy import ndimage
import numpy as np
import matplotlib as mpl
import glob
from mask_image import maskImage, getMask
# fn = r"F:\GeomorphologyPaper\DataFolder\m20Masks\2023\DS_13_20230701.tif"

#%%
def yearlyisland_statistics(dirs=r'D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks',ds='DS_13',year='2023', verbose=True): 
    # not done but will be main wrapper
    ls = []
    search_path = os.path.join(dirs, str(year), f"{ds}*.tif")
    ###############
    # For DS_21 and DS_22
    # just july to aug 
    # for i in search_path:
    #     do soemthing return better search path 
    
    
    
    ###############
    
    if ds == 'DS_34':
        imNumber = 1
    elif ds == 'DS_33':
        imNumber = 11
    elif ds == 'DS_24':
        imNumber = 2    
    elif ds == 'DS_21':
         imNumber = 2
    elif ds == 'DS_22':
        imNumber = 1
    elif ds == 'DS_32':
        imNumber = 13
    elif ds == 'DS_01':
        imNumber = 2
    else: 
        imNumber = 0 
    mask = getMask(search_path, imNumber)
   
    
   
    # go through every image in path
    for i in glob.glob(search_path):
        r = individualImage(i, mask, verbose)
        r.append(os.path.split(i)[1][6:-4])

        ls.append(r)
        if verbose:
            print(os.path.split(i)[-1])
    
    # make df, name cols, set index
    results = pd.DataFrame(ls)
    results.columns = ['i1', 'i2', 'i3', 'i4', 'itotal','largetotal', 'area', 'length', 'width', 'circumference', 'date']
    results = results.set_index('date')
    
    save_results(results, dirs, ds, year)
    
    return results

#%%
def individualImage(fn, mask, verbose):
    
    im = io.imread(fn)
    
    island_number = get_island_number(fn)
    
    ranked, sorted_values = group(im, verbose)
    if len(sorted_values) <=3:
        results = ['na']*9
        print('failure')
        #potential solution with new bank mask from good image. 
    else: 
        results = measure_islands(im,ranked, sorted_values, island_number,mask, minIslandSize=6000)
    
    
    return results 
    
    
    
#%%
def get_island_number(fn):
    # returns expected island number not actual number of islands. 
    ds = os.path.split(fn)[-1][2:5]
    # replace fn with the path
    path, x = os.path.split(fn)
    path, x = os.path.split(path)
    path, x = os.path.split(path)
    path, x = os.path.split(path)
    island_path = os.path.join(os.path.join(path,'Products', 'dictionaries'), 'island_numbers.csv')

    
    island = pd.read_csv(island_path)
    island= island.set_index('id')['island_number'].to_dict()
    #make dictionary
    island_number = island['ds'+ds]
    
    return island_number
#%%
def group(im, verbose):
    # image needs to be inverted
    im2 = 1-im
    
    s = [[1,1,1],[1,1,1],[1,1,1]] # so can be diagonally connected 
    label, nfeatures = ndimage.label(im2, structure=s)
   
    # size of each label
    sizes = np.bincount(label.ravel())

    # Create a dictionary to map label IDs to their corresponding sizes
    label_sizes = {i: size for i, size in enumerate(sizes)}
    
    # Sort the labels by their sizes in descending order
    sorted_labels = sorted(label_sizes.keys(), key=lambda k: label_sizes[k], reverse=True)
    sorted_dict = dict(sorted(label_sizes.items(), key=lambda item: item[1], reverse=True))
    sorted_vals = list(sorted_dict.values())
   
    # can add a verbose if wanted: 
    # for label_id, size in label_sizes.items():
    #     print(f"Label {label_id}: Size = {size}")
   
    # Create a new  image where labels are ordered by size
    ranked = np.zeros_like(label)
    
    for new_label, old_label in enumerate(sorted_labels, start=1):
        ranked[label == old_label] = new_label
        
    # # add a print option::::
    # if verbose:
    #     mpl.pyplot.figure()

    #     mpl.pyplot.imshow(ranked)
    
    return ranked, sorted_vals
#%%

def measure_islands(im, ranked_im, sorted_values, island_number,mask, minIslandSize):
    area_results = island_area(ranked_im,sorted_values, island_number, minIslandSize)
    dimensional_results = island_dimensions(ranked_im,sorted_values, island_number)
    percent = pure_percentage(im, mask)
    
    results = area_results+percent+dimensional_results

    return results
#%%

def island_area(ranked_im,sorted_values, island_number, minIslandSize=6000):
    # If we work off island number what do we get.
    
    isize = []
    for i in range(island_number):
        isize.append(sorted_values[i+2])
    for i in range(4-island_number):
        isize.append(0)
 
    isize.append(sum(isize))
    
    sorted_values = sorted_values[2:]
    isize.append(sum(value for value in sorted_values if value > minIslandSize))
    

    return isize

def pure_percentage(im, mask):
    # results is list
    try:
        masked = maskImage(im, mask)
    # percent = (np.sum(masked)/(im.shape[0]*im.shape[1]))*100
        percent = np.sum(masked)
    except ValueError:
        percent = 'na'
    #im is im
    return [percent]
    
def island_dimensions(ranked_im,sorted_values, island_number):



    # coordinates of the largest island boundary
    boundary = np.argwhere(ranked_im == 3)

    # Step 2: Calculate the circumference
    circumference = len(boundary)

    # Step 3: Calculate the major and minor axes
    # You can calculate the distances from the center of the circle to the boundary points
    # and determine the major and minor axes based on those distances.

    # Calculate the center of the circle
    center_x = int(np.mean(boundary[:, 1]))
    center_y = int(np.mean(boundary[:, 0]))

# Calculate the distances from the center to boundary points
    distances = np.linalg.norm(boundary - [center_y, center_x], axis=1)

# Determine the major and minor axes based on the distances
    major_axis = 2 * np.max(distances)
    minor_axis = 2 * np.min(distances)

    return [major_axis, minor_axis, circumference]

#%%

def save_results(df, fn, ds, year):
    # NOTE CHANGE IN DIR
    dirs = os.path.join(os.path.split(os.path.split(fn)[0])[0], 'Products\dimensions_drySeason')
    print('test')
    # dirs = r'D:\GeomorphologyPaper\DataFolder\Products\dimensions_fullYear\temp'
    path = os.path.join(dirs,  f"{ds}_"+str(year)+'.csv')
    
    df.to_csv(path)
    
#%%


for year in ['2023']: #, '2021', '2020', '2019', '2018', '2017', '2016']:
    for ds in ['DS_22']:
        r = yearlyisland_statistics(ds=ds, year=year, verbose=True)

# # for i in range(6,13):
# #     if i >=10:
# #         ds = 'DS_'+str(i)
# #     else:
# #         ds = 'DS_0'+str(i)
# #     print('Starting a new island here****************************************')
# #     r = yearlyisland_statistics(ds=ds, verbose=True)

# #%%
# for i in range(21,35):
#     ds = 'DS_'+str(i)
#     print('Starting a new island here****************************************')
#     r = yearlyisland_statistics(ds=ds, verbose=True)
