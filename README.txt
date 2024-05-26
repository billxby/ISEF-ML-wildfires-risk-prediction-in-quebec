# Predicting Wildfire Ignition Risks in Quebec with Machine Learning
This is a science fair project aiming to forecast wildfire occurence risks in regions of Quebec based on topography, hydrography, meteorological, and human activity data. 

### Datasets Used
SOPFEU Statistics. https://sopfeu.qc.ca/en/statistics/
Données Québec. https://www.donneesquebec.ca/recherche/fr/dataset/feux-de-foret 
Geoindex. https://geoapp.bibl.ulaval.ca/
NASA AppEEARS (GIS Observations): https://appeears.earthdatacloud.nasa.gov/


### Getting Started

For additional questions or help on running certain parts of the code, please email: xubill0707@gmail.com

See pip_list.txt for the required libraries and the python version.
A few of the files are Jupyter Notebooks, be ready to run .ipynb files. 
Python should be able to run on any OS with the right python version installed. 

Here is an explanation of each folder and subfolder's use:

1. /data:
This folder contains the links to the data I have obtained or used to generate my training datasets

2. /data-demo:
This folder contains some demo testing datasets for the plotly web app under the /Visualisation folder to navigate
sample test cases with the model's output and the expected output. 

3. /data-training:
This folder contains the bounds of all the bounding boxes (Chunks) that are then used to crop off the static geographic
features in the /data folder or to call the NASA AppEEARS API to obtain Temporal Chunk files also in the /data folder. 

4. /Extract:
This folder contains all of the process to extract the initial data before processing them and merging them into training
datasets. 
Subfolders:
    a. NASA API:
    This subfolder contains the code to call the API for the appropriate chunks and then downloading the results of the API
    call and saving the results as a Chunk .npy file (numpy file). The `/Google Cloud Instances` inside the NASA API folder is the same fetch
    requests code but converted into runable Google Cloud Instance scripts to be run on the cloud to have multiple files
    running at the same time and speed up the extraction process. The appropriate chunks borders are also generated
    in this subfolder. 

    Helpful link: https://github.com/nasa/AppEEARS-Data-Resources/blob/main/Python/tutorials/AppEEARS_API_Area.ipynb 

    To use the files in extract, create a new .env file in the NASA API folder and add the following variables:
        EARTHDATA_USERNAME = "$username" 
        EARTHDATA_PASSWORD = "$password" 
    Both variables as strings without the ""
        e.g. EARTHDATA_USERNAME = BillXu7
    
    b. Requests:
    This subfolder contains the IDs of the API calls we have made. This way, we can fetch the request just by calling the
    appropriate task id. 
    Note: Only the account holder can call the task ID and fetch the result. 

    c. Shapefiles:
    This subfolder contains the code I used to convert each shapefile into a sparse matrix that can be used to process training
    data later. To do this, I split the shapefile into different chunks (smaller images), which I turned into a matrix. I then
    merged all of the small chunks together into a single large matrix and as a sparse matrix to not take too much memory (RAM). 
    The `Merging NPZ` sub-subfolder demonstrates how I extracted three sample shapefiles and the `extract_shp_main.ipynb` file
    gives the overall logic. 
    The Google Cloud Instances sub-subfolder is the extraction file converted to a python script to run on the cloud and more
    conveniently. 

    d. Visualisation:
    This subfolder was to visualize the ignition points dataset, but finally it was not used anywhere in my project. 

    e.1 coords.json: the coordinate bounds for the Shapefiles folder
    e.2 processed_files.npy: serves the role of a file tracking which requests have been "visited" so we don't fetch the request again. 

5. /models
This folder contains the models that I have trained using K-fold cross validation pickled (models are from scikit-learn library)
A pickled variable is a variable from a python saved into a file, which can be loaded into any other python code as long as the python
and libraries/package versions are the same. 
The subfolders are Base (Base model) and Temporal (Temporal model)
Each of the subfolders have sub-subfolders. The folder `50 50` is the k-fold cross validation done on 50-50 split (50% igntion points,
50% no fire). The `Splits` folder contains the testing of different training data splits to determine the split generating the highest
model accuracy. The files ending in  `_acc.npy` in the sub-subfolders are a list with the average accuracy of the model type after 
K-fold cross validation. 

6. /Results View
This folder is a plotly web app to visualize and navigate sample test cases with the model's output and the expected output. 

7. /Training
This folder contains the code for the training and result display phase. Because they are Google Colab notebooks, I have exported them 
and placed them in the folder, but I will also provide the original links here: 
Preprocess Base Model: https://colab.research.google.com/drive/1_Yipd9ECoNqMjO5sT4nDnRLVYsM7Hlpn?usp=sharing 
ML Wildfires Base: https://colab.research.google.com/drive/1aGaxSHtGsIngKiWMH-fyjkOlxerYVaEg?usp=sharing (Training)
Preprocess Temporal Model: https://colab.research.google.com/drive/1bpZd_bTmljzfQqIympJD5CJaad2bpW56?usp=sharing 
ML Wildfires Temporal: https://colab.research.google.com/drive/18LcCmMdfLH7Fpe6xpfJIrXSLh9Ykp5L1?usp=sharing (Training)
Additionally, I will also provide the two additional notebooks that were used during the methodology revision to get lagged data and 
train a model with it: 
Preprocess Temporal Model Yesterday: https://colab.research.google.com/drive/1tpm3dumh7kwDnD-YyZpvocUjjJwUZ8Js?usp=sharing
ML Wildfires Temporal Yesterday: https://colab.research.google.com/drive/1i4mZIqf3ggBplc36-BA7T19LDkYTD1yN?usp=sharing 

Note: The folder directories in the Google Colab files are on my Google Drive, but the files the notebooks use 
have all been provided as links in the /data folder 

8. /Visualisation
This folder is a plotly web app to visualize and navigate the sparse matrices we have generated. 