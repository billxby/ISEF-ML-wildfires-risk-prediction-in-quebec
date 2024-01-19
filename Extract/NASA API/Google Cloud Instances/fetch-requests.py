import requests as r
import getpass, pprint, time, os, cgi, json
import geopandas as gpd
import numpy as np
import shapely
from shapely import Polygon, to_geojson
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import shutil

api = 'https://appeears.earthdatacloud.nasa.gov/api/'  # Set the AρρEEARS API to a variable

load_dotenv()

params = {'limit': 1, 'pretty': True} # Limit API response to the most recent entry, return as pretty json
relevantFiles = [
    "MOD13A1.061__500m_16_days_EVI_",
    "MOD13A1.061__500m_16_days_NDVI_",
    "MOD15A2H.061_Lai_500m_",
    "DAYMET.004_prcp_",
    "DAYMET.004_tmax_",
    "DAYMET.004_tmin_",
]

fileOrder = ["prcp", "tmax", "tmin", "EVI", "NDVI", "Lai"]
originalRatio = [(7,6),(7,6),(7,6),(11,12),(11,12),(11,12)]

destDir = "Destination"
requestsDir = "R34"

processedFiles = [] #np.load("processed_files.npy") #[]

sawStartFile = False

for requestFile in os.listdir(requestsDir):
    if (requestFile == "cur_idx.npy"):
        continue
    if (requestFile in processedFiles):
        continue
    accId = requestFile[1:2]
    dashIndex = requestFile.index('-')
    endIndex = requestFile.index(".npy")
    if (endIndex == -1):
        continue
    print("---------------------------------")
    print(requestFile)
    print("---------------------------------")
    startChunk = int(requestFile[3:dashIndex])
    nonIncluEndChunk = int(requestFile[dashIndex+1:endIndex])
    
    ids = np.load(requestsDir+"/"+requestFile)
    user = os.getenv("EARTHDATA_USERNAME"+str(accId))
    password = os.getenv("EARTHDATA_PASSWORD"+str(accId))
    token_response = r.post('{}login'.format(api), auth=(user, password)).json() # Insert API URL, call login service, provide credentials & return json
    token = token_response['token']                      # Save login token to a variable
    head = {'Authorization': 'Bearer {}'.format(token)}  # Create a header to store token information, needed to submit a request
    
    # # To be fixed files
    # if (ids.shape[0] != nonIncluEndChunk-startChunk):
    #     missingFinalRequest.append(requestFile)

    for chunkIdx in range(0, ids.shape[0]):
        bundle = r.get('{}bundle/{}'.format(api,ids[chunkIdx]), headers=head).json()  
        files = {}
        for f in bundle['files']: files[f['file_id']] = f['file_name']   # Fill dictionary with file_id as keys and file_name as values

        finalRelevantFiles = []

        for deleteFile in os.listdir(destDir):
            os.remove(destDir+"/"+deleteFile)

        for f in files:
            filename = files[f]
            if (".tif" in filename):
                if (any(substring in filename for substring in relevantFiles) == True):
                    filename = files[f].split('/')[1]
                    finalRelevantFiles.append(filename)
                    dl = r.get('{}bundle/{}/{}'.format(api, ids[chunkIdx], f), headers=head, stream=True, allow_redirects = 'True')   
                    filepath = os.path.join(destDir, filename)                                                       # Create output file path
                    with open(filepath, 'wb') as f:                                                                  # Write file to dest dir
                        for data in dl.iter_content(chunk_size=8192): f.write(data)
        data = []
        badFile = ""

        for filename in finalRelevantFiles:
            print(destDir + "/" + filename)
            dem = gdal.Open(destDir + "/" + filename)
            if (dem is None):
                print("is none")
                data = []
                badFile = "_bad"
                break
            else:
                demBand = dem.GetRasterBand(1) 
                demData = demBand.ReadAsArray().astype('float') 
                demFill = demBand.GetNoDataValue()
                demData[demData == demFill] = np.nan
                # Arbitray 13 x 13 shape so no out of bounds 
                if (13-demData.shape[0] < 0 or 13-demData.shape[1] < 0):
                    data = []
                    print("Bad process")
                    badFile = "_bad"
                    break 
                demData = np.pad(demData, [(0, 13-demData.shape[0]), (0, 13-demData.shape[1]),], mode='constant')
                data.append(demData)

        dem = "a" # stops reading the file to allow deletion 
        print(np.array(data).shape)

        np.save("Chunks/"+str(chunkIdx+startChunk)+badFile, data)
    
    processedFiles = np.append(processedFiles, requestFile)
    np.save("processed_files", processedFiles)

count = 0

for bounds in Training["Human"]:
  newinput = np.array([])
  print("ok")
  print(newinput.shape)
  for dataset in data:
    # print(dataset)
    print("okk")
    minx, maxx, miny, maxy = boundsToMat(bounds, dataset.shape)

    data_raw = dataset[minx:maxx, miny:maxy].todense()
    if (data_raw.size == 0):
      print("isNone ok skip")
      continue
    data_process = cv2.resize(data_raw, dsize=(12, 12), interpolation=cv2.INTER_CUBIC).ravel()
    newinput = np.concatenate((newinput, data_process))

    print(data_process.shape)
    # print(data_process)
    # newinput = np.concatenate((newinput, data_process.ravel()))
    # print(dataset[minx:maxx, miny:maxy].todense().reshape(-1))
    # print(dataset[minx:maxx, miny:maxy].todense().reshape(-1)[0].shape)

  print(newinput)
  print(newinput.shape)

  if count >= 0:
    break
  count+=1