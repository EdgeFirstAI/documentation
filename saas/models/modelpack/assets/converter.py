import tensorflow as tf
import numpy as np
import glob
import cv2

model_path = "model_tf" # Path to the TensorFlow saved mdoel
images_path = "coffeecup/*.jpg" # Conversion requires image samples for quantization.
input_shape = (480, 270) # Model (width, height) input shape.
output_path = "coffeecup-modelpack-multitask-t-1f54.tflite" # Path to save the TFLite model. 

def representative_data_gen():
    images = glob.glob(images_path)

    for image in images:
        image = cv2.imread(image)
        image = cv2.resize(image, input_shape)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32)
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        yield [image]

converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_model = converter.convert()
with open(output_path, "wb") as f:
    f.write(tflite_model)