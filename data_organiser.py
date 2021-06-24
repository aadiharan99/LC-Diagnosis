"""
Created on Wed Mar 24 10:48:47 2021

@author: aadiharan99
"""
import os
import matplotlib.pyplot as plt
import re
import shutil
import pydicom
import skimage

# os.system('conda install pydicom')
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

# os.chdir('/Users/aadiharan99/OneDrive/VSCode workspace/Others/Capstone_Project')
# #### getting the path_list first

ac_path_list=os.listdir('Adenocarcinoma')
small_cell_path_list=os.listdir('Small Cell Carcinoma')
squamous_cell_path_list=os.listdir('Squamous Cell Carcinoma')

Lung_folders_pattern=re.compile('Lung')

lung_folder_list=[]
for path_ in squamous_cell_path_list:
    if Lung_folders_pattern.match(path_):
        lung_folder_list.append(path_)

cwd=os.getcwd()
# # print()

for lung_folder in lung_folder_list:
    file_list=os.listdir(cwd+'/'+'Squamous Cell Carcinoma'+'/'+lung_folder)
    if len(file_list)>0:
        for file in file_list:
            shutil.move(cwd+'/'+'Squamous Cell Carcinoma'+'/'+lung_folder+'/'+file,os.path.join(cwd,'Squamous Cell Carcinoma',file))
        # lung_folder_list.pop(lung_folder_list.index(lung_folder))
        print('Done')
        
C3N_pattern=re.compile('C3N')

C3N_folder_list=[]
for path_ in squamous_cell_path_list:
    if C3N_pattern.match(path_):
        C3N_folder_list.append(path_)
        
for C3N_folder in C3N_folder_list:
    file_list=os.listdir(cwd+'/'+'Squamous Cell Carcinoma'+'/'+C3N_folder)
    if len(file_list)>0:
        for file in file_list:
            shutil.move(cwd+'/'+'Squamous Cell Carcinoma'+'/'+C3N_folder+'/'+file,os.path.join(cwd,'Squamous Cell Carcinoma',file))
        # C3N_folder_list.pop(C3N_folder_list.index(C3N_folder))
        print('Done')
        
# TCGA_pattern=re.compile('TCGA')
# TCGA_folder_list=[]
# for path_ in squamous_cell_path_list:
#     if TCGA_pattern.match(path_):
#         TCGA_folder_list.append(path_)
        
# for TCGA_folder in TCGA_folder_list:
#     file_list=os.listdir(cwd+'/'+'Squamous Cell Carcinoma'+'/'+TCGA_folder)
#     if len(file_list)>0:
#         for file in file_list:
#             shutil.move(cwd+'/'+'Squamous Cell Carcinoma'+'/'+TCGA_folder+'/'+file,os.path.join(cwd,'Squamous Cell Carcinoma',file))
#         # TCGA_folder_list.pop(TCGA_folder_list.index(TCGA_folder))
#         print('Done')

# cwd_paths=os.listdir(os.getcwd()+'/'+'Small Cell Carcinoma')
# print(cwd_paths)
# small_cell_lung_folder_list=[]

# for file_path in cwd_paths:
#     if Lung_folders_pattern.match(file_path):
#         small_cell_lung_folder_list.append(file_path)
#         print(small_cell_lung_folder_list)

# # for folder in small_cell_lung_folder_list:
# #     shutil.move(os.path.join(os.getcwd(),folder),os.path.join(os.getcwd(),'Small Cell Carcinoma'))

# #### inserting all images #########
# for folder in small_cell_lung_folder_list:
#     file_list=os.listdir(os.getcwd()+'/'+'Small Cell Carcinoma'+'/'+folder)
#     if len(file_list)>0:
#         for file in file_list:
#             shutil.move(os.getcwd()+'/'+'Small Cell Carcinoma'+'/'+folder+'/'+file,os.path.join(os.getcwd(),'Small Cell Carcinoma',file))
#         # lung_folder_list.pop(lung_folder_list.index(lung_folder))
#         print('Done')


Squamous_cell_cwd=os.listdir(os.getcwd()+'/'+'Squamous Cell Carcinoma')
Squamous_cell_folder_list=[]
for file_path in Squamous_cell_cwd:
       
    Squamous_cell_folder_list.append(file_path)
    # print(Squamous_cell_folder_list)

for folder in Squamous_cell_folder_list:
    file_list=os.listdir(os.getcwd()+'/'+'Squamous Cell Carcinoma'+'/'+folder)
    if len(file_list)>0:
        for file in file_list:
            shutil.move(os.getcwd()+'/'+'Squamous Cell Carcinoma'+'/'+folder+'/'+file,os.path.join(os.getcwd(),'Squamous Cell Carcinoma',file))
        # lung_folder_list.pop(lung_folder_list.index(lung_folder))
        print('Done')




        

   
        
    



        
    