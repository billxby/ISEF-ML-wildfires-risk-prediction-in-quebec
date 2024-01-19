import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import sys
# from get_plot import get_plot
from scipy import sparse
from sklearn.preprocessing import normalize

directory_base = r"D:\Users\xubil\OneDrive\Documents\Wildfires Data NPZ\Training\Ignore\Route"

items = ["Route1", "Route2", "Route3"]

smat = sparse.load_npz(directory_base+"/"+items[0]+".npz").tocsr()
# print(smat.shape)

for i in range(1, 3):
    next = sparse.load_npz(directory_base+"/"+items[i]+".npz").tocsr()
    # print(next.shape)
    smat += next

sparse.save_npz(r"D:\Users\xubil\OneDrive\Documents\Wildfires Data NPZ\Training\Ignore\Route", smat)
