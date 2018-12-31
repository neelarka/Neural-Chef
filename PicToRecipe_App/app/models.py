''' Predict vegitables code here '''
#imports
import keras
from keras.models import load_model
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing import image
import numpy as np
import pandas as pd

class PredictRawVeggies:

    ###########################################################################
    def __init__(self):
        #Load the model
        self.model = load_model("vgg19_pictoreceipe_1.h5")
        self.model._make_predict_function()
        #get the labels
        df_labels = pd.read_csv("labels.csv")
        self.labels= list(df_labels['Label'])

    ######################################################################
    def call_predict(self, images, folder):

        predictions = []
        #predict
        for image_name in images:
            image_path = folder+ "\\" +image_name
            print(f"imagepath: {image_path}")
            test_image = keras.preprocessing.image.load_img(image_path, target_size=(224,224), grayscale=False)
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            test_image = preprocess_input(test_image)
            print(test_image)
            predict = self.model.predict(test_image)
            print(predict)
            zip_pred= zip(predict[0], self.labels)
            for pred_value, pred in zip_pred:
                if (pred_value > 0):
                    predictions.append((image_name, pred))

        return predictions
