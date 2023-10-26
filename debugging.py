import os
import csv
import matplotlib.pyplot as plt  # plotting
import numpy as np  # numerics
from skimage import io
from natsort import natsorted
#import skimage.io
import skimage.color
import skimage.morphology
import skimage.measure as sm

from skimage.io import imread
from skimage.segmentation import clear_border
from skimage import measure
from skimage.measure import label,regionprops
from skimage import (io, filters,  morphology, measure, segmentation, feature, util, exposure)
from scipy.ndimage import gaussian_filter 
from scipy import ndimage as ndi
from scipy.ndimage import measurements, center_of_mass, binary_dilation, zoom

#define two folder paths - for September 2023 and October 2023 
folder_path_september = './HoloMonitor Beta TIFF/September 2023/MDCK Edna_06.09.23-B1-1_100ul'
folder_path_october = './HoloMonitor Beta TIFF/October 2023/MDCK 17.10.23/B2-1'

"""September data (images)"""
list_files_september = [os.path.join(folder_path_september, f) for f in os.listdir(folder_path_september)]
list_files_september = natsorted(list_files_september)
image_list_september = []

#open all images in the stack
for filename in list_files_september:
    image_list_september.append(io.imread(filename))

"""October data (images)"""
list_files_october = [os.path.join(folder_path_october, f) for f in os.listdir(folder_path_october)]
list_files_october = natsorted(list_files_october)
image_list_october = []

#open all images in the stack
for filename in list_files_october:
    image_list_october.append(io.imread(filename))

csv_file_path_september = 'September_2023_MDCK_Edna_06.09.23-B1-1_100ul_minmaxvalues_rawHM.csv'
csv_file_path_october = 'MDCK_17.10.23_B2-1_minmaxvalues_rawHM.csv' 

"""September data (optical thickness)"""
min_values_september = []
max_values_september = []

# Read the CSV file
with open(csv_file_path_september, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    
    # Skip the header row if it exists
    header = next(csv_reader, None)
    
    # Iterate through the rows and extract data
    for row in csv_reader:
        min_values_september.append(float(row[0]))
        max_values_september.append(float(row[1]))
        
min_values_september = np.array(min_values_september)
max_values_september = np.array(max_values_september)
min_values_september = min_values_september * 15.875
max_values_september = max_values_september * 15.875

"""October data (optical thickness)"""
min_values_october = []
max_values_october = []

# Read the CSV file
with open(csv_file_path_october, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    
    # Skip the header row if it exists
    header = next(csv_reader, None)
    
    # Iterate through the rows and extract data
    for row in csv_reader:
        min_values_october.append(float(row[0]))
        max_values_october.append(float(row[1]))
        
min_values_october = np.array(min_values_october)
max_values_october= np.array(max_values_october)
min_values_october = min_values_october * 15.875
max_values_october = max_values_october * 15.875

"""Scaling pixels into micrometers for September data - first image in the stack"""
delta_I = 65535
zeta_min_september = np.min(min_values_september)
delta_zeta_i_september = max_values_september - min_values_september

I_hat_0_september = ( (image_list_september[0]/delta_I) * delta_zeta_i_september[0] + zeta_min_september - min_values_september[0] ) #*1000 #scaled to nanometers for the first image in the stack

"""Scaling pixels into micrometers for October data - first image in the stack"""
delta_I = 65535
zeta_min_october = np.min(min_values_october)
delta_zeta_i_october = max_values_october - min_values_october

I_hat_0_october = ( (image_list_october[0]/delta_I) * delta_zeta_i_october[0] + zeta_min_october - min_values_october[0] ) #*1000 #scaled to nanometers for the first image in the stack
