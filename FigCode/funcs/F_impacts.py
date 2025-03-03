# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 16:12:13 2024

@author: lgxsv2
"""


from scipy import ndimage
import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.ndimage import convolve
import cv2 
import matplotlib.pyplot as plt 



def testPlotFunc(im):
    plt.figure()
    plt.imshow(im)
    plt.show()

###############################################################################
# Island size functions
###############################################################################

def group(im, verbose=False):
    # working on water so doesnt need to be inverted
    im2 = im#1-im
    
    s = [[1,1,1],[1,1,1],[1,1,1]] # so can be diagonally connected 
    labelim, nfeatures = ndimage.label(im2, structure=s)
    return labelim, nfeatures


###############################################################################
# centerline
###############################################################################

# this requires the following functions beneath it 
def calculateCenterline(im):
    # uses riv cloud width method to calculate centreline based on a gradient map
    dist = CalcDistanceMap(im)
    grad = CalcGradientMap(dist, 2)
    cl = CalcOnePixelWidthCenterline(im, grad, 0.9)
    # cl1Cleaned1 = CleanCenterline(cl1, 300, True)
    # cl1px = CleanCenterline(cl1Cleaned1, 300, False)
    return cl, dist



###################### Internal functions of above
def CalcDistanceMap(im, neighborhoodSize=1000, scale=3):
    binary_im = np.where(im > 0, 1, 0)

    # Calculate the Euclidean distance transform
    dpixel = distance_transform_edt(binary_im)

    # Convert distance to meters based on the given scale
    dmeters = dpixel * scale

    # # Apply a mask to keep distances only for river pixels within the specified neighborhood size
    # mask = (dpixel <= neighborhoodSize) & (im > 0)
    # DM = np.where(mask, dmeters, 0)

    return dmeters #DM


def CalcGradientMap(im, scale=3):

    # Define convolution kernels for x and y gradients
    k_dx = np.array([[-0.5, 0.0, 0.5]])
    k_dy = np.array([[0.5], [0.0], [-0.5]])

    # Convolve the image with the x and y kernels
    dx = convolve(im, k_dx)
    dy = convolve(im, k_dy)

    # Calculate the gradient magnitude
    g = np.sqrt(dx**2 + dy**2) / scale

    return g
def CalcOnePixelWidthCenterline(im, GM, hGrad):
    # Fast distance transform of the river banks
    img_d2 = cv2.dilate(im, None, iterations=2)

    # Mask areas where gradient is less than or equal to the threshold hGrad
    cl = np.logical_and(GM <= hGrad, img_d2 > 0)

    # Apply skeletonization twice to get a 1px centerline
    cl1px = skeletonize(cl, 2, 1)

    return cl1px

def skeletonize(image, num_iterations, kernel_size):
    # Apply skeletonization num_iterations times
    for _ in range(num_iterations):
        # Use a kernel for erosion
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))
        image = cv2.erode(image.astype(np.uint8), kernel)

    return image.astype(bool)