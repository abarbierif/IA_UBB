#libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import pandas as pd
import sys
from tensorflow.keras.utils import to_categorical

def preprocess_data(preprocess, images_ndarray=None, images_list=None, thresh=30, labels_ndarray=None):
    match preprocess:
        case 'simple':
            return simple(images_ndarray)
        case 'batch_normalization':
            return batch_normalization(images_ndarray)
        case 'crop':
            return crop(images_list, thresh)
        case 'onehot_encoding':
            return onehot_encoding(labels_ndarray)

#
def simple(images_ndarray):
    return images_ndarray/255.0

#
def batch_normalization(images_ndarray):
    return (images_ndarray - np.mean(images_ndarray))/(np.std(images_ndarray) + 1e-07)

#
def crop(images_list, thresh=30):
  images_list_cropped = []
  for image in images_list:
    if len(image.shape)==2 or (len(image.shape)==3 and image.shape[-1]==1):
        image_gray = image
    else:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_binarized = (image_gray > thresh).astype(np.uint8)
    image_filtered = cv2.medianBlur(image_binarized, 5)
    image_coords = np.argwhere(image_filtered)
    y_max = np.max(image_coords[:,0])
    y_min = np.min(image_coords[:,0])
    x_max = np.max(image_coords[:,1])
    x_min = np.min(image_coords[:,1])
    image_cropped = image[y_min:y_max, x_min:x_max]
    images_list_cropped.append(image_cropped)

  return images_list_cropped

#
def onehot_encoding(labels_ndarray):
    num_labels = len(np.unique(labels_ndarray))
    if isinstance(labels_ndarray[np.random.randint(labels_ndarray.shape[0])], int) == False:
        labels_map = {label:number for number,label in enumerate(np.unique(labels_ndarray))}
        labels_ndarray = np.array([labels_map[label] for label in labels_ndarray])

    return to_categorical(labels_ndarray, num_labels)