
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:13:11 2019

@author: TOP
"""


import pandas as pd 
import skimage, os
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.measure import label,regionprops, perimeter
from skimage.morphology import binary_dilation, binary_opening
from skimage.filters import roberts, sobel
from skimage import measure, feature
from skimage.segmentation import clear_border
from skimage import data
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pydicom as dicom
import scipy.misc
import numpy as np


#Start : Reading CT
filename = 'F:/LIDC-IDRI/LIDC-IDRI/LIDC-IDRI-0020/01-01-2000-29935/3000525-47372/000069.dcm' 
lung = dicom.read_file(filename)
slice = lung.pixel_array
slice[slice == -2000] = 0
plt.imshow(slice, cmap=plt.cm.gray)

#Step 1: Convert into a binary image.
binary = slice < 604
plt.axis('off')
plt.imshow(binary, cmap=plt.cm.bone) 

#Step 2: Remove the blobs connected to the border of the image.
cleared = clear_border(binary)
plt.axis('off')
plt.imshow(cleared, cmap=plt.cm.bone) 

#Step 3: Label the image.
label_image = label(cleared)
plt.axis('off')
plt.imshow(label_image, cmap=plt.cm.bone)

#Step 4: Keep the labels with 2 largest areas
areas = [r.area for r in regionprops(label_image)]
areas.sort()
if len(areas) > 2:
    for region in regionprops(label_image):
        if region.area < areas[-2]:
            for coordinates in region.coords: 
                label_image[coordinates[0], coordinates[1]] = 0
binary = label_image > 0
plt.axis('off')
plt.imshow(binary, cmap=plt.cm.bone)

#Step 5: Erosion operation with a disk of radius 2. This operation is seperate the lung nodules attached to the blood vessels.
selem = disk(2)
binary = binary_erosion(binary, selem)
plt.axis('off')
plt.imshow(binary, cmap=plt.cm.bone) 

#Step 6: Closure operation with a disk of radius 10. This operation is to keep nodules attached to the lung wall.
selem = disk(10)
binary2 = binary_closing(binary, selem)
plt.axis('off')
plt.imshow(binary, cmap=plt.cm.bone)
edges = roberts(binary2)
binary3 = ndi.binary_fill_holes(edges)
plt.axis('off')
plt.imshow(binary3, cmap=plt.cm.bone)

#Step 7: Save Results
plt.imsave('output.tif',binary3, cmap=plt.cm.bone)




