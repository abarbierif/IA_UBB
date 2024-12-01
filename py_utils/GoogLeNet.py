from tensorflow.keras.layers import Conv2D, MaxPool2D, concatenate

#inception module
def inception_module(x,
                filters_1x1,
                filters_3x3_reduce, filters_3x3,
                filters_5x5_reduce, filters_5x5,
                filters_max_pool_reduce,
                name=None):

    conv_1x1 = Conv2D(filters=filters_1x1, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(x)

    conv_3x3_reduce = Conv2D(filters=filters_3x3_reduce, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(x)
    conv_3x3 = Conv2D(filters=filters_3x3, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu')(conv_3x3_reduce)

    conv_5x5_reduce = Conv2D(filters=filters_5x5_reduce, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(x)
    conv_5x5 = Conv2D(filters=filters_5x5, kernel_size=(5,5), strides=(1,1), padding='same', activation='relu')(conv_5x5_reduce)

    max_pool = MaxPool2D(pool_size=(3,3), strides=(1,1), padding='same')(x)
    max_pool_reduce = Conv2D(filters=filters_max_pool_reduce, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(max_pool)

    output = concatenate([conv_1x1, conv_3x3, conv_5x5, max_pool_reduce], axis=3, name=name)

    return output
  
  
#GoogLeNet Architecture (InceptionV1)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, AveragePooling2D, Flatten, Dropout, Dense


def GoogLeNet(
  	auxiliary_classifiers=True,
	input_shape=(224,224,3),
	classes=1000,
	classifier_activation="softmax"):

  input_layer = Input(shape=input_shape)

  #Part A
  x = Conv2D(filters=64, kernel_size=(7,7), strides=(2,2), padding='same', activation='relu')(input_layer)
  x = MaxPool2D(pool_size=(3,3), strides=(2,2), padding='same')(x)
  x = Conv2D(filters=64, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(x)
  x = Conv2D(filters=192, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu')(x)
  x = MaxPool2D(pool_size=(3,3), strides=(2,2), padding='same')(x)

  #Part B
  x = inception_module(x,
                  filters_1x1=64,
                  filters_3x3_reduce=96, filters_3x3=128,
                  filters_5x5_reduce=16, filters_5x5=32,
                  filters_max_pool_reduce=32,
                  name='3a')

  x = inception_module(x,
                  filters_1x1=128,
                  filters_3x3_reduce=128, filters_3x3=192,
                  filters_5x5_reduce=32, filters_5x5=96,
                  filters_max_pool_reduce=64,
                  name='3b')

  x = MaxPool2D(pool_size=(3,3), strides=(2,2), padding='same')(x)

  x = inception_module(x,
                  filters_1x1=192,
                  filters_3x3_reduce=96, filters_3x3=208,
                  filters_5x5_reduce=16, filters_5x5=48,
                  filters_max_pool_reduce=64,
                  name='4a')

  classifier_1 = AveragePooling2D(pool_size=(5,5), strides=(3,3), padding='valid')(x)
  classifier_1 = Conv2D(filters=128, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(classifier_1)
  classifier_1 = Flatten()(classifier_1)
  classifier_1 = Dense(1024, activation='relu')(classifier_1)
  classifier_1 = Dropout(rate=0.7)(classifier_1)
  classifier_1 = Dense(classes, activation='softmax')(classifier_1)

  x = inception_module(x,
                  filters_1x1=160,
                  filters_3x3_reduce=112, filters_3x3=224,
                  filters_5x5_reduce=24, filters_5x5=64,
                  filters_max_pool_reduce=64,
                  name='4b')

  x = inception_module(x,
                  filters_1x1=128,
                  filters_3x3_reduce=128, filters_3x3=256,
                  filters_5x5_reduce=24, filters_5x5=64,
                  filters_max_pool_reduce=64,
                  name='4c')

  x = inception_module(x,
                  filters_1x1=112,
                  filters_3x3_reduce=144, filters_3x3=288,
                  filters_5x5_reduce=32, filters_5x5=64,
                  filters_max_pool_reduce=64,
                  name='4d')

  classifier_2 = AveragePooling2D(pool_size=(5,5), strides=(3,3), padding='valid')(x)
  classifier_2 = Conv2D(filters=128, kernel_size=(1,1), strides=(1,1), padding='same', activation='relu')(classifier_2)
  classifier_2 = Flatten()(classifier_2)
  classifier_2 = Dense(1024, activation='relu')(classifier_2)
  classifier_2 = Dropout(rate=0.7)(classifier_2)
  classifier_2 = Dense(classes, activation='softmax')(classifier_2)

  x = inception_module(x,
                  filters_1x1=256,
                  filters_3x3_reduce=160, filters_3x3=320,
                  filters_5x5_reduce=32, filters_5x5=128,
                  filters_max_pool_reduce=128,
                  name='4e')

  x = MaxPool2D(pool_size=(3,3), strides=(2,2), padding='same')(x)

  x = inception_module(x,
                  filters_1x1=256,
                  filters_3x3_reduce=160, filters_3x3=320,
                  filters_5x5_reduce=32, filters_5x5=128,
                  filters_max_pool_reduce=128,
                  name='5a')

  x = inception_module(x,
                  filters_1x1=384,
                  filters_3x3_reduce=192, filters_3x3=384,
                  filters_5x5_reduce=48, filters_5x5=128,
                  filters_max_pool_reduce=128,
                  name='5b')
  
  #Part C
  x = AveragePooling2D(pool_size=(7,7), strides=(1,1), padding='valid')(x)
  x = Dropout(rate=0.4)(x)
  x = Dense(classes, activation=classifier_activation)(x)
  
  if auxiliary_classifiers == True:
    googlenet = Model(inputs=input_layer, outputs = [x,classifier_1,classifier_2])
  else:
    googlenet = Model(inputs=input_layer, outputs = [x])
  
  
  return googlenet