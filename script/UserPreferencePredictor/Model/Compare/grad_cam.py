from .evaluate_network import EvaluateNetwork
import tensorflow as tf
import numpy as np
import cv2


class GradCam:
    def __init__(self, evaluate_network: EvaluateNetwork, input_image_size: tuple):
        self.evaluate_network = evaluate_network
        self.input_image_size = input_image_size

    def get_cam(self, image_array: np.array):
        K = tf.keras.backend
        y_c = self.evaluate_network.output[0]
        conv_output = self.evaluate_network.conv2d_2.output
        grads = K.gradients(y_c, conv_output)[0]

        input_image_array = np.array(
            [cv2.resize(image_array, self.input_image_size).astype(np.float32)/255])
        output, grads_val = K.function(
            [self.evaluate_network.input], [conv_output, grads])(input_image_array)
        output, grads_val = output[0, :], grads_val[0, :, :, :]

        weights = np.mean(grads_val, axis=(0, 1))
        cam = np.dot(output, weights)

        height, width, _ = image_array.shape
        # Process CAM
        cam = cv2.resize(cam, (width, height), cv2.INTER_LINEAR)
        cam = np.maximum(cam, 0)

        cam = (255*cam / cam.max()).astype(np.uint8)
        cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

        alpha = 0.5
        cam = cv2.addWeighted(image_array, alpha, cam, 1-alpha, 0)
        return cam
