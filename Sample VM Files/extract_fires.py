import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
from scipy import sparse
from shapely.geometry import Point, Polygon, LineString
import pandas as pd
import os 

# Basically converting the 'extract SHP'.ipynb into a py file to run on Virtual Instances on the cloud

coords = {"limits": {
        "xmin":-8953229.45098,
        "xmax":-6750696.01502,
        "ymin":5559313.031810002,
        "ymax":6900707.257190002
    }}

mpl.rcParams['figure.dpi'] = 120
# mpl.rcParams['savefig.pad_inches'] = 0


# This code is processed 
# I have manually processed every file using this format

gdf = gpd.read_file("FEUX_PROV.gpkg")

gdf2 = gdf.fillna('0')
gdf2 = gdf2[gdf2.an_origine.astype(int) >= 2013]
gdf2 = gdf2.to_crs(3857)
bnds = gdf2["geometry"].bounds

xmin, xmax, ymin, ymax = int(coords["limits"]["xmin"]), int(coords["limits"]["xmax"]), int(coords["limits"]["ymin"]), int(coords["limits"]["ymax"])
x_total = 59700
y_total = 36400
x_ratio = x_total/(xmax-xmin)
y_ratio = y_total/(ymax-ymin)
chunk_x = (xmax-xmin)/100
chunk_y = (ymax-ymin)/100

fires = []

for idx, cur_row in gdf2.iterrows():
    # print("hi")
    # print(idx)

    if (idx < 70544):
        continue

    y_factor = 10

    x_min, x_max, y_min, y_max = int(bnds["minx"][idx]), int(bnds["maxx"][idx]), int(bnds["miny"][idx]), int(bnds["maxy"][idx])
    # These coords only have 5 digits vs 7 for x and 6 digits vs 7 for y... or not let's manually fix this 
    
    
    # print(x_min, x_max, y_min, y_max)
    # # print(left_x_min, left_x_max,  top_y_min, top_y_max)
    # print(xmin, xmax, ymin, ymax)

    # if (count > 20):
    #     break
    # count+=1

    if (x_min < xmin or x_max > xmax or y_min < ymin or y_max > ymax):
        # print("out of bounds")
        continue 

    fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
    gpd.GeoSeries(cur_row['geometry']).plot(ax=ax, color="white")
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0, 0))
    # Plot the fire into a sparse matrix 
    sparse_mat = sparse.csr_matrix((y_total, x_total)).tolil()
    # print(sparse_mat.shape)

    # We first render the required chunks

    left_x_min = xmin + (x_min-xmin) - ((x_min-xmin) % chunk_x)
    left_x_max = xmin + (x_max-xmin) - ((x_max-xmin) % chunk_x)
    top_y_min = ymin + (y_min-ymin) - ((y_min-ymin) % chunk_y)
    top_y_max = ymin + (y_max-ymin) - ((y_max-ymin) % chunk_y)

    # left_x_min /= 100
    # left_x_max /= 100
    # top_y_min /= y_factor
    # top_y_max /= y_factor

    # print((x_min-xmin))
    # print(chunk_x)
    # print((x_min-xmin) % chunk_x)
    # print(left_x_min, left_x_max,  top_y_min, top_y_max)

    for x in range(int((left_x_max - left_x_min)/chunk_x)+1):
        for y in range(int((top_y_min - top_y_max)/chunk_y)+1):
            ax.axis([
                left_x_min+x*chunk_x, 
                left_x_min+(x+1)*chunk_x, 
                top_y_min+y*chunk_y,
                top_y_min+(y+1)*chunk_y,
            ])

            fig.canvas.draw()

            X = np.array(fig.canvas.renderer.buffer_rgba())
            # X_final = np.zeros((len(X), len(X[0])))

            for row in range(108, 472):
                for col in range(95, 692):
                    # print(left_x_min+(x*chunk_x)*100)

                    # print(int(((top_y_min+(y*chunk_y))*10-ymin)*y_ratio)+col-108,int(((left_x_min+(x*chunk_x))*100-xmin)*x_ratio)+row-95)
                    sparse_mat[int(((top_y_min+(y*chunk_y))-ymin)*y_ratio)+row-108,int(((left_x_min+(x*chunk_x))-xmin)*x_ratio)+col-95] = (float(X[row][col][3]))/255.0
                    # X_final[row][col] = (float(X[row][col][3]))/255.0
            # X_final = X_final[108:472, 95:692]

            # print(X_final.shape)
    
    sparse_mat = sparse_mat.tocsr()

    sparse.save_npz("fires/"+cur_row['an_origine']+"/"+str(idx)+".npz", sparse_mat)

    # fires.append(sparse_mat)
    del sparse_mat, fig, ax

os.system("sudo poweroff")