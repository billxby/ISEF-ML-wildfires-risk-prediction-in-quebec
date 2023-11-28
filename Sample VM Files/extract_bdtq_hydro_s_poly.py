import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
from scipy import sparse
import os



print("Started")

coords = {"limits": {
        "xmin":-8953229.45098,
        "xmax":-6750696.01502,
        "ymin":5559313.031810002,
        "ymax":6900707.257190002
    }}
mpl.rcParams['figure.dpi'] = 120

# Set resolution
mpl.rcParams['figure.dpi'] = 300

def get_plot(gdf, item, color):

    plots = []
    titles = []

    print("Processing item ", item)
    fig, ax = plt.subplots(facecolor=(0, 0, 0, 0))
    gdf.plot(ax=ax, color=color)
        # ax.axis('off')
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0, 0))
    # fig.savefig(str(item)+".png")
    plots.append((fig, ax))
    titles.append(item)

    return plots, titles

print("processing shit")
gdf = gpd.read_file("bdtq_hydro_s_poly/bdtq_hydro_s_poly.shp")
gdf = gdf.fillna("None")

plots,titles = get_plot(gdf, "bdtq_hydro_s_poly", "white")
xmin, xmax, ymin, ymax = int(coords["limits"]["xmin"]), int(coords["limits"]["xmax"]), int(coords["limits"]["ymin"]), int(coords["limits"]["ymax"])

# Matrix Size:
# Limits: [108:472, 95:692]

# y length
ylen = 472-108

# x length
xlen = 692-95

split = 100
cur_plot = 2

final_mat = []

for main_idx in range(len(plots)):

    final_mat_it = sparse.csr_matrix(np.empty((0, xlen*split)))

    for iy in range(split):

        new_row = sparse.csr_matrix(np.empty((ylen, 0)))

        for ix in range(split):
            plots[main_idx][1].axis([
                xmin+(((xmax-xmin)/split)*ix),
                xmin+(((xmax-xmin)/split)*(ix+1)),
                ymin+(((ymax-ymin)/split)*iy),
                ymin+(((ymax-ymin)/split)*(iy+1)),
            ])


            plots[main_idx][0].canvas.draw()

            X = np.array(plots[main_idx][0].canvas.renderer.buffer_rgba())
            X_final = np.zeros((len(X), len(X[0])))

            # convert matrix to a 0-1 scale to save space
            # print(ix, iy)

            for row in range(len(X)):
                for col in range(len(X[row])):
                    X_final[row][col] = (float(X[row][col][3]))/255.0
            X_final = X_final[108:472, 95:692]


            # figx, axX = plt.subplots()
            # axX.set_title("x"+str(ix)+"y"+str(iy))
            # axX.matshow(X_final)

            new_row = sparse.hstack((new_row, sparse.csr_matrix(X_final)))
            del X_final
            # plt.close(figx)

        # print(new_row)

        final_mat_it = sparse.vstack((new_row, final_mat_it))
        del new_row

    sparse.save_npz("data/"+titles[main_idx]+".npz", final_mat_it)

    del final_mat_it

    # figx, axX = plt.subplots()
    # axX.set_title(titles[main_idx])
    # axX.matshow(final_mat_it)

    # final_mat.append(final_mat_it)

os.system("sudo poweroff")