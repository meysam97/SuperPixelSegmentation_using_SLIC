# -*- coding: utf-8 -*-
"""Project_02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E9zqYz_HZW0eRydE4aIDFzhRGrzdeuWV
"""

import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2lab, label2rgb
from skimage.segmentation import slic, mark_boundaries, slic_superpixels
from skimage import io

from skimage.measure import regionprops
from skimage.future.graph import rag_mean_color, show_rag, cut_threshold, merge_hierarchical

from skimage.filters import gaussian
from skimage import segmentation, color, filters
from skimage.future import graph
import utils

# load the image
im_number = 1
images = ['/SLIC_mex/0073MR0003970000103657E01_DRCL.jpg',
          '/SLIC_mex/0174ML0009370000105185E01_DRCL.jpg',
          '/SLIC_mex/0617ML0026350000301836E01_DRCL.jpg',
          '/SLIC_mex/1059ML0046560000306154E01_DRCL.jpg']
im_0 = plt.imread(images[im_number])
im_0 = im_0[:,:,0:3]
# im_0 = gaussian(im_0, sigma=2, multichannel=True)
print(type(im_0))
print(im_0.shape)
plt.figure(dpi=200)
plt.imshow(im_0)
plt.title('Original Image - picture ' + str(im_number))

## SLIC algorithm
compactness = 30
n_segments = 30
num_cuts = 30
h_thresh = 25
Ncuts_thresh = 0.0005
adabtive_SLIC = True # False: SLIC     True:active SLIC
SLIC_label = slic(im_0, compactness=compactness, n_segments=n_segments, multichannel=True, convert2lab=True, max_iter=50)
SLIC_label = SLIC_label + 1# So that no labelled region is 0 and ignored by regionprops
print(type(SLIC_label), SLIC_label.shape)
plt.figure(dpi=200)
plt.imshow(SLIC_label)
plt.title('SLIC label - picture ' + str(im_number) + '\n compactness: ' + str(compactness) + 
          '     number of segments: ' + str(n_segments))

## Adabtive SLIC (labels obtained from MATLAB file "SLICOdemo.m")
SLIC0_labels = ['/SLIC_mex/0073MR0003970000103657E01_DRCL.tif',
                '/SLIC_mex/0174ML0009370000105185E01_DRCL.tif',
                '/SLIC_mex/0617ML0026350000301836E01_DRCL.tif',
                '/SLIC_mex/1059ML0046560000306154E01_DRCL.tif']
SLIC0_label = plt.imread(SLIC0_labels[im_number])
SLIC0_label = SLIC0_label + 1
plt.figure(dpi=200)
plt.imshow(SLIC0_label)
plt.title('Adabtive SLIC label - picture ' + str(im_number) + '\n number of segments: ' + str(n_segments))

if adabtive_SLIC:
  label = SLIC0_label
  compactness = 'Adabtive'
else:
  label = SLIC_label

utils.display_inital_segmentaion(adabtive_SLIC, label, im_0, im_number, n_segments, compactness)
utils.display_inital_RAG(adabtive_SLIC, label, im_0, im_number, n_segments, compactness)
utils.Hierarchical_merging(adabtive_SLIC, label, im_0, im_number, h_thresh, n_segments, compactness)
Ncuts_label = utils.Ncuts_merging(adabtive_SLIC, label, im_0, im_number, Ncuts_thresh, n_segments, num_cuts, compactness)

print(type(Ncuts_label), Ncuts_label.shape, Ncuts_label.max())
print(Ncuts_label)
Ncuts_label2 =  np.interp(Ncuts_label, (Ncuts_label.min(), Ncuts_label.max()), (0, 255))
print(np.sort(Ncuts_label, axis=None))
a = np.where(Ncuts_label==1)
a = np.array(a)
Ncuts_label
print(a.shape)

b = np.array([1,2,5,0])
b = np.where(Ncuts_label==490, Ncuts_label, 0)
b = np.repeat(b, 3, axis=2)

print(b.shape, np.unique(Ncuts_label))
plt.figure()
plt.imshow(b)

plt.figure()
plt.imshow(im_0)
