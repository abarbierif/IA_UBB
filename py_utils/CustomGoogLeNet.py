from GoogLeNet import *

class CustomGoogLeNet:
    def __init__(self,
                 auxiliary_classifiers=True,
                 input_shape=None,
                 classes=1000,
                 classifier_activation="softmax",
                 ):

        self.auxiliary_classifiers = auxiliary_classifiers  
        self.input_shape = input_shape
        self.classes = classes
        self.classifier_activation = classifier_activation
        
        self.model = GoogLeNet(auxiliary_classifiers=self.auxiliary_classifiers,
                               input_shape=self.input_shape,
                               classes=self.classes,
                               classifier_activation=self.classifier_activation)


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
                           jit_compile=jit_compile)
        
        if validation_data is not None:
          validation_data=(preprocess_input(validation_data[0]),validation_data[1])

        history = self.model.fit(x=x,
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
                                 validation_freq=validation_freq)

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
                 **kwargs):
      
        if filepath != None:
          self.model.load_weights(filepath=filepath)
          
        score = self.model.evaluate(x=x,
                                    y=y,
                                    batch_size=batch_size,
                                    verbose=verbose,
                                    sample_weight=sample_weight,
                                    steps=steps,
                                    callbacks=callbacks,
                                    return_dict=return_dict,
                                    **kwargs)

        return score

    def predict(self,
                x,
                batch_size=None,
                verbose="auto",
                steps=None,
                callbacks=None):

        predicted_probs = self.model.predict(x=x,
                                             batch_size=batch_size,
                                             verbose=verbose,
                                             steps=steps,
                                             callbacks=callbacks)

        return predicted_probs
