import pandas as pd
import tciaclient
from tciaclient import *
# import skimage as image
import numpy as np
import matplotlib.pyplot as plt
import os,shutil
import zipfile,pathlib

os.chdir('/Volumes/Aadi WD/Capstone_Project')
#### defining a helper function #####
def getResponse(response):
    if response.getcode() is not 200:
        raise ValueError("Server returned an error")
    else:
        return response.read()

#### defining a function for image retireval and returning the list of all the paths ######
def image_retriever(json_df):
    pwd_=pathlib.Path('/Volumes/Aadi WD/Capstone_Project')
    series_UID=[i for i in json_df.SeriesInstanceUID]
    patient_id=[j for j in json_df.PatientID]
    ### retrieving images for all SreisInstanceUIDs

    folder_list=[]
    for num in range(len(series_UID)):

        response=client_connection.get_image(series_UID[num],downloadPath=pwd_,zipFileName="images.zip")
        
        fid=zipfile.ZipFile("images.zip")
        fid.extractall(patient_id[num])
        folder_list.append(str(pwd_)+"/"+str(patient_id[num]))
        print(str(num)+'/'+str(len(series_UID)))
    return folder_list

##### defining a function to unpack images from their individual directories into the directory for that particular disease ####

def image_unpacker(str_path):
    path_list=os.listdir(str_path)
    sub_folder_list=[]
    for subpath in path_list:
        sub_folder_list.append(os.path.join(str_path,subpath))
        # print(sub_folder_list)
        for image_files in sub_folder_list:
            image_folder_list=os.listdir(image_files)
            for files in image_folder_list:
            # print(files)
                shutil.move(os.path.join(image_files,files),os.path.join(str_path,files))


    return os.listdir(str_path)

#defining basic parameters for API call#
baseUrl="https://services.cancerimagingarchive.net/services/v4"
resource = "TCIA"

#### establishing connection to ####

client_connection=tciaclient.TCIAClient(baseUrl=baseUrl,resource=resource)

#### extracting images part1 #####
response=client_connection.get_series(collection="Lung-PET-CT-Dx",modality="PT")
str_response=getResponse(response)
series_df=pd.io.json.read_json(str_response)
# series_df=series_df[series_df.BodyPartExamined=="CHEST"]
images_list_1=image_retriever(series_df)

for path_ in images_list_1:
    if "A" in path_:
        shutil.move(path_,"Adenocarcinoma")
    if "B" in path_:
        shutil.move(path_,"Small Cell Carcinoma")
    if "G" in path_:
        shutil.move(path_,"Squamous Cell Carcinoma")

#### extracting images part2: Adding to Adenocarcinoma images #######
response2=client_connection.get_series(collection="TCGA-LUAD",modality="PT")
str_response2=getResponse(response2)
series_df2=pd.io.json.read_json(str_response2)
series_df2=series_df2[series_df2.BodyPartExamined=="LUNG"]
tcga_image_paths=image_retriever(series_df2)
tcga_image_paths=list(set(tcga_image_paths))

for a_paths in tcga_image_paths:
    if "TCGA" in a_paths:
        shutil.move(a_paths,"Adenocarcinoma")
        tcga_image_paths.pop(tcga_image_paths.index(a_paths))

#### extracting images part3: Adding to Squamous cell carcinoma images ######

response3=client_connection.get_series(collection="TCGA-LUSC",modality="PT")
str_response3=getResponse(response3)
series_df3=pd.io.json.read_json(str_response3)
series_df3=series_df3[series_df3.BodyPartExamined=="LUNG"]
tcga_scimage_paths=image_retriever(series_df3)
tcga_scimage_paths=list(set(tcga_scimage_paths))
for i in range(len(tcga_scimage_paths)):
    shutil.move(tcga_scimage_paths[i],"Squamous Cell Carcinoma")

# #### extracting images part4: Adding to squamous cell carcinoma images ######

# response4=client_connection.get_series(collection="CPTAC-LSCC",modality="PT")
# str_response4=getResponse(response4)
# series_df4=pd.io.json.read_json(str_response4)
# series_df4=series_df4[series_df4.BodyPartExamined=="LUNG"]
# cptac_sc_paths=image_retriever(series_df4)
# cptac_sc_paths=list(set(cptac_sc_paths))
# for i in range(len(cptac_sc_paths)):
#     shutil.move(cptac_sc_paths[i],"Squamous Cell Carcinoma")



# image_unpacker('Adenocarcinoma')
# image_unpacker('Small Cell Carcinoma')







