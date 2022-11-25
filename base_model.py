import csv

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers

import filenames
import init

base_model = keras.Sequential(
    [
        layers.Dense(1, input_shape=(131,), activation="sigmoid")
    ]
)
base_model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                   metrics=[tf.keras.metrics.BinaryAccuracy()],
                   run_eagerly=True)
base_model.fit(init.dataset_arm_training, init.labels_arm_training, epochs=10, batch_size=init.BATCH_SIZE,
               validation_data=(init.dataset_arm_validation, init.labels_arm_validation))
#
# weights = base_model.get_weights()
# print("weights: ", weights)

[_, binary_accuracy_base] = base_model.evaluate(init.dataset_arm_test, init.labels_arm_test)
print(binary_accuracy_base)
[[predict_base]] = base_model.predict(init.topredict)
print(predict_base)
base_model.save(filenames.base_model)

with open("files/Base-model.txt", "w") as f:
    f.write("Binary Accuracy: " + str(binary_accuracy_base) + "\nPrediction: " + str(predict_base))


