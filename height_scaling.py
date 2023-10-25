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

#define data paths, again have one for september and one for october
folder_path = './HoloMonitor Beta TIFF/September 2023/MDCK Edna_06.09.23-B1-1_100ul'
# folder_path = './HoloMonitor Beta TIFF/October 2023/MDCK 17.10.23/B2-1'

list_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
list_files = natsorted(list_files)
image_list_B2_1 = []

#open all images in the stack
for filename in list_files:
    image_list_B2_1.append(io.imread(filename))
    
# Define the file path of the raw, float min and max values that we obtained using reading_metadata.py
#again, one for september and one for october
csv_file_path = 'September_2023_MDCK_Edna_06.09.23-B1-1_100ul_minmaxvalues_rawHM.csv'
# csv_file_path = 'MDCK_17.10.23_B2-1_minmaxvalues_rawHM.csv' 

# Initialize empty lists to store the data from the CSV file
min_values = []
max_values = []

# Read the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    
    # Skip the header row if it exists
    header = next(csv_reader, None)
    
    # Iterate through the rows and extract data
    for row in csv_reader:
        min_values.append(float(row[0]))
        max_values.append(float(row[1]))

# Convert the lists to NumPy arrays to make life easier and ensure that everything is floats
min_values_array = np.array(min_values, dtype=float)
max_values_array = np.array(max_values, dtype=float)

#multiply all values by HoloMonitor factor: 15.875
min_values_array = min_values_array*15.875
max_values_array = max_values_array*15.875

zeta_min = np.min(min_values_array)
delta_zeta_i = max_values_array - min_values_array #should this be absolute value?
delta_I = 65535

#for one image
I_hat_0 = ( (image_list_B2_1[0]/delta_I) * delta_zeta_i[0] + zeta_min - min_values_array[0] ) #*1000 #scaled to nanometers for the first image in the stack
# print("Scaled optical height for the first image in the stack: ", I_hat_0)


#for all images in the stack

I_hat_all = [] #scaled optical heights in nanometers for all images in the stack
for i in range(len(image_list_B2_1)):
    I_hat_all.append(( (image_list_B2_1[i]/delta_I) * delta_zeta_i[i] + zeta_min - min_values_array[i] ) * 1000)


print("Scaled optical heights for all images in the stack: ", I_hat_all)
