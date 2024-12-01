#libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2
import tensorflow_datasets as tfds

def channels_expand(X):
    return np.dstack((X,X,X))

#
def load_data(source, to, path=None, dataset=None, dims=(128,128), failures_only=True, three_channels=False):
    match source:
        case 'dir':
            return from_dir(path, to, dims)
        case 'tfds':
            return from_tfdataset(dataset, to, dims)
        case 'wm811k':
            return load_wm811k(path, to, dims=dims, failures_only=failures_only, three_channels=three_channels)


#
def from_dir(path, to, dims=(128,128)):
    labels = sorted(os.listdir(path))
    images_list = []
    labels_list = []
    for label in labels:
        dir_path = os.path.join(path, label)
        for img_name in sorted(os.listdir(dir_path)):
            img_path = os.path.join(dir_path, img_name)
            image = cv2.imread(img_path)

            if to == 'ndarray':
                image = cv2.resize(image, dims)

            if len(image.shape) == 2:
                image = np.expand_dims(image, -1)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            images_list.append(image)
            labels_list.append(label)

    if to == 'ndarray':
        return np.array(images_list), np.array(labels_list)
    elif to == 'list':
        return images_list, labels_list

    
#
def from_tfdataset(dataset, to, dims=(128,128)):

    ds, ds_info = tfds.load(dataset, split='all', as_supervised=True, with_info=True)
    ds_numpy = tfds.as_numpy(ds)

    images_list = []
    labels_list = []
    for _ in ds_numpy:
        image, label = _

        if to == 'ndarray':
            image = cv2.resize(image, dims)
        
        if len(image.shape) == 2:
            image = np.expand_dims(image, -1)
        
        images_list.append(image)
        labels_list.append(label)
        
    if to == 'ndarray':
        return np.array(images_list), np.array(labels_list)
    elif to == 'list':
        return images_list, labels_list, ds_info

#
def load_wm811k(pkl_file, to, dims=(128,128), failures_only=True, three_channels=False):
    df = pd.read_pickle(pkl_file)
    
    df['failureType'] = df['failureType'].apply(lambda x: 'not-labeled' if type(x) == np.ndarray else x)
    df['trainTestLabel'] = df['trainTestLabel'].apply(lambda x: 'not-labeled' if type(x) == np.ndarray else x)
    
    if failures_only == True:
      df.drop(index=df[df['failureType'] == 'none'].index, inplace=True)
      df.drop(index=df[df['failureType'] == 'not-labeled'].index, inplace=True)
    else:
      pass
      
    images_list = []
    labels_list = []

    for _ in range(len(df)):
        image = df.iloc[_]['waferMap']
        label = df.iloc[_]['failureType']

        if df.iloc[_]['trainTestLabel'] == 'Training' or df.iloc[_]['trainTestLabel'] == 'Test':     
            if to == 'ndarray':
                image = cv2.resize(image, dims)
                
            if three_channels == True:
                image = channels_expand(image)

            if len(image.shape) == 2:
                image = np.expand_dims(image, -1)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            images_list.append(image)
            labels_list.append(label)

    if to == 'ndarray':
        return np.array(images_list), np.array(labels_list)
    elif to == 'list':
        return images_list, labels_list
    
    
if __name__ == '__main__':
    print('executed successfully!')