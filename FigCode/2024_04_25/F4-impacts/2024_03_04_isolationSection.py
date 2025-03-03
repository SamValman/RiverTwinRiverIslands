# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:57:38 2024

@author: lgxsv2
"""
import skimage.io as io
import os 
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np 
import skimage.morphology as M
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
import module
import F_impacts
#%%
ds = 'DS_03'
file_names = ['20230701', '20230720', '20230824', '20230923']
of = r'D:\GeomorphologyPaper\Analysis\Figures\2024_03_01\F4-impacts\locatedImages'
#%%

# for i in file_names:
#     im = (ds+'_'+i+'.tif')
#     fn_in = os.path.join(r'D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023', im)
#     fn_raw = os.path.join(r'D:\GeomorphologyPaper\DataFolder\Imagery\rawImages\2023\done', im)
#     out = os.path.join(of, im)


#     module.tifProjection(fn_in, fn_raw, out)


#%% get the two levels we needed 

plt.close('all')
tick = 1


# Just the images with isolated islands
for i in file_names[2:]:
    im = (ds+'_'+i+'.tif')
    fn_in = os.path.join(r'D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023', im)
    # read im
    im = io.imread(fn_in)
    
    # use Ndim for pixel connectivity analysis!!!
    newShape, groupSizes = F_impacts.group(im)
    
    
    
    ###########################################################################
    # Plot to have a look 
    ###########################################################################
    # Create a custom colormap
    length = groupSizes#len(groupSizes)
    colors = np.random.rand(length, 3)
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors, N=length)

    plt.figure()
    plt.imshow(newShape, cmap=cmap)
    plt.title(i)
    plt.show()
    # for visualisation only
    NS = newShape
    for i in (range(6)):
        NS = M.dilation(NS)
    plt.figure()
    plt.imshow(NS, cmap=cmap)
    plt.title('dilation')
    plt.show()
    
    ###########################################################################
    # Print sizes
    ###########################################################################
    
    if tick == 1:
        island = newShape[newShape==40]
        print('size for 08: ', (len(island)*3))
    else:
        island = newShape[newShape==67]
        island1 = newShape[newShape==34]
        print('size for 09 small: ', (len(island)*3))
        print('size for 09 large: ', (len(island1)*3))

    

    
    
    
    
    ###########################################################################
    # Save image to be located in next section
    ###########################################################################
    
    #save to have a look properly
    out = os.path.join(of, ('Lincreased_'+str(tick)+'.tif'))
    tick+=1
    # io.imsave(out, newShape)
    # io.imsave(out, NS)

    
#%% Locate these images
# file_names=file_names[2:]

# for f, i in zip([1,2], file_names):
#     im = (ds+'_'+i+'.tif')
#     fn_in = os.path.join(of, ('L_'+str(f)+'.tif'))
#     fn_raw = os.path.join(r'D:\GeomorphologyPaper\DataFolder\Imagery\rawImages\2023\done', im)
#     im = 'islands_'+im
#     out = os.path.join(of, im)
    
    
#     module.tifProjection(fn_in, fn_raw, out)

    




fn_in = os.path.join(of, ('Lincreased_'+'2'+'.tif'))
im = (ds+'_20230923.tif')
fn_raw = os.path.join(r'D:\GeomorphologyPaper\DataFolder\Imagery\rawImages\2023\done', im)

im = 'VisualIslands_'+im
out = os.path.join(of, im)
module.tifProjection(fn_in, fn_raw, out)



















    