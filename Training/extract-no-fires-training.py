import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
from scipy import sparse
import random
import os
from sys import getsizeof

coords = {
    "limits_4326": {
        "xmin":-80.4,
        "xmax": -60.6,
        "ymin": 44.6,
        "ymax": 52.6
    },
}

target_limit =  "limits_4326" #"limits_testing_9_chunks"
xmin, xmax, ymin, ymax = (coords[target_limit]["xmin"]), (coords[target_limit]["xmax"]), (coords[target_limit]["ymin"]), (coords[target_limit]["ymax"])

def pointInRect(point,rect):
    x1, y1, x2, y2 = rect
    # x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

'''
where new_image is a figure.canvas.buffer_rgba() turned into a np matrix: 

nonzero_rows, nonzero_cols = np.nonzero(new_image) # Get all nonzero rows & collumns 

min_row, max_row = np.min(nonzero_rows), np.max(nonzero_rows)
min_col, max_col = np.min(nonzero_cols), np.max(nonzero_cols)
# After a series of test, (0, 575, 3, 764) was the exact fit of the canvas when the ration between width:height = 2:1

'''

min_row, max_row, min_col, max_col = 0, 575, 3, 764 
xyratio = 2/1

resx = 0.2
resy = resx/xyratio
n_chunkx = int(round((xmax-xmin)/resx, 1)) # MAKE SURE YOU CAN MATH: because we convert to int if you get 0.1232131 sketch 
n_chunky = int(round((ymax-ymin)/resy, 1)) # We're using round to not get like 2.9999999999999999997 make sure to get 0.3

# For Final Extraction: 
# x: 19.8/99 = 0.2 per chunk for 99 chunks
# y: 8/80 = 0.1 per chunk for 80 chunks

# For this file more specifically, we want to process an area around the point. Let us use the size of a chunk: 0.2 for x and 0.1 for y
mat_l, mat_w = 0.1, 0.2

gdf = gpd.read_file("Feux_pt_ori_SHP/FEUX_PT_ORI_1972_2022.shp") # Path to the shapefile 
gdf = gdf.to_crs(4326)

count = 0

random.seed(11) # MAKE SURE WE GET THE SAME BOUNDS EVERY TIME :))
trainingInputCoords = []

for i in range(42000): # About the same number of entries as Humaine and Foudre combined

    movingOn = False
    
    while(not movingOn):
        rand = random.random() 

        rxcoord, rycoord = (random.random()*(xmax-xmin)+xmin), (random.random()*(ymax-ymin)+ymin) # Generate two points between the bounds

        min_x, min_y = round(rxcoord-int(rand*mat_l), 3), round(rycoord-int(rand*mat_l), 3)
        max_x, max_y = min_x+mat_l, min_y+mat_l


        # Shift the square if it is out of boundsss 
        if (min_x < xmin):
            min_x = xmin
            max_x = xmin+mat_l
        if (min_y < ymin):
            min_y = ymin
            max_y = ymin+mat_l
        if (max_x > xmax):
            max_x = xmax
            min_x = xmax-mat_l
        if (max_y >= ymax):
            max_y = ymax-1
            min_y = ymax-mat_l
        
        for point in gdf.iterrows():
            checkx, checky = point[1]["geometry"].bounds[0], point[1]["geometry"].bounds[1]
            if not pointInRect((checkx, checky), (min_x, max_x, min_y, max_y)):
                movingOn = True
            
    trainingInputCoords.append((min_x, max_x, min_y, max_y))

    print(min_x, max_x, min_y, max_y)

    count+=1

np.save('data/Sans-Feu', trainingInputCoords)
del trainingInputCoords

os.system("sudo poweroff")