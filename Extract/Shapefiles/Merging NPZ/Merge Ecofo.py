import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import sys
# from get_plot import get_plot
from scipy import sparse
from sklearn.preprocessing import normalize

directory_base = "D:/Users/xubil/OneDrive/Documents/Wildfires Data NPZ/Foret Raw/ecoforet"

items = ["F", "M", "R"] # , "None" 

smat = [sparse.load_npz(directory_base+"/F.npz").tocsr(), 
        sparse.load_npz(directory_base+"/M.npz").tocsr(), 
        sparse.load_npz(directory_base+"/R.npz").tocsr(), 
        # sparse.load_npz(directory_base+"/None.npz").tocsr()
]

for i in range(1, 6):
    for j in range(len(items)):
        next = sparse.load_npz(directory_base+""+str(i)+"/"+items[j]+".npz").tocsr()
        smat[j] += next

for i in range(len(smat)):
    sparse.save_npz("D:/Users/xubil/OneDrive/Documents/Wildfires Data NPZ/Foret Raw/"+items[i]+".npz", normalize(smat[i], copy=False))
