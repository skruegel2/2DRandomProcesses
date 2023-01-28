#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:54:16 2021

@author: Wenrui Li
"""

import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.
HALF_FILT = 1
FILT = 3
IMG_SIZE = 512
def BetterSpecAnal(x):
# Find center row
    num_rows = x.shape[0]
    num_cols = x.shape[1]
    center_row = int(num_rows/2)
    center_col = int(num_cols/2)
    psd = np.empty([64,64])
    psd_dft = np.empty([64,64])
    psd_dft_avg = np.zeros([64,64])
    #Hamming window does not need to be recalculated
    W = np.outer(np.hamming(64), np.hamming(64));
    # wind_row, wind_col are the window indices
    # cur_row, cur_col are the pixel indices
    for wind_row in range(-2,3):
        for wind_col in range(-2,3):
            for cur_row in range(64):
                for cur_col in range(64):
                    # Fill window with data
                    psd[cur_row][cur_col] = float(x[cur_row+wind_row*64+center_row][cur_col+wind_col*64+center_col])
                    # Multiply by Hamming window W
                    psd[cur_row][cur_col] = psd[cur_row][cur_col] * W[cur_row][cur_col];
            # Compute squared DFT magnitude
            psd_dft = (1/64**2)*np.abs(np.fft.fft2(psd))**2
            # Use fftshift to move the zero frequencies to the center of the plot.
            psd_dft = np.fft.fftshift(psd_dft)
            psd_dft_avg = psd_dft_avg + psd_dft
    psd_dft_avg = psd_dft_avg/25.0
    # Plot the result using a 3-D mesh plot and label the x and y axises properly. 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    a = b = np.linspace(-np.pi, np.pi, num = 64)
    X, Y = np.meshgrid(a, b)
    # Compute the logarithm of the Power Spectrum.
    Zabs = np.log(psd_dft_avg)

    surf = ax.plot_surface(X, Y, Zabs, cmap=plt.cm.coolwarm)

    ax.set_xlabel('$\mu$ axis')
    ax.set_ylabel('$\\nu$ axis')
    ax.set_zlabel('Z Label')

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    
def InitTestSrc(src, src_size):
    for cur_row in range(src_size):
        for cur_col in range(src_size):
            src[cur_row][cur_col] = 1
    
def InitTestFilt(filt):
    for cur_row in range(FILT):
        for cur_col in range(FILT):
            filt[cur_row][cur_col] = 1
            
def DisplaySrc(src, src_size):
    for cur_row in range(src_size):
        for cur_col in range(src_size):
            print('src:', cur_row, cur_col, src[cur_row][cur_col])
    
def InitFilt(filt):
    # Define filter manually since there are few elements
    filt[0][0] = -0.9801
    filt[0][1] = 0.99
    filt[0][2] = 0
    filt[1][0] = 0.99
    filt[1][1] = 3
    filt[1][2] = 0
    filt[2][0] = 0
    filt[2][1] = 0
    filt[2][2] = 0

def DisplayFilt(filt):
    for cur_row in range(FILT):
        for cur_col in range(FILT):
            print('filt:', cur_row, cur_col, filt[cur_row][cur_col])
            
def MultiplyOneFilterEl(src, src_size, src_cur_row, src_cur_col,
                        filt, filt_cur_row, filt_cur_col):
    # Check for out of bounds to left
    if (src_cur_col + filt_cur_col < 0):
        return 0;
    # Check for out of bounds to right
    elif (src_cur_col + filt_cur_col > (src_size - 1)):
        return 0;
    # Check for out of bounds on top
    elif (src_cur_row + filt_cur_row < 0):
        return 0;
    # Check for out of bounds on bottom
    elif (src_cur_row + filt_cur_row > (src_size - 1)):
        return 0;
    else:
        return src[src_cur_row + filt_cur_row][src_cur_col + filt_cur_col]*filt[filt_cur_row + HALF_FILT][filt_cur_col + HALF_FILT]
            
    
def TestMultiplyOneFilterEl():
    test_src = np.zeros([5,5])
    InitTestSrc(test_src, 5)
    #DisplaySrc(test_src, 5)
    filt = np.zeros([3,3])
    InitTestFilt(filt)
    #DisplayFilt(filt)
    for src_cur_row in range(5):
        for src_cur_col in range(5):
            for filt_cur_row in range(-1,2):
                for filt_cur_col in range(-1, 2):
                    ret_val = MultiplyOneFilterEl(test_src, 5, src_cur_row, src_cur_col,
                                        filt, filt_cur_row, filt_cur_col)
                    print('src row:',src_cur_row,'src col:', src_cur_col, 'filt row:', filt_cur_row,
                          'filt_col:', filt_cur_col, 'ret:',ret_val)
            
def MultiplyOnePixelEl(src, src_size, src_cur_row, src_cur_col, filt):
    # Init before accumulating
    ret_val = 0.0
    for filt_cur_row in range(-1,2):
        for filt_cur_col in range(-1, 2):
            ret_val = ret_val + MultiplyOneFilterEl(src, src_size, src_cur_row, src_cur_col, filt,
                                                filt_cur_row, filt_cur_col)
    return ret_val;

def FilterImage(src, src_size, filt, result):
    for cur_row in range(IMG_SIZE):
        for cur_col in range(IMG_SIZE):
            src[cur_row][cur_col] = MultiplyOnePixelEl(src, src_size, cur_row, cur_col, filt)

def AddOffset(src, src_size, offset):
    for src_row in range(src_size):
        for src_col in range(src_size):
            src[src_row][src_col] = src[src_row][src_col] + offset;

def Threshold(src, src_size, low_thresh, high_thresh):
    for src_row in range(src_size):
        for src_col in range(src_size):
            if src[src_row][src_col] > high_thresh:
                src[src_row][src_col] = high_thresh;
            elif src[src_row][src_col] < low_thresh:
                src[src_row][src_col] = low_thresh;
    
            
# Generate 512 x 512 image
x = np.random.uniform(-0.5, 0.5, [IMG_SIZE,IMG_SIZE])
# Read in a gray scale TIFF image.
#im = Image.open('img04g.tif')
print('x shape: ', x.shape)

# Display x_scaled
x_scaled = np.ubyte(255*(x+0.5))
img_out = Image.fromarray(x_scaled)
img_out.save('x_scaled.tif')                 
y = np.zeros([IMG_SIZE, IMG_SIZE])
# Define filter
filt = np.zeros([3,3])
InitFilt(filt)
#TestMultiplyOneFilterEl()
FilterImage(x, IMG_SIZE, filt, y)
AddOffset(x, IMG_SIZE, 127)
Threshold(x, IMG_SIZE, 0, 255);
img_y = Image.fromarray(x)
y_array = np.array(img_y)
plt.imshow(y_array, cmap=plt.cm.gray)
plt.show()
#img_y.save('y.tif');
# Import Image Data into Numpy array.
# The matrix x contains a 2-D array of 8-bit gray scale values. 
##x = np.array(im)
##print('Data type: ', x.dtype)
##
### Test BetterSpecAnal
##x = np.double(x)/255.0
##BetterSpecAnal(x)

