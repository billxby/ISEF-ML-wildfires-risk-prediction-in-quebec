import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib as mpl

# Set resolution
mpl.rcParams['figure.dpi'] = 300

def get_plot(gdf, target, color):
    uniques = gdf[target].unique()

    plots = []
    titles = []
    
    for item in uniques:
        print("Processing item ", item)
        fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
        gdf[gdf[target] == item].plot(ax=ax, color=color)
        # ax.axis('off')
        ax.set_axis_off()
        ax.set_facecolor((0, 0, 0, 0))
        # fig.savefig(str(item)+".png")
        plots.append((fig, ax))
        titles.append(item)
    
    return plots, titles


def get_full_plot(gdf, title, color):

    plots = []
    titles = []
    
    print("Processing item ", title)
    fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
    gdf.plot(ax=ax, color=color)
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0, 0))
    plots.append((fig, ax))
    titles.append(title)
    
    return plots, titles

