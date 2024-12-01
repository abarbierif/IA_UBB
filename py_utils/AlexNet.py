from keras.src import layers
from keras.src.applications import imagenet_utils
from keras.src.models import Functional
from keras.src import backend

def AlexNet(
    include_top=True,
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
):
    """Instantiates the AlexNet architecture."""

    # Determine proper input shape
    input_shape = imagenet_utils.obtain_input_shape(
        input_shape,
        default_size=227,
        min_size=32,
        data_format=backend.image_data_format(),
        require_flatten=include_top,
    )

    if input_tensor is None:
        img_input = layers.Input(shape=input_shape)
    else:
        if not backend.is_keras_tensor(input_tensor):
            img_input = layers.Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor

    # 1st layer (conv + pool + batchnorm)
    x = layers.Conv2D(filters=96, kernel_size=(11, 11), activation='relu', strides=(4, 4), padding="valid", name="conv1")(img_input)
    x = layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name="pool1")(x)
    x = layers.BatchNormalization(name="bn1")(x)

    # 2nd layer (conv + pool + batchnorm)
    x = layers.Conv2D(filters=256, kernel_size=(5, 5), activation='relu', strides=(1, 1), padding="same", name="conv2")(x)
    x = layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name="pool2")(x)
    x = layers.BatchNormalization(name="bn2")(x)

    # layer 3 (conv + batchnorm)      <--- note that the authors did not add a POOL layer here
    x = layers.Conv2D(filters=384, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding="same", name="conv3")(x)
    x = layers.BatchNormalization(name="bn3")(x)

    # layer 4 (conv + batchnorm)      <--- similar to layer 3
    x = layers.Conv2D(filters=384, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding="same", name="conv4")(x)
    x = layers.BatchNormalization(name="bn4")(x)

    # layer 5 (conv + batchnorm)
    x = layers.Conv2D(filters=256, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding="same", name="conv5")(x)
    x = layers.BatchNormalization(name="bn5")(x)
    x = layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name="pool5")(x)

    #classifier
    if include_top:
        # Flatten the CNN output to feed it with fully connected layers
        x = layers.Flatten(name="flatten")(x)

        # layer 6 (Dense layer + dropout)
        x = layers.Dense(4096, activation='relu', name="fc6")(x)
        x = layers.Dropout(0.5)(x)

        # layer 7 (Dense layer + dropout)
        x = layers.Dense(4096, activation='relu', name="fc7")(x)
        x = layers.Dropout(0.5)(x)

        # layer 8 (Dense layer)
        x = layers.Dense(classes, activation=classifier_activation, name="fc8")(x)
    else:
        if pooling == "avg":
            x = layers.GlobalAveragePooling2D()(x)
        elif pooling == "max":
            x = layers.GlobalMaxPooling2D()(x)
        elif pooling == None:
            x = layers.Flatten(name="flatten")(x)

    # Create model
    model = Functional(img_input, x, name="alexnet")

    return model