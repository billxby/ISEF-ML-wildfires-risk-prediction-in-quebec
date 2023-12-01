import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import sys
# from get_plot import get_plot
from scipy import sparse
from sklearn.preprocessing import normalize

directory_base = "D:/Users/xubil/OneDrive/Documents/Wildfires Data NPZ/dmti_transmissionlines_2021_l_arc"

items = ["POWER", "TELEPHONE OTHER"]

smat = sparse.load_npz(directory_base+"/"+items[0]+".npz").tocsr()
# print(smat.shape)

for i in range(1, 2):
    next = sparse.load_npz(directory_base+"/"+items[i]+".npz").tocsr()
    # print(next.shape)
    smat += next

sparse.save_npz("D:/Users/xubil/OneDrive/Documents/Wildfires Data NPZ/dmti_transmissionlines_2021_l_arc/Lignes", smat)
