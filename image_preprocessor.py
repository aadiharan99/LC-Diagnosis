import pydicom as dicom
import numpy as np
from numpy import interp
import os
import cv2
from skimage import morphology,restoration,transform
from torch.utils.data import DataLoader,Dataset
from torchvision import *
from sklearn.model_selection import train_test_split as tts
from progress.bar import IncrementalBar
from PIL import Image
from keras_preprocessing.image import img_to_array
print("packages imported")
class Progress:
    """
    Class to print progress bar instead of printing n times
    """
    def __init__(self, value, end,buffer, title='Preprocessing'):
        self.title = title
        #when calling in a for loop it doesn't include the last number
        self.end = end -1
        self.buffer = buffer
        self.value = value
        self.progress()

    def progress(self):
        maped = int(interp(self.value, [0, self.end], [0, self.buffer]))
        print(f'{self.title}: [{"#"*maped}{"-"*(self.buffer - maped)}]{self.value}/{self.end} {((self.value/self.end)*100):.2f}%', end='\r')
class data_preprocessing():
    """
    Class containing all functions used for preprocessing the binary numpy objects
    obtained from the dicom files
    """
    def image_preprocessor(self,path_):
        """
        Takes all dicom files in a directory, preprocesses the files by
        performing morphological transformations and returns the images in a numpy array.
        """
        count=0
        processed_array=[]
        ## loading the normalised images saved as npy file ##
        norm_images=np.load(path_,allow_pickle=True)
        print("Images loaded from npy,beginning preprocessing now......")
        bar=IncrementalBar('Preprocessing',max=norm_images.shape[0])
        ## iterating through the images to perform operations on each image ##
        for i in range(norm_images.shape[0]):
            ## defining a mask ##
            norm_images[i] = norm_images[i] * (np.max(norm_images[i]) - np.min(norm_images[i])) + np.min(norm_images[i])
            mask=morphology.opening(norm_images[i],np.ones((5, 5)))
            ## applying the mask to our normalised image ##
            final_image=mask*norm_images[i]
            ## normalising the final_image ##
            # final_image=(final_image-final_image.min())-(final_image.max()-final_image.min())

            final_image=Image.fromarray(final_image)
            final_image=img_to_array(final_image)
            processed_array.append(final_image)
            bar.next()
            # print(str(count)+' images processed....., appending in array now')
        bar.finish()
        return np.array(processed_array)

    def label_maker(self,np_array,cat):
        """
        function to make category wise labels for each of the 3 categories:
        Adenocarcinoma, Squamous Cell Carcinoma, Small Cell Carcinoma
        """
        label_list=[]
        for i in range(np_array.shape[0]):
            label_list.append(cat)
        return label_list

    def data_splitter(self,data,labels,test_size,random_state=42):
        """
        function to automate the train_test_split
        """
        x_train,x_test,y_train,y_test=tts(data,labels,test_size=test_size,random_state=random_state)
        return x_train,x_test,y_train,y_test
    
    def list_to_numpy(self,np_array):
        """
        function that simply used np.array() to convert to array
        """
        return np.array(np_array)
    
    def final_data_maker(self,array_1,array_2,array_3):
        """
        Basically concatenating three lists into one big list, used for creating
        the final data
        """
        final_list=[]
        for images in array_1:
            final_list.append(images)
        for images2 in array_2:
            final_list.append(images2)
        for images3 in array_3:
            final_list.append(images3)
        return self.list_to_numpy(final_list)
    
    def final_label_maker(self,array_1,array_2,array_3):
        """
        Concatenates all labels into one list and then returns the 
        'label encoded' array
        """
        final_array=self.final_data_maker(array_1, array_2, array_3)
        final_array=np.unique(final_array,return_inverse=True)[1]
        return final_array
    
    def load_from_npy(self,npy_path):
        """
        A function to easily call np.load() to retrieve data from numpy 
        binary files

        """
        print("Loading file from npy.......Done")
        return np.load(npy_path,allow_pickle=True)
        

##### classes to make pytorch dataset #####
class ArrayDataset(Dataset):
    "Dataset for numpy arrays based on fastai example: "
    
    def __init__(self, data, target):
        self.data = torch.from_numpy(data)
        self.target = torch.from_numpy(target)
        
        
    def __getitem__(self, index):
        x = self.data[index]
        y = self.target[index]
        
        
        
        return x, y
    
    def __len__(self):
        return len(self.data)

# class AdjustGamma(object):
#     def __call__(self, img):
#         return transforms.functional.adjust_gamma(img, 0.8, gain=1)

# class AdjustContrast(object):
#     def __call__(self, img):
#         return transforms.functional.adjust_contrast(img, 2)

# class AdjustBrightness(object):
#     def __call__(self, img):
#         return transforms.functional.adjust_brightness(img, 2)    


# dp=data_preprocessing()
# #run only once 
# # final_data=dp.final_data_maker(dp.image_preprocessor('processed_data/adenocarcinoma.npy'), dp.image_preprocessor('processed_data/squamous_cell.npy')
# # ,dp.image_preprocessor('processed_data/small_cell.npy'))
# # final_labels=dp.final_data_maker(dp.label_maker(dp.image_preprocessor('processed_data/adenocarcinoma.npy'), "Adenocarcinoma"), dp.label_maker(dp.image_preprocessor('processed_data/squamous_cell.npy'),"Squamous Cell Carcinoma")
# # ,dp.label_maker(dp.image_preprocessor("processed_data/small_cell.npy"),"Small Cell Carcinoma"))

# train_data,test_data,train_labels,test_labels=dp.data_splitter(dp.final_data_maker(dp.image_preprocessor('processed_data/adenocarcinoma.npy'), dp.image_preprocessor('processed_data/squamous_cell.npy')
# ,dp.image_preprocessor('processed_data/small_cell.npy')),dp.final_data_maker(dp.label_maker(dp.image_preprocessor('processed_data/adenocarcinoma.npy'), "Adenocarcinoma"), dp.label_maker(dp.image_preprocessor('processed_data/squamous_cell.npy'),"Squamous Cell Carcinoma")
# ,dp.label_maker(dp.image_preprocessor("processed_data/small_cell.npy"),"Small Cell Carcinoma")) , test_size=0.2)

# tr_data,val_data,tr_labels,val_labels=dp.data_splitter(train_data, train_labels, test_size=0.2)

# print(tr_data.shape,val_data.shape,test_data.shape,sep='\n')


