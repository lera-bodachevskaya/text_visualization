import keras
import numpy as np
import matplotlib.pyplot as plt

from keras.applications import vgg16, inception_v3, resnet50, mobilenet
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

from Database import Database
from Image import Image


class ImageNN:
    model = None

    modelImageNN = 0

    def __init__(self, model):
        self.LoadingModel(model)

    def LoadingModel(self, model):
        if model == '0':
            self.model = resnet50.ResNet50(weights='imagenet')
        elif model == '1':
            self.model = mobilenet.MobileNet(weights='imagenet')
        else:
            self.model = vgg16.VGG16(weights='imagenet')

    def LoadingAndPreprocessingImage(self, url):
        # load an image in PIL format
        original = load_img(url, target_size=(224, 224))

        # convert the PIL image to a numpy array
        # IN PIL - image is in (width, height, channel)
        # In Numpy - image is in (height, width, channel) нормализация
        numpy_image = img_to_array(original)

        # lt.imshow(np.uint8(numpy_image))
        # plt.show()

        # Convert the image / images into batch format
        # expand_dims will add an extra dimension to the data at a particular axis
        # We want the input matrix to the network to be of the form (batchsize, height, width, channels)
        # Thus we add the extra dimension to the axis 0.
        image_batch = np.expand_dims(numpy_image, axis=0)

        return image_batch

    def PredictingObjectClass(self, image):
        url = image.url
        image_batch = self.LoadingAndPreprocessingImage(url)

        # prepare the image for the VGG model
        processed_image = vgg16.preprocess_input(image_batch.copy())

        # get the predicted probabilities for each class
        predictions = self.model.predict(processed_image)

        # convert the probabilities to class labels
        # We will get top 5 predictions which is the default
        label = decode_predictions(predictions)

        res = ''
        for elem in label[0]:
            res += str(elem[1]) + ' '

        image.tags = res

    def PredictingObjectClassByUrl(self, url):
                image_batch = self.LoadingAndPreprocessingImage(url)

                # prepare the image for the VGG model
                processed_image = vgg16.preprocess_input(image_batch.copy())

                # get the predicted probabilities for each class
                predictions = self.model.predict(processed_image)

                # convert the probabilities to class labels
                # We will get top 5 predictions which is the default
                label = decode_predictions(predictions)

                res = ''
                for elem in label[0]:
                    res += str(elem[1]) + '\n'

                return res
