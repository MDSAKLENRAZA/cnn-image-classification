# -*- coding: utf-8 -*-
"""Image Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iWxmPURZn2g6jkaX1afcTPgFE9fg7QLO
"""

# import libarary
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""# Dataset"""

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

!kaggle datasets download -d salader/dogs-vs-cats --force

# unzip data

# unzip dataset
import zipfile
zip_ref = zipfile.ZipFile('/content/dogs-vs-cats.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

# library
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout

# Generator
import os
train_dataset=keras.utils.image_dataset_from_directory(
    directory='/content/train',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

validate_data=keras.utils.image_dataset_from_directory(
    directory='/content/test',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

# Normalize
def process(image,label):
    image=tf.cast(image/255.,tf.float32)
    return image,label
train_dataset=train_dataset.map(process)
validate_data=validate_data.map(process)

# Cnn model
# Define the CNN architecture
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3),padding="valid", activation='relu', input_shape=(256, 256, 3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2),strides=2,padding='valid'))

model.add(Conv2D(64, kernel_size=(3, 3),padding="valid", activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2),strides=2,padding='valid'))


model.add(Conv2D(128, kernel_size=(3, 3),padding="valid",activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2),strides=2,padding='valid'))


model.add(Flatten())


model.add(Dense(128, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))

model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history=model.fit(train_dataset,epochs=10,validation_data=validate_data)

# plot
import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

"""# showing overfiting gap"""

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

"""# Test image"""

import cv2

test_img=cv2.imread('/content/cat.10.jpg')

plt.imshow(test_img)

