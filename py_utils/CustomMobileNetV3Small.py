from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.initializers import GlorotUniform, Zeros

class CustomMobileNetV3Small:
  def __init__(self,
               input_shape=None,
               alpha=1.0,
               minimalistic=False,
               include_top=True,
               weights="imagenet",
               input_tensor=None,
               classes=1000,
               pooling=None,
               dropout_rate=0.2,
               classifier_activation="softmax",
               include_preprocessing=True,
               name="MobileNetV3Small",
               custom_classifier_layers=None,
               custom_classifier_neurons=None,
               custom_classifier_activation='relu',
               custom_classifier_batchnormalization=False,
               custom_classifier_dropout=False,
               dropout_rate_custom_classifier=None,
               fine_tuning=False,
               non_freeze_layers=None,
              ):
  
      #keras functions
      self.input_shape = input_shape
      self.alpha = alpha
      self.minimalistic = minimalistic
      self.include_top = include_top
      self.weights = weights
      self.input_tensor = input_tensor
      self.classes = classes
      self.pooling = pooling
      self.dropout_rate = dropout_rate
      self.classifier_activation = classifier_activation
      self.include_preprocessing = include_preprocessing
      self.name = name
      #custom classifier
      self.custom_classifier_layers = custom_classifier_layers
      self.custom_classifier_neurons = custom_classifier_neurons
      self.custom_classifier_activation = custom_classifier_activation
      self.custom_classifier_batchnormalization = custom_classifier_batchnormalization
      self.custom_classifier_dropout = custom_classifier_dropout
      self.dropout_rate = dropout_rate
      self.fine_tuning = fine_tuning
      self.non_freeze_layers = non_freeze_layers

      #model
      self.model = MobileNetV3Small(input_shape=self.input_shape,
                                    alpha=self.alpha,
      								minimalistic=self.minimalistic,
      								include_top=self.include_top,
                                    weights=self.weights,
                                    input_tensor=self.input_tensor,
                                    classes=self.classes,
                                    pooling=self.pooling,
                                    dropout_rate=self.dropout_rate,
                                    classifier_activation=self.classifier_activation,
                                    include_preprocessing=self.include_preprocessing,
                                    name=self.name
                              		)

      if self.fine_tuning:
        if self.non_freeze_layers == None: #all frozen layers
          for layer in self.model.layers:
            layer.trainable = False
        else:
          for layer in self.model.layers[:-self.non_freeze_layers]:
            layer.trainable = False

      if self.include_top == False:
        #add classifier

        #feature extractor output
        x = self.model.output
        x = GlobalAveragePooling2D()(x)

        #classifier
        if self.custom_classifier_layers != None:
          for custom_classifier_layer in range(self.custom_classifier_layers):
            x = Dense(self.custom_classifier_neurons, activation=self.custom_classifier_activation,
                      kernel_initializer=GlorotUniform(seed=1), bias_initializer=Zeros())(x)
            if self.custom_classifier_batchnormalization:
              x = BatchNormalization()(x)
            if self.custom_classifier_dropout:
              x = Dropout(dropout_rate_custom_classifier, seed=1)(x)
        else:
          pass

        #output layer
        x = Dense(self.classes, activation=self.classifier_activation,
                  kernel_initializer=GlorotUniform(seed=1), bias_initializer=Zeros())(x)

        #model
        self.model = Model(inputs=self.model.input, outputs=x)


  def train(self,
            optimizer="rmsprop",
            loss=None,
            loss_weights=None,
            metrics=None,
            weighted_metrics=None,
            run_eagerly=False,
            steps_per_execution=1,
            jit_compile="auto",
            x=None,
            y=None,
            batch_size=None,
            epochs=1,
            verbose="auto",
            callbacks=None,
            validation_split=0.0,
            validation_data=None,
            shuffle=True,
            class_weight=None,
            sample_weight=None,
            initial_epoch=0,
            steps_per_epoch=None,
            validation_steps=None,
            validation_batch_size=None,
            validation_freq=1
           ):

    self.model.compile(optimizer=optimizer,
                       loss=loss,
                       loss_weights=loss_weights,
                       metrics=metrics,
                       weighted_metrics=weighted_metrics,
                       run_eagerly=run_eagerly,
                       steps_per_execution=steps_per_execution,
                       jit_compile=jit_compile,
                      )
    
    if validation_data is not None:
      validation_data=(preprocess_input(validation_data[0]),validation_data[1])

    history = self.model.fit(x=preprocess_input(x),
                             y=y,
                             batch_size=batch_size,
                             epochs=epochs,
                             verbose=verbose,
                             callbacks=callbacks,
                             validation_split=validation_split,
                             validation_data=validation_data,
                             shuffle=shuffle,
                             class_weight=class_weight,
                             sample_weight=sample_weight,
                             initial_epoch=initial_epoch,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             validation_batch_size=validation_batch_size,
                             validation_freq=validation_freq
                            )

    return history

  def evaluate(self,
               filepath,
               x=None,
               y=None,
               batch_size=None,
               verbose="auto",
               sample_weight=None,
               steps=None,
               callbacks=None,
               return_dict=False,
               **kwargs
              ):
    
    if filepath != None:
      self.model.load_weights(filepath=filepath)
      
    score = self.model.evaluate(x=preprocess_input(x),
                                y=y,
                                batch_size=batch_size,
                                verbose=verbose,
                                sample_weight=sample_weight,
                                steps=steps,
                                callbacks=callbacks,
                                return_dict=return_dict,
                                **kwargs
                               )

    return score
      
  def predict(self,
              x,
              batch_size=None,
              verbose="auto",
              steps=None,
              callbacks=None
             ):
        
    predicted_probs = self.model.predict(x=preprocess_input(x),
                                         batch_size=batch_size,
                                         verbose=verbose,
                                         steps=steps,
                                         callbacks=callbacks
                                        )

    return predicted_probs