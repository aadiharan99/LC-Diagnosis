from keras.models import load_model
import sys
from keras_preprocessing.image import img_to_array
import cv2
from PIL import Image
import tensorflow as tf
import os
import ast

os.chdir("/Users/aadiharan99/Downloads/Capstone_Project")

test_image_path= sys.argv[1]



best_model=load_model("/Users/aadiharan99/Downloads/Capstone_Project/best_model.h5")
print("Model loaded....")
test_image=cv2.imread(test_image_path)
print("Reading Image.....")
test_image=cv2.cvtColor(test_image,cv2.COLOR_BGR2GRAY)
print("Preprocessing 1/3 steps completed....")
test_image=cv2.resize(test_image,(200,200))
print("Preprocessing 2/3 steps completed.....")
test_image=Image.fromarray(test_image)
test_image=img_to_array(test_image)
print("Preprocessing completed......")
test_image=tf.expand_dims(test_image,0)
print("Identifying type of Lung Cancer.....")
prediction=best_model.predict(test_image)
class_labels=["Adenocarcinoma","Squamous Cell Carcinoma","Small Cell Carcinoma"]
identified_category=class_labels[list(prediction[0]).index(1.0)]
print("The identified category of Lung Cancer from this image is: "+identified_category)
